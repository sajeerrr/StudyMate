from rag.llm import generate_answer

def ask_rag(query, vectordb):
    docs = vectordb.similarity_search(
        query,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    you are a helpful study assistant.

    Answer ONLY using the provided context.

    If the answer is not found in the context,
    say:
    "I could not find that information in the document."

    Context:
    {content}

    Question:
    {query}

    Answer:
    """

    answer = generate_answer(prompt)

    return answer