evaluation_dataset = [
    {
        "question": "How many casual leaves can an employee take?",
        "expected_answer": "Employees are entitled to 12 days of casual leave every year.",
        "expected_source": "company_policy.pdf"
    },
    {
        "question": "Do employees receive medical insurance?",
        "expected_answer": "Employees receive medical insurance benefits from the company.",
        "expected_source": "company_policy.pdf"
    },
    {
        "question": "How often must employees reset their password?",
        "expected_answer": "Employees must reset their password every 90 days.",
        "expected_source": "company_policy.pdf"
    },
    {
        "question": "What is the company's policy on moon travel?",
        "expected_answer": "I don't have enough information in the provided documents to answer this question.",
        "expected_source": None
    }
]


if __name__ == "__main__":

    print("Evaluation Dataset")
    print("=" * 60)

    for item in evaluation_dataset:

        print("\nQuestion:")
        print(item["question"])

        print("\nExpected Answer:")
        print(item["expected_answer"])

        print("\nExpected Source:")
        print(item["expected_source"])

        print("-" * 60)