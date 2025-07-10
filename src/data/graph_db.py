from neo4j import GraphDatabase

from src.config import settings


class GraphDB:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_session(self):
        return self._driver.session()


graph_db_instance = GraphDB(
    uri=settings.NEO4J_URI,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)
