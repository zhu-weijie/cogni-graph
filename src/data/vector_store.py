from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from src.config import settings

connection_string = settings.DATABASE_URL
collection_name = "documents"
embeddings_function = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

vector_store = PGVector(
    connection=connection_string,
    embeddings=embeddings_function,
    collection_name=collection_name,
)
