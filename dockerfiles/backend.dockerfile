FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

COPY backend ./backend
COPY monitoring ./montoring

RUN pip install uv
RUN uv sync --frozen

EXPOSE 8000

CMD ["sh", "-c", " uv run python -m monitoring.register_prompts && uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"]
