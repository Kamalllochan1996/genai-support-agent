from langchain_core.documents import Document


document = Document(
    page_content=(
        "Employees are entitled to "
        "12 days of casual leave every year."
    ),
    metadata={
        "source": "company_policy.pdf",
        "page": 2
    }
)


print("Content:")
print(document.page_content)

print("\nMetadata:")
print(document.metadata)