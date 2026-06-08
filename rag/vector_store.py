from langchain_chroma import Chroma

def create_vector_store(chunks, embeddings):
    vectordb = Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,
        persist_directory = "chroma_db"
    )

    return vectordb

def load_vector_store(embeddings):
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return vectordb