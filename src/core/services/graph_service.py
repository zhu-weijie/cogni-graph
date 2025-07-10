from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from neo4j import Session as Neo4jSession

llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
llm_transformer = LLMGraphTransformer(llm=llm)


def extract_and_store_graph(
    neo4j_session: Neo4jSession, text: str, tenant_id: str, doc_id: str
):
    doc = Document(page_content=text)

    graph_documents = llm_transformer.convert_to_graph_documents([doc])

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    for node in nodes:
        neo4j_session.run(
            "MERGE (n:`%s` {id: $id}) SET n.tenant_id = $tenant_id, n.doc_id = $doc_id"
            % node.type,
            id=node.id,
            tenant_id=tenant_id,
            doc_id=doc_id,
        )

    for rel in relationships:
        neo4j_session.run(
            """
            MATCH (a {id: $start_id})
            MATCH (b {id: $end_id})
            MERGE (a)-[r:%s]->(b)
            """
            % rel.type,
            start_id=rel.source.id,
            end_id=rel.target.id,
        )

    return len(nodes), len(relationships)
