from pathlib import Path

import chromadb

from app.ingestion.chunk import DocumentChunk


class ChromaVectorStore:

    def __init__(
        self,
        persist_directory: str = "data/chroma_db",
        collection_name: str = "support_documents",
    ):
        self.client = chromadb.PersistentClient(
            path=str(Path(persist_directory))
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:

        if not chunks:
            return

        ids = [
            f"{chunk.source}-{chunk.metadata['chunk_index']}"
            for chunk in chunks
        ]

        documents = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = [
            chunk.embedding
            for chunk in chunks
        ]

        metadatas = [
            chunk.metadata
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> list[dict]:

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        return [
            {
                "content": document,
                "metadata": metadata,
                "distance": distance,
            }
            for document, metadata, distance
            in zip(
                documents,
                metadatas,
                distances,
            )
        ]