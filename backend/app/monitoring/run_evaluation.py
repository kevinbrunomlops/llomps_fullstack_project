from __future__ import annotations

import asyncio
import json

import mlflow
from mlflow.genai import evaluate
from mlflow.genai.datasets import create_dataset
from mlflow.genai.scorers import Guidelines

from app.agents.travel_agent import run_travel_agent
from app.core.constants import LLM_JUDGE
from app.core.mlflow_utils import set_experiment
from app.schemas.chat import ChatRequest

async def predict(question: str) -> str:
    response = await run_travel_agent(ChatRequest(message=question))
    return response.answer

def sync_predict(inputs: dict) -> str:
    question = inputs["question"]
    return asyncio.run(predict(question))

def main() -> None:
    set_experiment("travel_chatbot_evaluation")
    experiment = mlflow.get_experiment_by_name("travel_chatbot_evaluation")

    with open("monitoring/eval_data.json", encoding="utf-8") as file:
        eval_data = json.load(file)
    
    evaluation_dataset = create_dataset(
        name="travel_chatbot_eval_v1",
        experiment_id=experiment.experiment_id,
        tags={"stage": "validation", "domain": "travel"},
    )
    evaluation_dataset.merge_records(eval_data)

    scorers = [
        Guidelines(
            name="travel_response_quality",
            guidelines=(
                "The answer should be relevant to the user's city and preferences, "
                "organized clearly, cautious about uncertainty, and practical for trip planning."
            ),
            model=LLM_JUDGE,
        )
    ]

    result = evaluate(
        data=evaluation_dataset,
        predict_fn=sync_predict,
        scorers=scorers,
    )
    print(result)

if __name__ == "__main__":
    main() 