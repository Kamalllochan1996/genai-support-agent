from app.llm.llm_service import LLMService


llm = LLMService()


# ============================================================
# 1. Context Relevance
# ============================================================

def evaluate_context_relevance(
    question: str,
    context: str
) -> bool:

    prompt = f"""
You are evaluating the retrieval quality of a RAG system.

Determine whether the provided context is relevant
to the user's question.

Question:
{question}

Context:
{context}

Rules:

1. The context should contain information useful for
   answering the question.
2. If the context is clearly unrelated, return FAIL.
3. If the context is relevant, return PASS.

Return ONLY:

PASS

or

FAIL
"""

    result = llm.generate(prompt)

    return result.strip().upper() == "PASS"


# ============================================================
# 2. Faithfulness
# ============================================================

def evaluate_faithfulness(
    context: str,
    answer: str
) -> bool:

    prompt = f"""
You are evaluating the faithfulness of a RAG system.

Determine whether the answer is fully supported by
the provided context.

Context:
{context}

Answer:
{answer}

Rules:

1. Every factual claim in the answer must be supported
   by the context.
2. The answer must not introduce unsupported facts.
3. If the answer is supported by the context, return PASS.
4. If the answer contains unsupported or contradictory
   information, return FAIL.

Return ONLY:

PASS

or

FAIL
"""

    result = llm.generate(prompt)

    return result.strip().upper() == "PASS"


# ============================================================
# 3. Answer Relevance
# ============================================================

def evaluate_answer_relevance(
    question: str,
    answer: str
) -> bool:

    prompt = f"""
You are evaluating the answer relevance of a RAG system.

Determine whether the answer directly addresses
the user's question.

Question:
{question}

Answer:
{answer}

Rules:

1. The answer should directly address the question.
2. The answer should not focus on unrelated information.
3. If the answer directly addresses the question, return PASS.
4. If the answer is unrelated or does not answer the question,
   return FAIL.

Return ONLY:

PASS

or

FAIL
"""

    result = llm.generate(prompt)

    return result.strip().upper() == "PASS"


# ============================================================
# 4. Answer Correctness
# ============================================================

def evaluate_answer_correctness(
    question: str,
    expected_answer: str,
    actual_answer: str
) -> bool:

    prompt = f"""
You are evaluating the correctness of an answer generated
by a RAG system.

Determine whether the actual answer correctly answers
the question compared with the expected answer.

Question:
{question}

Expected Answer:
{expected_answer}

Actual Answer:
{actual_answer}

Rules:

1. The actual answer does not need to use the exact wording
   of the expected answer.
2. Different wording is acceptable if the meaning is equivalent.
3. The important facts must be correct.
4. If the actual answer is factually equivalent to the
   expected answer, return PASS.
5. If the actual answer gives incorrect, contradictory,
   or materially different information, return FAIL.

Return ONLY:

PASS

or

FAIL
"""

    result = llm.generate(prompt)

    return result.strip().upper() == "PASS"


# ============================================================
# 5. Evaluate All RAG Metrics
# ============================================================

def evaluate_rag(
    question: str,
    context: str,
    expected_answer: str,
    actual_answer: str
) -> dict:

    context_relevance = evaluate_context_relevance(
        question=question,
        context=context
    )

    faithfulness = evaluate_faithfulness(
        context=context,
        answer=actual_answer
    )

    answer_relevance = evaluate_answer_relevance(
        question=question,
        answer=actual_answer
    )

    answer_correctness = evaluate_answer_correctness(
        question=question,
        expected_answer=expected_answer,
        actual_answer=actual_answer
    )

    passed_metrics = sum([
        context_relevance,
        faithfulness,
        answer_relevance,
        answer_correctness
    ])

    total_metrics = 4

    score = passed_metrics / total_metrics

    return {
        "context_relevance": context_relevance,
        "faithfulness": faithfulness,
        "answer_relevance": answer_relevance,
        "answer_correctness": answer_correctness,
        "passed_metrics": passed_metrics,
        "total_metrics": total_metrics,
        "score": score
    }