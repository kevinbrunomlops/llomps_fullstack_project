from pathlib import Path

import mlflow

from backend.app.core.config import get_settings

settings = get_settings()

MODEL_SMALL = settings.model_small
MODEL_MEDIUM = settings.model_medium
MODEL_LARGE = settings.model_large
LLM_JUDGE = settings.llm_judge

MONITORING_PATH = settings.monitoring_path

Path(MONITORING_PATH).mkdir(parents=True, exist_ok=True)

mlflow.set_tracking_uri(settings.tracking_uri)
mlflow.set_experiment(settings.mlflow_experiment_name)
if settings.app_env != "evaluation":
    mlflow.pydantic_ai.autolog()