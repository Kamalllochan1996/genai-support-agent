from langchain_text_splitters import RecursiveCharacterTextSplitter


text = """
Employees are entitled to 12 days of casual leave every year.

Employees receive medical insurance benefits from the company.

Employees must reset their password every 90 days.

Employees may request planned leave through the company's
approved leave process.
"""


splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)


chunks = splitter.split_text(text)


for i, chunk in enumerate(chunks):

    print(f"\n--- Chunk {i} ---")
    print(chunk)