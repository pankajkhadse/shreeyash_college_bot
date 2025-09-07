from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
import glob

# List of CSV files (you can add/remove files here)
csv_files = [
    "general_info.csv",
    "departments.csv",
    "fees.csv",
    "facilities.csv",
    "events.csv",
    "faculties.csv"
]

# Initialize embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Path to store the vector DB
db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for file in csv_files:
        if os.path.exists(file):
            df = pd.read_csv(file)

            for i, row in df.iterrows():
                # Flexible: use whatever columns exist in the file
                text_content = " ".join(
                    [str(v) for v in row.values if pd.notna(v)]
                )

                document = Document(
                    page_content=text_content,
                    metadata={"source_file": file},
                    id=f"{file}_{i}"
                )
                ids.append(f"{file}_{i}")
                documents.append(document)

# Create / load Chroma vector store
vector_store = Chroma(
    collection_name="college_info",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Retriever for querying
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
