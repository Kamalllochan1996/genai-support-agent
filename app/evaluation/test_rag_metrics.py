from app.evaluation.rag_metrics import evaluate_rag


# ============================================================
# Test Data
# ============================================================

question = "How many casual leaves can I take?"

context = """
Employees are entitled to 12 days of casual leave every year.
"""

answer = """
Employees are entitled to 12 days of casual leave every year.
"""


# ============================================================
# Run Evaluation
# ============================================================

result = evaluate_rag(
    question=question,
    context=context,
    answer=answer
)


# ============================================================
# Print Input
# ============================================================

print("\n" + "=" * 60)

print("\nQuestion:")
print(question)

print("\nContext:")
print(context)

print("\nAnswer:")
print(answer)


# ============================================================
# Print Individual Metrics
# ============================================================

print("\n" + "-" * 60)

print("Context Relevance:")
print(
    "PASS"
    if result["context_relevance"]
    else "FAIL"
)

print("\nFaithfulness:")
print(
    "PASS"
    if result["faithfulness"]
    else "FAIL"
)

print("\nAnswer Relevance:")
print(
    "PASS"
    if result["answer_relevance"]
    else "FAIL"
)


# ============================================================
# Print Overall Score
# ============================================================

print("\n" + "-" * 60)

print(
    f"Metrics Passed: "
    f"{result['passed_metrics']}/"
    f"{result['total_metrics']}"
)

print(
    f"Overall Score: "
    f"{result['score'] * 100:.2f}%"
)

print("\n" + "=" * 60)