FROM python:3.13-slim

ENV PYTHONDONTWRITTEBYTECODE=1 \
    PYTHONUNBUFFERED=1

    WORKDIR /app

  RUN pip install --no-cache-dir uv  

  COPY frontend/ /app/frontend/

  WORKDIR /app/frontend

  RUN uv sync --no-dev

  EXPOSE 8501

  CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]