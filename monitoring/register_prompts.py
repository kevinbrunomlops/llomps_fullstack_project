from textwrap import dedent

from mlflow.genai.prompts import register_prompt

from backend.app.core.mlflow_utils import set_experiment


def register_travel_prompts() -> None:
    set_experiment()

    register_prompt(
        name="travel_chatbot_system_prompt",
        template=dedent(
            """ 
            Du är en skandinavisk reseassistent.
            Hjälp användaren att planera en resa med hjälp av det tillhandahållna resekontexten.
            Var praktisk, undvik att hitta på saknade detaljer och var transparent vid osäkerhet.
            Föredra kortfattade svar på svenska med tydliga sektioner.
            """
        ).strip(),
        tags={
            "author": "team",
            "agent": "travel-chatbot",
            "prompt_type": "system_prompt",
            
        },
    )

    register_prompt(
        name="travel_dataset_lookup_description",
        template=dedent(
            "Use this tool to inspect curated seed data for attractions, restaurants or activities "
            "for a Scandinavian city before answering."
        ).strip(),
        tags={
            "author": "team",
            "agent": "travel-chatbot",
            "prompt_type": "tool_description",
            "tool_name": "lookup_seed_places",
            
        },
    )

    register_prompt(
        name="travel_google_maps_lookup_description",
        template=dedent(
            "Use live Google Maps data carefully for real places. "
            "Prefer a small number of results and avoid claiming unavailable details."
        ).strip(),
        tags={
            "author": "team",
            "agent": "travel-chatbot",
            "prompt_type": "tool_description",
            "tool_name": "google_maps_search",
            
        },
    )

if __name__ == "__main__":
    register_travel_prompts()
    print("Travel prompts registered in MLFlow.") 

    
