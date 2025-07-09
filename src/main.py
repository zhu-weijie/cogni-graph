from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.data.database import SessionLocal

app = FastAPI(title="CogniGraph")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database_status": "ok"}
    except Exception as e:
        return {"status": "ok", "database_status": "error", "detail": str(e)}
