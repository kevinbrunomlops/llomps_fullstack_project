FROM python:3.12-slim

  WORKDIR /app

  COPY pyproject.toml uv.lock ./
  
  COPY frontend ./frontend
  COPY backend ./backend

  RUN pip install uv  
  RUN uv sync --frozen

  EXPOSE 8501

  CMD ["uv", "run", "streamlit", "run", "frontend/src/app.py", "--server.address=0.0.0.0", "--server.port=8501"]