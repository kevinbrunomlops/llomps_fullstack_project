FROM python:3.12

WORKDIR /app

COPY pyproject.toml uv.lock ./

COPY backend ./backend
COPY montoring ./montoring

RUN pip install uv
RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
