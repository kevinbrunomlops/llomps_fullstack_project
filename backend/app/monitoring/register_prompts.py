from mlflow.genai.prompts import register_prompt

from app.core.mlflow_utils import set_experiment

def register_travel_prompts() -> None:
    set_experiment()

    register_prompt(
        name="travel_chatbot_system_prompt",
        template=(
            """ 
            You are a Scandinavian Travel assistant. 
            Help the user plan a trip using the provided travel context
            Be practical, avoid hallucinating missing details and be transparent about uncertainty.
            Prefer concise Swedish answers with clear sections.
            """
        ),
        tags={
            "author": "team",
            "agent": "travel-chatbot",
            "prompt_type": "system_prompt",
            "version": "v1",
        },
    )

    register_prompt(
        name="travel_dataset_lookup_description",
        template=(
            "Use this tool to inspect curated seed data for attractions, restaurants or activities "
            "for a Scandinavian city before answering."
        ),
        tags={
            "author": "team",
            "agent": "travel-chatbot",
            "prompt_type": "tool_description",
            "tool_name": "lookup_seed_places",
            "version": "v1",
        },
    )

    register_prompt
