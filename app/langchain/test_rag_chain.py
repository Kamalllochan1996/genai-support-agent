from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFacePipeline

from transformers import pipeline


# -------------------------
# 1. Vector Store
# -------------------------

vector_store = Chroma(
    collection_name="documents",
    persist_directory="./data/chroma_db"
)


retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3
    }
)


# -------------------------
# 2. Local LLM
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
# 3. Prompt
# -------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are an enterprise knowledge assistant.

Answer the question using ONLY the provided context.

If the answer is not present in the context,
say that you don't have enough information.

Context:
{context}

Question:
{question}

Answer:
"""
)


# -------------------------
# 4. Retrieve
# -------------------------

question = "How many casual leaves can I take?"

documents = retriever.invoke(question)


context = "\n\n".join(
    document.page_content
    for document in documents
)


# -------------------------
# 5. Build prompt
# -------------------------

messages = prompt.invoke({
    "context": context,
    "question": question
})


# -------------------------
# 6. Generate answer
# -------------------------

response = llm.invoke(messages)


print("\nQuestion:")
print(question)

print("\nAnswer:")
print(response)

print("\nSources:")

for document in documents:

    print(
        f"- {document.metadata.get('source')} "
        f"(Page {document.metadata.get('page')})"
    )