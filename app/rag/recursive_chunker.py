from langchain_text_splitters import RecursiveCharacterTextSplitter


def recursive_chunk_text(
    text: str,
    metadata: dict,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_text(text)

    documents = []

    for chunk_id, chunk in enumerate(chunks):

        chunk_metadata = metadata.copy()
        chunk_metadata["chunk_id"] = chunk_id

        documents.append({
            "text": chunk,
            "metadata": chunk_metadata
        })

    return documents