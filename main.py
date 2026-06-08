from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embedder import get_embedding_model
from rag.vector_store import load_vector_store
from rag.chatbot import ask_rag

docs = load_pdf("data/sample.pdf")

chunks = split_documents(docs)

embeddings = get_embedding_model()

db = load_vector_store(embeddings)


while True:
    query = input("\nAsk Question: ")

    if query.lower() == "exit":
        break

    answer = ask_rag(
        query,
        db
    )

    print("\nAnswer:")
    print(answer)