from __future__ import annotations

import asyncio
import json
from pathlib import Path

import mlflow
from mlflow.genai import evaluate
from mlflow.genai.datasets import create_dataset
from mlflow.genai.scorers import Guidelines

from app.agents.travel_agent import run_travel_agent
from app.core.constants import LLM_JUDGE
from app.core.mlflow_utils import set_experiment
from app.schemas.chat import ChatRequest

EXPERIMENT_NAME = "travel_chatbot_evaluation"
DATASET_NAME = "travel_chatbot_eval_v1"
EVAL_DATA_PATH = Path("data/eval_data.json")

async def predict(question: str) -> str:
    response = await run_travel_agent(ChatRequest(message=question))
    return response.answer

def sync_predict(inputs: dict) -> str:
    question = inputs["question"]
    return asyncio.run(predict(question))

def load_eval_data(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Evaluation data file was not found at '{path}'. "
            "Expected location: backend/data/eval_data.json"
        )
    
    with path-open(encoding="utf-8") as file:
        return json.load(file)

def main() -> None:
    set_experiment(EXPERIMENT_NAME)

    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        raise RuntimeError(f"MLFlow experiment '{EXPERIMENT_NAME}' was not found.")
    
    eval_data = load_eval_data(EVAL_DATA_PATH)
    
    evaluation_dataset = create_dataset(
        name=DATASET_NAME,
        experiment_id=experiment.experiment_id,
        tags={"stage": "validation", 
              "domain": "travel",
              "source_file": str(EVAL_DATA_PATH),
              },
    )
    # This merges the records into the named MLFlow dataset.
    # Keep DATASET_NAME stable when you wanto comparable evalutation runs
    # Change DATASET_NAME when you intentoinally create a new evaluation dataset.
    evaluation_dataset.merge_records(eval_data)

    scorers = [
        Guidelines(
            name="travel_response_quality",
            guidelines=(
                "The answer should be relevant to the user's city and preferences, "
                "organized clearly, cautious about uncertainty, and practical for trip planning."
            ),
            model=LLM_JUDGE,
        ),
    ]

    results = evaluate(
        data=evaluation_dataset,
        predict_fn=sync_predict,
        scorers=scorers,
    )
    
    print(results)

if __name__ == "__main__":
    main() 