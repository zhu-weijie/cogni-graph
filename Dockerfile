# ---- Stage 1: Production Base ----
FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home appuser
RUN mkdir -p /home/appuser/app/uploads && chown -R appuser:appuser /home/appuser/app
USER appuser

WORKDIR /home/appuser/app

COPY ./src ./src

COPY alembic.ini .
COPY alembic ./alembic

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ---- Stage 2: Test Stage ----
FROM base AS test

ENV PATH=/home/appuser/.local/bin:$PATH

WORKDIR /home/appuser/app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

CMD ["pytest"]