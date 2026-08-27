def chunk_text(
    text: str,
    metadata: dict,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict]:

    chunks = []

    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = chunk_id

            chunks.append({
                "text": chunk,
                "metadata": chunk_metadata
            })

            chunk_id += 1

        start += chunk_size - overlap

    return chunks