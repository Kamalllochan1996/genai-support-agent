from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_huggingface import HuggingFacePipeline

from transformers import pipeline
from app.langchain.rag_chain import run_rag




# -------------------------
# 1. Vector Store
# -------------------------

vector_store = Chroma(
    collection_name="documents",
    persist_directory="./data/chroma_db"
)


# -------------------------
# 2. Retrieval Configuration
# -------------------------

TOP_K = 3
MAX_DISTANCE = 1.5


# -------------------------
# 3. Local LLM
# -------------------------

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_new_tokens=200,
    temperature=0.1
)

llm = HuggingFacePipeline(
    pipeline=generator
)


# -------------------------
# 4. Prompt
# -------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are an enterprise knowledge assistant.

Answer the question using ONLY the provided context.

IMPORTANT:
If the context contains
"NO_RELEVANT_INFORMATION_FOUND",
do not try to answer the question.

Instead say:

"I don't have enough information in the
provided documents to answer this question."

Do not use your general knowledge.

Context:
{context}

Question:
{question}

Answer:
"""
)


# -------------------------
# 5. Retrieve Documents
# -------------------------

def retrieve_documents(question):

    results = vector_store.similarity_search_with_score(
        question,
        k=TOP_K
    )

    relevant_documents = []

    print("\nRetrieved results:")

    for document, distance in results:

        print(f"Distance: {distance}")
        print(f"Text: {document.page_content}")
        print("-" * 50)

        if distance <= MAX_DISTANCE:

            # Store distance inside metadata
            document.metadata["distance"] = distance

            relevant_documents.append(document)

    return relevant_documents


# -------------------------
# 6. Format Documents
# -------------------------

def format_documents(documents):

    if not documents:
        return "NO_RELEVANT_INFORMATION_FOUND"

    return "\n\n".join(
        document.page_content
        for document in documents
    )


# -------------------------
# 7. Prepare Retrieval
# -------------------------

def prepare_retrieval(question):

    documents = retrieve_documents(question)

    return {
        "question": question,
        "documents": documents,
        "context": format_documents(documents)
    }


# -------------------------
# 8. Generate Answer
# -------------------------

def generate_answer(data):

    prompt_input = {
        "context": data["context"],
        "question": data["question"]
    }

    response = (
        prompt
        | llm
        | StrOutputParser()
    ).invoke(prompt_input)

    return {
        "answer": response,
        "documents": data["documents"]
    }


# -------------------------
# 9. Final RAG Chain
# -------------------------

rag_chain = (
    RunnableLambda(prepare_retrieval)
    | RunnableLambda(generate_answer)
)


# -------------------------
# 10. Run RAG
# -------------------------

def run_rag(question):

    result = rag_chain.invoke(question)

    sources = []

    for document in result["documents"]:

        sources.append({
            "source": document.metadata.get("source"),
            "page": document.metadata.get("page"),
            "distance": document.metadata.get("distance")
        })

    return {
        "answer": result["answer"],
        "sources": sources
    }


# -------------------------
# 11. Test
# -------------------------

question = "How many casual leaves can I take?"

result = run_rag(question)


# -------------------------
# 12. Output
# -------------------------

print("\n" + "=" * 60)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")

if result["sources"]:

    for source in result["sources"]:

        print(
            f"- {source['source']} "
            f"(Page {source['page']}, "
            f"Distance: {source['distance']})"
        )

else:

    print("- No relevant sources found.")

print("\n" + "=" * 60)
# from app.langchain.rag_chain import run_rag


if __name__ == "__main__":

    question = "How many casual leaves can I take?"

    result = run_rag(question)

    print("\n" + "=" * 60)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    if result["sources"]:

        for source in result["sources"]:

            print(
                f"- {source['source']} "
                f"(Page {source['page']}, "
                f"Distance: {source['distance']})"
            )

    else:

        print("- No relevant sources found.")

    print("\n" + "=" * 60)