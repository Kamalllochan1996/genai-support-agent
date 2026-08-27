from app.llm.llm_service import LLMService


llm = LLMService()


def evaluate_semantically(
    question: str,
    expected_answer: str,
    actual_answer: str
) -> bool:

    prompt = f"""
You are an evaluator for a Retrieval Augmented Generation system.

Evaluate whether the actual answer correctly answers the question
and conveys the same meaning as the expected answer.

Question:
{question}

Expected Answer:
{expected_answer}

Actual Answer:
{actual_answer}

Rules:

1. Ignore differences in wording.
2. Ignore capitalization and punctuation.
3. The actual answer does not need to be identical.
4. If the actual answer contains the correct information, return PASS.
5. If the actual answer is incorrect, incomplete, or contradicts
   the expected answer, return FAIL.

Return ONLY:

PASS

or

FAIL
"""

    result = llm.generate(prompt)

    result = result.strip().upper()

    return result == "PASS"