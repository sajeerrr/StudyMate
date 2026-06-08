from rag.loader import load_pdf
from rag.splitter import split_documents

docs = load_pdf("data/sample.pdf")

chunk = split_documents(docs)

print(len(chunk))
print(chunk[3].page_content)