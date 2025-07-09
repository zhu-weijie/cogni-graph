from fastapi import FastAPI

app = FastAPI(title="CogniGraph")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
