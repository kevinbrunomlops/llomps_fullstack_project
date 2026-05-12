print("A: start imports", flush=True)

import asyncio
import json
from pathlib import Path

print("B: basic imports done", flush=True)

import mlflow
from mlflow.genai import evaluate
from mlflow.genai.datasets import create_dataset
from mlflow.genai.scorers import Guidelines

print("C: mlflow imports done", flush=True)

from backend.app.core.mlflow_utils import set_experiment
from backend.app.schemas.chat import ChatRequest
from backend.app.core.constants import LLM_JUDGE

print("D: backend core imports done", flush=True)

from backend.app.agent.travel_agent import run_travel_agent

print("E: travel agent import done", flush=True)

EXPERIMENT_NAME = "travel_chatbot_evaluation"
DATASET_NAME = "travel_chatbot_eval_v1"
EVAL_DATA_PATH = Path("backend/data/nordic_travel_dataset_complete.json")

async def predict(question: str) -> str:
    print("Calling travel agent...", flush=True)
    response = await run_travel_agent(ChatRequest(message=question))
    print("Travel agent returned.", flush=True)
    return response.answer

def sync_predict(question: str) -> str:
    mlflow.autolog(disable=True)
    print(f"Evaluating question: {question[:120]}...", flush=True)
    return asyncio.run(asyncio.wait_for(predict(question), timeout=120))

def load_eval_data(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Evaluation data file was not found at '{path}'.")

    with path.open(encoding="utf-8") as file:
        raw_data = json.load(file)

    places = raw_data.get("places_flat", [])

    records = []

    for place in places:
        city = place.get("city")
        country = place.get("country")
        name = place.get("name")
        category = place.get("category")
        budget = place.get("budget_level")
        family = place.get("family_friendly")
        styles = ", ".join(place.get("travel_styles", []))

        question = (
            f"I am visiting {city}, {country}. "
            f"Would you recommend {name} for a traveler interested in {category}? "
            f"My budget level is {budget}. "
            f"Travel style: {styles}. "
            f"Family friendly required: {family}. "
            f"Please explain why and give practical travel advice."
        )

        records.append({
            "inputs": {
                "question": question
            },
            "expectations": {
                "place_name": name,
                "city": city,
                "country": country,
                "category": category,
                "budget_level": budget,
                "family_friendly": family
            }
        })

    return records[:1]

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