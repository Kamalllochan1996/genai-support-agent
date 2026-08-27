from app.llm.llm_service import LLMService


llm = LLMService()

response = llm.generate(
    "Explain what RAG is in two sentences."
)

print(response)