# import sys
# sys.path.append('D:/Vivek_Roushan/Sales_Agent/Code')
from .Code.Import_Libraries_and_Set_Up_Your_Environment import *





# Define the FastAPI app
app = FastAPI()

pdfs_directory = "uploads"
os.makedirs(pdfs_directory, exist_ok=True)
print("Directory 'uploads' created successfully")
uploaded_files = []

# Endpoint for uploading text files
@app.post("/upload/")
async def upload_file(files: list[UploadFile] = File(...) ):
    """
    This endpoint allows users to upload text files.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        dict: Message indicating the success or failure of the upload.
    """

    # pdfs_directory = "uploads"
    # os.makedirs(pdfs_directory, exist_ok=True)
    # print("Directory 'pdfs' created successfully")
    # uploaded_files = []

    for file in files:
        # file_name = file.filename
        # file_path = f"{pdfs_directory}/{file_name}"
        file_path = os.path.join(pdfs_directory, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        uploaded_files.append(file_path)
    
    
    # try:
    #     knowledge_base = process_and_create_knowledge_base()
    #     if knowledge_base:
    #         return {"message": "Knowledge base created successfully."}
    #     else:
    #         return {"error": "Failed to create knowledge base."}
    # except Exception as e:
    #     return {"error": str(e)}

def process_and_create_knowledge_base():
    """
    This function processes the uploaded files, splits the text into chunks, creates embeddings,
    and saves them to a Chroma vector database.
    Args:
        file_paths (list[str]): Paths to the uploaded files.
    Returns:
        RetrievalQA: The knowledge base object.
    """
    

    # try:
    # Load the text from the uploaded file
    # loader = TextLoader(file_path)
    loader = PyPDFDirectoryLoader("uploads")


    # documents = loader.load()
    data = loader.load_and_split()

    context = "\n".join(str(p.page_content) for p in data)

    # Split the text into chunks
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)


    # splits = text_splitter.split_documents(documents)
    texts = text_splitter.split_text(context)

    # Create embeddings for the text chunks
    embeddings = OpenAIEmbeddings()

    # Create the Chroma vector index and save the embeddings
    # vector_index = Chroma.from_documents(splits, embedding=embeddings).as_retriever()
    vector_index = Chroma.from_texts(texts, embeddings)
    retriever = vector_index.as_retriever()

    # Set up the knowledge base
    # llm = ChatOpenAI(temperature=0.9)
    # knowledge_base = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_index)
    # llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    return knowledge_base
    # except Exception as e:
    #     raise f"Error occurred while creating knowledge base from : {str(e)}"
         





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)