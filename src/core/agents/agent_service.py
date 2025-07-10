from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from src.config import settings
from src.core.services import document_service, qa_service


@tool
def vector_search(query: str, tenant_id: str) -> str:
    """
    Use this tool for general questions about the content of the document.
    It is good for answering questions about concepts, summaries, or finding
    general information. Input should be the user's original question.
    """
    retrieved_chunks = document_service.search_documents(
        query=query, tenant_id=tenant_id
    )
    answer = qa_service.generate_answer(query=query, context=retrieved_chunks)
    return answer


@tool
def graph_search(query: str, tenant_id: str) -> str:
    """
    Use this tool for specific questions about entities and their relationships.
    It is good for questions like 'Who is X?', 'What is the email of Y?',
    or 'What is the relationship between A and B?'.
    Input should be the user's original question.
    """
    retrieved_chunks = document_service.search_documents(
        query=query, tenant_id=tenant_id
    )
    context_str = "\n".join([chunk.page_content for chunk in retrieved_chunks])
    augmented_query = f"Context: {context_str}\n\nQuestion: {query}"
    answer = qa_service.generate_graph_answer(query=augmented_query)
    return answer


tools = [vector_search, graph_search]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a helpful assistant. You have access to two tools: "
                "a vector search tool for general questions and a graph search "
                "tool for specific, factual questions about entities and relationships."
            ),
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model="gpt-4o", temperature=0)

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def run_agent(query: str, tenant_id: str) -> str:
    response = agent_executor.invoke({"input": query, "tenant_id": tenant_id})
    return response["output"]
