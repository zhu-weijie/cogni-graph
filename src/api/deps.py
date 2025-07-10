from src.data.database import SessionLocal
from src.data.graph_db import graph_db_instance


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_graph_session():
    session = graph_db_instance.get_session()
    try:
        yield session
    finally:
        session.close()
