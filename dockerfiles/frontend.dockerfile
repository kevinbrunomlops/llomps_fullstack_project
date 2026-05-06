FROM python:3.12

  WORKDIR /app

  COPY pyproject.toml uv.lock ./
  
  COPY frontend ./frontend

  RUN pip install uv  
  RUN uv sync --frozen

  EXPOSE 8501

  CMD ["uv", "run", "streamlit", "run", "frontend/src/main.py", "--server.address=0.0.0.0", "--server.port=8501"]