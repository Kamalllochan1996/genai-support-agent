class PromptBuilder:

    def build(
        self,
        question: str,
        context: str,
        history: list[dict]
    ) -> str:

        conversation = ""

        for message in history:
            conversation += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        return f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the
provided context.

Use the conversation history to understand
references such as "it", "that", "what about",
etc.

If the answer is not present in the context,
say that you do not have enough information.

Conversation history:
{conversation}

Context:
{context}

Current question:
{question}

Answer:
"""
class RAGPromptBuilder:

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""
You are a helpful support assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided documents."

Do not invent or assume information.

Context:
--------------------
{context}
--------------------

User Question:
{question}

Answer:
""".strip()