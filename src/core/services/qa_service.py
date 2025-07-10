from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import settings

llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model="gpt-4o")

prompt = ChatPromptTemplate.from_template(
    """Answer the following question based only on the provided context.
If you don't know the answer, just say that you don't know. Don't try
to make up an answer.

<context>
{context}
</context>

Question: {input}"""
)

qa_chain = create_stuff_documents_chain(llm, prompt)


def generate_answer(query: str, context: list[Document]) -> str:
    response = qa_chain.invoke({"input": query, "context": context})
    return response
