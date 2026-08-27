# from app.rag.embedding_service import EmbeddingService
# from app.rag.vector_store import VectorStore
# from app.llm.llm_service import LLMService

# from app.core.settings import settings
# class RAGService:

#     MAX_DISTANCE = 1.5

#     def __init__(self):

#         self.embedding_service = EmbeddingService()
#         self.vector_store = VectorStore()
#         self.llm = LLMService()

#     def answer(
#         self,
#         question: str,
#         history: list[dict] | None = None
#     ) -> dict:

#         if history is None:
#             history = []

#         query_embedding = (
#             self.embedding_service.embed_text(question)
#         )

#         # results = self.vector_store.search_with_scores(
#         #     query_embedding,
#         #     top_k=3
#         # )
#         results = self.vector_store.search_with_scores(
#                 query_embedding,
#                 top_k=settings.TOP_K
#             )

#         print("\nRetrieved results:")

#         for result in results:
#             print(
#                 f"Distance: {result['distance']}"
#             )
#             print(
#                 f"Text: {result['text']}"
#             )
#             print("-" * 50
#         )

#         relevant_results = [
#             result
#             for result in results
#             if result["distance"] <= settings.MAX_DISTANCE
#         ]

#         if not relevant_results:
#             return {
#                 "answer": (
#                     "I don't have enough information "
#                     "in the provided documents to answer this question."
#                 ),
#                 "sources": []
#             }

#         context = "\n\n".join(
#             result["text"]
#             for result in relevant_results
#         )

#         conversation = ""

#         for message in history:
#             conversation += (
#                 f"{message['role']}: "
#                 f"{message['content']}\n"
#             )

#         prompt = f"""
#     You are an enterprise knowledge assistant.

#     Answer the user's question using ONLY the
#     provided context.

#     Use the conversation history to understand
#     references such as "it", "that", "what about",
#     etc.

#     If the answer is not present in the context,
#     say that you do not have enough information.

#     Conversation history:
#     {conversation}

#     Context:
#     {context}

#     Current question:
#     {question}

#     Answer:
#     """

#         answer = self.llm.generate(prompt)

#         sources = []

#         for result in relevant_results:

#             source = result["metadata"].get("source")
#             page = result["metadata"].get("page")

#             sources.append({
#                 "source": source,
#                 "page": page
#             })

#         return {
#             "answer": answer,
#             "sources": sources
#         }

from app.rag.retriever import Retriever
from app.rag.prompt_builder import PromptBuilder
from app.llm.llm_service import LLMService


class RAGService:

    def __init__(self):

        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()

    def answer(
        self,
        question: str,
        history: list[dict] | None = None
    ) -> dict:

        if history is None:
            history = []

        relevant_results = self.retriever.retrieve(
            question
        )

        if not relevant_results:

            return {
                "answer": (
                    "I don't have enough information "
                    "in the provided documents to answer "
                    "this question."
                ),
                "sources": []
            }

        context = "\n\n".join(
            result["text"]
            for result in relevant_results
        )

        prompt = self.prompt_builder.build(
            question,
            context,
            history
        )

        answer = self.llm.generate(prompt)

        sources = []

        for result in relevant_results:

            sources.append({
                "source": result["metadata"].get("source"),
                "page": result["metadata"].get("page")
            })

        return {
            "answer": answer,
            "sources": sources
        }