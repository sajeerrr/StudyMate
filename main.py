from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.embedder import get_embedding_model
from rag.vector_store import create_vector_store

docs = load_pdf("data/sample.pdf")

chunks = split_documents(docs)

embeddings = get_embedding_model()

db = create_vector_store(
    chunks,
    embeddings
)


query = "What is the machine learning?"

results = db.similarity_search(
    query,
    k=3
)

print("\nRetrieved Chunks:\n")

for doc in results:
    print(doc.page_content)
    print("-" * 50)