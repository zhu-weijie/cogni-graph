import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from neo4j import Session as Neo4jSession

from src.core.services import graph_service
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


def search_documents(query: str, tenant_id: str) -> list[Document]:
    results = vector_store.similarity_search(
        query=query, filter={"tenant_id": tenant_id}
    )
    return results


def process_document(
    file_path: str, tenant_id: str, doc_id: str, neo4j_session: Neo4jSession
):
    text = extract_text_from_pdf(file_path)

    num_chunks = chunk_and_store_text(text=text, tenant_id=tenant_id, doc_id=doc_id)

    num_nodes, num_rels = graph_service.extract_and_store_graph(
        neo4j_session=neo4j_session,
        text=text[:10000],
        tenant_id=tenant_id,
        doc_id=doc_id,
    )

    return num_chunks, num_nodes, num_rels
