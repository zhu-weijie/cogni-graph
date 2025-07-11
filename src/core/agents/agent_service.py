from functools import partial

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

from src.config import settings
from src.core.services import document_service, qa_service


class SearchInput(BaseModel):
    query: str = Field(description="The user's original, full question.")


def vector_search(query: str, tenant_id: str) -> str:
    retrieved_chunks = document_service.search_documents(
        query=query, tenant_id=tenant_id
    )
    answer = qa_service.generate_answer(query=query, context=retrieved_chunks)
    return answer


def graph_search(query: str, tenant_id: str) -> str:
    retrieved_chunks = document_service.search_documents(
        query=query, tenant_id=tenant_id
    )
    context_str = "\n".join([chunk.page_content for chunk in retrieved_chunks])
    augmented_query = f"Context: {context_str}\n\nQuestion: {query}"
    answer = qa_service.generate_graph_answer(query=augmented_query)
    return answer


async def stream_agent(query: str, tenant_id: str):
    tools = [
        Tool(
            name="vector_search",
            func=partial(vector_search, tenant_id=tenant_id),
            description="Use this for general questions about concepts, summaries, "
            "or finding general information.",
            args_schema=SearchInput,
        ),
        Tool(
            name="graph_search",
            func=partial(graph_search, tenant_id=tenant_id),
            description="Use this for specific questions about entities "
            "(people, places, things) and their relationships.",
            args_schema=SearchInput,
        ),
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. You must use one of the provided tools "
                "to answer the user's question.",
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model="gpt-4o",
        temperature=0,
        streaming=True,
    )

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    async for event in agent_executor.astream_events({"input": query}, version="v1"):
        kind = event["event"]
        if kind == "on_chain_end" and event["name"] == "AgentExecutor":
            break
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield content
