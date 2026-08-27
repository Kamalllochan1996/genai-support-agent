from app.evaluation.semantic_evaluator import evaluate_semantically


question = "How many casual leaves can an employee take?"

expected_answer = (
    "Employees are entitled to 12 days of casual leave every year."
)

actual_answer = (
    "An employee can take 12 casual leave days each year."
)


result = evaluate_semantically(
    question,
    expected_answer,
    actual_answer
)


print("\nQuestion:")
print(question)

print("\nExpected:")
print(expected_answer)

print("\nActual:")
print(actual_answer)

print("\nSemantic Evaluation:")
print("PASS" if result else "FAIL")