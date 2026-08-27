from app.rag.document_loader import load_pdf
from app.rag.text_cleaner import clean_text
from app.rag.text_chunker import chunk_text


documents = load_pdf("data/documents/company_policy.pdf")

all_chunks = []

for document in documents:

    cleaned_text = clean_text(document["text"])

    chunks = chunk_text(
        cleaned_text,
        document["metadata"]
    )

    all_chunks.extend(chunks)


print("Total chunks:", len(all_chunks))

for chunk in all_chunks[:5]:

    print("=" * 50)

    print("Metadata:")
    print(chunk["metadata"])

    print("\nText:")
    print(chunk["text"][:300])