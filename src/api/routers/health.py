from fastapi import APIRouter, Depends
from neo4j import Session as Neo4jSession
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_graph_session
from src.celery_worker import add

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check(
    db: Session = Depends(get_db),
    graph_db: Neo4jSession = Depends(get_graph_session),
):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    try:
        graph_db.run("RETURN 1")
        graph_db_status = "ok"
    except Exception:
        graph_db_status = "error"

    try:
        task = add.delay(2, 2)
        celery_status = "ok"
        task_id = task.id
    except Exception as e:
        celery_status = "error"
        task_id = str(e)

    return {
        "status": "ok",
        "database_status": db_status,
        "graph_database_status": graph_db_status,
        "celery_status": celery_status,
        "test_task_id": task_id,
    }
