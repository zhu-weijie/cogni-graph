from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import ChatOpenAI

from src.config import settings

llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model="gpt-4o")

rag_prompt = ChatPromptTemplate.from_template(
    """Answer the following question based only on the provided context.
If you don't know the answer, just say that you don't know. Don't try
to make up an answer.

<context>
{context}
</context>

Question: {input}"""
)
rag_qa_chain = create_stuff_documents_chain(llm, rag_prompt)


def generate_answer(query: str, context: list[Document]) -> str:
    response = rag_qa_chain.invoke({"input": query, "context": context})
    return response


graph = Neo4jGraph(
    url=settings.NEO4J_URI,
    username=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)

graph_qa_chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    verbose=True,
    allow_dangerous_requests=True,
)


def generate_graph_answer(query: str) -> str:
    response = graph_qa_chain.invoke({"query": query})
    return response["result"]
