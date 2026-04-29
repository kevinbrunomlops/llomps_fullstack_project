from __future__ import annotations

from typing import Any

import mlflow

from app.core.config import get_settings

def set_experiment(name: str | None = None) -> None:
    settings = get_settings()
    mlflow.set_tracking_uri(settings.tracking_uri)
    mlflow.set_experiment(name or settings.mlflow_experiment_name)

def add_request_tags(**tags: Any) -> None:
    clean_tags = {key: str(value) for key, value in tags.items() if value is not None}
    if clean_tags:
        mlflow.set_tags(clean_tags)
