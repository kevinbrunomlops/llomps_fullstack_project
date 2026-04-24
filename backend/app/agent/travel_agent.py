from dotenv import load_dotenv

from pydantic_ai import Agent

from app.core.constants import MODEL_MEDIUM
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.recommendations import RecommendationRequest


load_dotenv()

travel_agent = Agent(
    model=MODEL_MEDIUM,
    system_prompt=""
)

@travel_agent.tool_plain
def lookup_seed_places(
    city: str,
    environment: str,
    travel_styles: str, 
    tags: str,
    category: str = "attraction",
    budget_level: str | None = None,
    family_friendly: bool | None = None
) -> str:
    """ Tool description should be registred in MLflow prompt registry."""
    places = filter_places(
        city=city,
        category=category,
        budget_level=budget_level,
        family_friendly=family_friendly,
        environment=environment,
        travel_styles=travel_styles,
        tags=tags
    )
    return format_places_for_prompt(places[:10])