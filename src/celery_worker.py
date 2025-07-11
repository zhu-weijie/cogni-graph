from celery import Celery

from src.config import settings
from src.core.services import document_service
from src.data.graph_db import graph_db_instance

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
)

celery_app.conf.update(
    task_track_started=True,
)


@celery_app.task
def add(x, y):
    return x + y


@celery_app.task(bind=True)
def process_document_task(self, file_path: str, tenant_id: str, doc_id: str):
    self.update_state(state="PROGRESS", meta={"status": "Extracting text..."})

    neo4j_session = graph_db_instance.get_session()

    try:
        num_chunks, num_nodes, num_rels = document_service.process_document(
            file_path=file_path,
            tenant_id=tenant_id,
            doc_id=doc_id,
            neo4j_session=neo4j_session,
        )
        return {
            "status": "Complete",
            "rag_chunks_stored": num_chunks,
            "kg_nodes_created": num_nodes,
            "kg_relationships_created": num_rels,
        }
    finally:
        neo4j_session.close()
