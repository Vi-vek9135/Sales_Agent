# from Import_Libraries_and_Set_Up_Your_Environment import TextLoader, RecursiveCharacterTextSplitter, ChatOpenAI, Chroma, OpenAIEmbeddings, RetrievalQA
from Sales_conversation_stages import llm




from Import_Libraries_and_Set_Up_Your_Environment import *
# from Sales_conversation_stages import *


# Set up a knowledge base
def setup_knowledge_base():
    # """
    # We assume that the product knowledge base is simply a text file.
    # """
    # # load product catalog
    # # with open(product_catalog, "r") as f:
    # #     product_catalog = f.read()

    # loader = TextLoader("Data/room.txt")
    # documents = loader.load()

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # # llm = ChatOpenAI(temperature=0)
    # splits = text_splitter.split_documents(documents)
    # vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    # retriever = vectorstore.as_retriever()

    # # text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=0)
    # # texts = text_splitter.split_text(product_catalog)

    # # llm = ChatOpenAI(temperature=0.9)
    # # embeddings = OpenAIEmbeddings()
    # # docsearch = Chroma.from_texts(
    # #     texts, embeddings, collection_name="product-knowledge-base"
    # # )

    # knowledge_base = RetrievalQA.from_chain_type(
    #     llm=llm, chain_type="stuff", retriever=retriever
    # )
    # return knowledge_base



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




# knowledge_base = setup_knowledge_base()
# knowledge_base.run("What products do you have available?")
















