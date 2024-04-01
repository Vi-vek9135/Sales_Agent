from Import_Libraries_and_Set_Up_Your_Environment import TextLoader, RecursiveCharacterTextSplitter, ChatOpenAI, Chroma, OpenAIEmbeddings, RetrievalQA




# from Import_Libraries_and_Set_Up_Your_Environment import *
# from Sales_conversation_stages import *


# Set up a knowledge base
def setup_knowledge_base():
    """
    We assume that the product knowledge base is simply a text file.
    """
    # load product catalog
    # with open(product_catalog, "r") as f:
    #     product_catalog = f.read()

    loader = TextLoader("Data/room.txt")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    llm = ChatOpenAI(temperature=0)
    splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

    # text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=0)
    # texts = text_splitter.split_text(product_catalog)

    # llm = ChatOpenAI(temperature=0)
    # embeddings = OpenAIEmbeddings()
    # docsearch = Chroma.from_texts(
    #     texts, embeddings, collection_name="product-knowledge-base"
    # )

    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    return knowledge_base




knowledge_base = setup_knowledge_base()
# knowledge_base.run("What products do you have available?")