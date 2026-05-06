FROM python:3.13-slim

ENV PYTHONDONTWRITTEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend/ /app/backend/

WORKDIR /app/backend

RUN uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "8000"]
