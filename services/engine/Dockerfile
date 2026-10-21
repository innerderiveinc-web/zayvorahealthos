# Multi-stage Docker build for ZMIE Engine
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies manifest from services/engine
COPY services/engine/pyproject.toml .

# Install python dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pydantic \
    pydantic-settings \
    httpx \
    asyncpg \
    neo4j \
    redis \
    sqlalchemy \
    greenlet \
    minio \
    pgvector

# Runner image
FROM python:3.11-slim as runner

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Copy engine application source code and essential runtime assets
COPY services/engine/app ./app
COPY catalog_seed.json ./catalog_seed.json
COPY workbench.html ./workbench.html
COPY index.html ./index.html
COPY sw.js ./sw.js

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
