
""" 
Pydantic-AI travel agent.

Uses curated manual data from backend/data/scandinavia_data.json first,
then optional Google Maps enrichment through the recommendation service. 
"""

from __future__ import annotations

from dotenv import load_dotenv
from mlflow.genai.prompts import load_prompt
from pydantic_ai import Agent

from backend.app.core.constants import MODEL_MEDIUM, MODEL_LARGE
from backend.app.core.mlflow_utils import add_request_tags
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.schemas.recommendations import RecommendationRequest
from backend.app.services.content_service import filter_places, format_places_for_prompt
from backend.app.services.planner_service import build_day_plan
from backend.app.services.recommendation_service import build_recommendations
from backend.app.utils.localization import to_swedish_city, to_swedish_budget


load_dotenv()

travel_agent = Agent(
    model=MODEL_MEDIUM,
    system_prompt=load_prompt("travel_chatbot_system_prompt").template
)

@travel_agent.tool_plain
def lookup_dataset_places(
    city: str,
    category: str = "attraction",
    budget_level: str | None = None,
    family_friendly: bool | None = None,
    environment: str | None = None,
    travel_style: str | None = None, 
    tag: str | None = None, 
) -> str:
    """Look up curated places from the manual Scandinavia travel dataset."""

    interests: list[str] = []
    if tag:
        interests.append(tag)

    places = filter_places(
        city=city,
        category=category,
        interests=interests,
        budget=budget_level,
        family_friendly=family_friendly,
        environment=environment,
        travel_group=travel_style,
        
    )
    return format_places_for_prompt(places[:10])

async def run_travel_agent(request: ChatRequest) -> ChatResponse:
    recommendation_request = RecommendationRequest(
        city=request.city or "Stockholm",
        days=request.days or 1,
        budget=request.budget,
        interests=request.interests,
        travel_group=request.travel_group,
        family_friendly=request.family_friendly,
        environment=request.environment,
        indoors=request.indoors,
        use_google_maps=request.use_google_maps,
    )

    recommendations = await build_recommendations(recommendation_request)
    day_plan = build_day_plan(
        city=recommendation_request.city,
        days=recommendation_request.days or 1,
        recommendations=recommendations,
    )

    swedish_city = to_swedish_city(recommendation_request.city)
    swedish_budget = to_swedish_budget(recommendation_request.budget)
    
    prompt = f"""
Användarens fråga:
{request.message}

Strukturerad reseinformation:
- stad: {swedish_city}
- antal dagar: {recommendation_request.days}
- budgetnivå: {swedish_budget}
- intressen: {recommendation_request.interests}
- resesällskap: {recommendation_request.travel_group}
- familjevänligt: {recommendation_request.family_friendly}
- miljö: {recommendation_request.environment}
- google maps aktiverat: {recommendation_request.use_google_maps}

Möjliga sevärdheter:
{format_places_for_prompt(recommendations.attractions)}

Möjliga restauranger:
{format_places_for_prompt(recommendations.restaurants)}

Möjliga aktiviteter:
{format_places_for_prompt(recommendations.activities)}

Enkel preliminär dagsplan:
{day_plan}

Instruktioner:
- Svara alltid på naturlig svenska.
- Använd svenska namn på städer och områden när det finns.
- Om datasetet innehåller engelska beskrivningar ska du översätta och skriva om dem till naturlig svenska.
- Skriv aldrig "Day 1", skriv alltid "Dag 1".
- Alla rubriker ska vara på svenska.
- Skriv som en personlig, hjälpsam och konkret svensk reseguide.
- Anpassa rekommendationerna efter budget, antal dagar, resesällskap, intressen och miljö.
- Prioritera platser från listorna ovan.
- Hitta inte på öppettider, priser, betyg eller exakta adresser om de inte finns i datan.
- Om det saknas tillräcklig information, säg det tydligt och ge ett försiktigt generellt tips.
- Nämn inte tekniska ord som JSON, RAG, embedding eller dataset för användaren.
- Avsluta alltid med två korta följdfrågor på svenska.
"""
    
    add_request_tags(
        endpoint="/chat",
        city=recommendation_request.city,
        prompt_name="travel_chatbot_system_prompt",
        prompt_version=request.prompt_version,
    )
    print("Before travel_agent.run", flush=True)
    result = await travel_agent.run(prompt)
    print("After travel_agent.run", flush=True)

    all_places = [
        *recommendations.attractions,
        *recommendations.restaurants,
        *recommendations.activities,
    ]
    sources = sorted({place.source_type for place in all_places})

    return ChatResponse(
        answer=result.output,
        city=recommendation_request.city,
        prompt_name="travel_chatbot_system_prompt",
        prompt_version=request.prompt_version or "latest", 
        attractions=[place.model_dump() for place in recommendations.attractions],
        restaurants=[place.model_dump() for place in recommendations.restaurants],
        activities=[place.model_dump() for place in recommendations.activities],
        follow_up_questions=[
            {"question": "Vill du att jag gör ett billigare upplägg?"},
            {"question": "Vill du att jag fokuserar mer på mat, kultur eller natur?"},
        ],
        sources=sources,
    )