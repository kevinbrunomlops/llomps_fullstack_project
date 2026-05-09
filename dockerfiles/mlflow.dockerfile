FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend ./backend
COPY monitoring ./monitoring

RUN pip install uv
RUN uv sync --frozen

CMD ["sh", "-c", "uv run mlflow server --backend-store-uri \"$MLFLOW_DATABASE_URL\" --host 0.0.0.0 --port 5001 --allowed-hosts travel-chatbot-mlflow.calmsky-b2c3c199.francecentral.azurecontainerapps.io,localhost,127.0.0.1 --cors-allowed-origins '*'"]