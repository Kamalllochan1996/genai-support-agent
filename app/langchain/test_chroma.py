from langchain_chroma import Chroma


vector_store = Chroma(
    collection_name="documents",
    persist_directory="./data/chroma_db"
)


retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3
    }
)


question = "How many casual leaves can I take?"

documents = retriever.invoke(question)


for i, document in enumerate(documents):

    print(f"\n--- Result {i + 1} ---")

    print("Content:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)