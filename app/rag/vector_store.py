import chromadb


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./data/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def add_documents(self, documents: list[dict]):

        ids = []
        texts = []
        embeddings = []
        metadatas = []

        for index, document in enumerate(documents):

            ids.append(
                f"{document['metadata']['source']}_"
                f"{document['metadata']['page']}_"
                f"{document['metadata']['chunk_id']}"
            )

            texts.append(document["text"])
            embeddings.append(document["embedding"])
            metadatas.append(document["metadata"])

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    def search_with_scores(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ) -> list[dict]:

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_documents = []

        for i, document in enumerate(results["documents"][0]):

            retrieved_documents.append({
                "text": document,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return retrieved_documents