from fastapi import FastAPI,UploadFile ,File, HTTPException, status
import uvicorn
import os
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI



# Load environment variables for authentication
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Define the FastAPI app
app = FastAPI(title="Upload the room document")




# Declare vector_index globally
vector_index = None



# Endpoint for uploading PDF files
@app.post("/uploadpdf/")
async def upload_pdf(pdf_name: str, files: list[UploadFile] = File(...) ):
    """
    This endpoint allows users to upload PDF files.

    Args:
        pdf_name (str): Name of the PDF file to be uploaded.
        files (list[UploadFile]): List of uploaded files.

    Returns:
        dict: Message indicating the success or failure of the upload.
    """



    # Save the uploaded PDF file
    # Create the 'pdfs' directory if it doesn't exist
    pdfs_directory = "pdfs"
    os.makedirs(pdfs_directory, exist_ok=True)
    print("Directory 'pdfs' created successfully")
    uploaded_files = []
    for file in files:
        file_ext = file.filename.split(".").pop()
        
        # Check if the file is a PDF
        # if file_ext.lower() != "pdf":
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Only PDF files are allowed.")

        file_name = file.filename
        file_path = f"{pdfs_directory}/{file_name}"
        
        
        try:  
          # Save the uploaded file
          with open(file_path,"wb") as f:
              content = await file.read()
              f.write(content)
          uploaded_files.append(file_path)
        except Exception as e:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occured while  saving file: {e}"
          )


    try:
      # Load and split the uploaded PDF using PyPDFDirectoryLoader
      loader = PyPDFDirectoryLoader("pdfs")
      data = loader.load_and_split()
    except Exception as e:
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error occured while loading PDF: {e}"
      )


    # Combine page content into a single context string
    context = "\n".join(str(p.page_content) for p in data)

    # Split the Extracted Data into Text Chunks
    # Split the context into text chunks using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    context = "\n\n".join(str(p.page_content) for p in data)
    texts = text_splitter.split_text(context)
    # texts[0]


    # Save to Chroma Vector Database
    # Process and save the text chunks to Chroma Vector Database
    try:
      success_message = process_and_save_to_chroma(pdfs_directory, pdf_name)
      return {"message": success_message}
    except Exception as e:
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Error occured while processing and saving text: {e}"
      )





def process_and_save_to_chroma(pdf_path, pdf_name):
    
    """
    This function converts the text from a PDF into embeddings and saves them to Chroma.

    Args:
        pdf_path (str): Path to the PDF file.
        pdf_name (str): Name of the PDF file.

    Returns:
        str: Message indicating the success of the conversion and saving.
    """



    global vector_index  # Declare vector_index as a global variable


    if not os.path.exists(pdf_path):
      return f"Error: PDF file '{pdf_name}' not found at '{pdf_path}'"


    
    # Extract the text from the PDF's
    # Load and split the PDF text
    try:
      loader = PyPDFDirectoryLoader(pdf_path)
      data = loader.load_and_split()

      context = "\n".join(str(p.page_content) for p in data)

      # Split the Extracted Data into Text Chunks
      text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
      context = "\n\n".join(str(p.page_content) for p in data)
      texts = text_splitter.split_text(context)


      # Create embeddings for the text chunks
      embeddings = create_embeddings()


      # Chroma vector index and save the embeddings
      vector_index = Chroma.from_texts(texts, embeddings).as_retriever()
      return f"Document '{pdf_name}' successfully converted to embeddings and saved to Chroma DB."
    except Exception as e:
      return f"Error occured while processing PDF '{pdf_name}': {e}"



def create_embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    return embeddings





@app.post("/qa/")
async def perform_qa(pdf_name: str, question: str):
    # Search Chroma Vector Database for relevant segments
    try:
      relevant_segments = search_chroma_db(question)
      
      answer = get_answer_using_palm2(relevant_segments, question)
      
      return {"answer": answer}
    except Exception as e:
      return {"error": f"Error answering question or answer not found: {e}"}



def search_chroma_db(question):
    # Add code to query Chroma Vector Database based on user question
    docs = vector_index.get_relevant_documents(question)
    # return relevant_segments
    return docs



def get_answer_using_palm2(relevant_segments, question):
    prompt_template = """
      Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
      provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
      Context:\n {context}?\n
      Question: \n{question}\n

      Answer:
    """


    try:
      if not relevant_segments:
        return "Answer not available in the context."



      prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
      model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
      chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
      response = chain({"input_documents":relevant_segments, "question": question}, return_only_outputs=True)
      return response
    except Exception as e:
       return f"An error occurred while retrieving answer: {str(e)}"






if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",reload=True)











