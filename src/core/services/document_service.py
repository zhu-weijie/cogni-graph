import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.data.vector_store import vector_store


def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")
        return ""


def chunk_and_store_text(text: str, tenant_id: str, doc_id: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)

    vector_store.add_texts(
        texts=chunks,
        metadatas=[{"tenant_id": tenant_id, "doc_id": doc_id} for _ in chunks],
    )
    return len(chunks)
