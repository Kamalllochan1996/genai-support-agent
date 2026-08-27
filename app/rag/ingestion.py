from app.rag.document_loader import load_pdf
from app.rag.text_cleaner import clean_text
from app.rag.recursive_chunker import recursive_chunk_text
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


def ingest_pdf(file_path: str):

    # 1. Load PDF
    documents = load_pdf(file_path)

    # 2. Clean and chunk
    all_chunks = []

    for document in documents:

        cleaned_text = clean_text(
            document["text"]
        )

        chunks = recursive_chunk_text(
            cleaned_text,
            document["metadata"]
        )

        all_chunks.extend(chunks)

    print(f"Created {len(all_chunks)} chunks")

    # 3. Create embeddings
    embedding_service = EmbeddingService()

    embedded_documents = (
        embedding_service.embed_documents(
            all_chunks
        )
    )

    print("Embeddings created")

    # 4. Store in vector database
    vector_store = VectorStore()

    vector_store.add_documents(
        embedded_documents
    )

    print("Documents stored in ChromaDB")

    return len(embedded_documents)