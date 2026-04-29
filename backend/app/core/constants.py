from pathlib import Path

import mlflow

from app.core.config import get_settings

MODEL_SMALL = "openrouter:liquid/lfm-2.5-1.2b-instruct:free"
MODEL_MEDIUM = "openrouter:nvidia/nemotron-3-nano-30b-a3b:free"
MODEL_LARGE = "openrouter:nvidia/nemotron-3-super-120b-a12b:free"

LLM_JUDGE = "openrouter:nvidia/nemotron-3-nano-30b-a3b:free"

settings = get_settings()
MONITORING_PATH = settings.monitoring_path

Path(MONITORING_PATH).mkdir(parents=True, exist_ok=True)

mlflow.set_tracking_uri(settings.tracking_uri)
mlflow.set_experiment(settings.mlflow_experiment_name)
mlflow.pydantic_ai.autolog()