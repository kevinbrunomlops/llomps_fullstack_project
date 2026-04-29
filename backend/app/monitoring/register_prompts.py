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
            
        },
    )

    register_prompt(
        name="travel_google_maps_lookup_description",
        template=(
            "Use live Google Maos data carefully for real places. "
            "Prefer a small number of results and avoid claiming unavailable details."
        ),
        tags={
            "author": "team",
            "agent": "travel-chatbot",
            "prompt_type": "tool_description",
            "tool_name": "google_maps_search",
            
        },
    )

if __name__ == "__main__":
    register_travel_prompts()
    print("Travel prompts registred in MLFlow.") 

    
