# src/data/vector_store.py
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from src.config import settings

connection_string = settings.DATABASE_URL
collection_name = "documents"
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

vector_store = PGVector(
    connection_string=connection_string,
    embedding_function=embeddings,
    collection_name=collection_name,
)
