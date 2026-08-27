from app.rag.ingestion import ingest_pdf


file_path = "data/documents/company_policy.pdf"

count = ingest_pdf(file_path)

print(f"Successfully ingested {count} chunks")