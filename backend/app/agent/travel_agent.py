
""" 
Pydantic-AI travel agent.

Uses curated manual data from backend/data/scandinavia_data.json first,
then optional Google Maps enrichment through the recommendation service. 
"""

from __future__ import annotations

from dotenv import load_dotenv
from mlflow.genai.prompts import load_prompt
from pydantic_ai import Agent

from app.core.constants import MODEL_MEDIUM
from app.core.mlflow_utils import add_request_tags
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.recommendations import RecommendationRequest
from app.services.content_service import filter_places, format_places_for_prompt
from app.services.planner_service import build_day_plan
from app.services.recommendation_service import build_recommendations


load_dotenv()

travel_agent = Agent(
    model=MODEL_MEDIUM,
    system_prompt=load_prompt("travel_chatbot_system_prompt").format(),
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
    prompt =f"""
User_request: {request.message}
Structured travel context:
- city: {recommendation_request.city}
- days: {recommendation_request.days}
- budget: {recommendation_request.budget}
- interests: {recommendation_request.interests}
- travel_group: {recommendation_request.travel_group}
- family_friendly: {recommendation_request.family_friendly}
- environment: {recommendation_request.environment}
- use_google_maps: {recommendation_request.use_google_maps}

Candidate attractions:
{format_places_for_prompt(recommendations.attractions)}

Candidate restaurants:
{format_places_for_prompt(recommendations.restaurants)}

Candidate activitites:
{format_places_for_prompt(recommendations.activities)}

Simple draft day plan:
{day_plan}

Instructions:
- Answer in Swedish.
- Use only the candidate places above unless you clearly say that you are giving a general suggestion. 
- Keep the tone helpful and practical.
- Use headings for Sevärdheter, Restauranger, Aktiviteter and Enkel dagsplan. 
- Respect budget, travel group, family-friendly and environent filters when they are provided.
- Mention whether the recommendations come from the manual dataset or Google Maps if relevant. 
- End with 2 short follow-up questions.
"""
    
    add_request_tags(
        endpoint="/chat",
        city=recommendation_request.city,
        prompt_name="travel_chatbot_system_prompt",
        prompt_version=request.prompt_version,
    )
    result = await travel_agent.run(prompt)

    all_places = [
        *recommendations.attractions,
        *recommendations.restaurants,
        *recommendations.activitites,
    ]
    sources = sorted({place.source_type for place in all_places})

    return ChatResponse(
        answer=result.output,
        city=recommendation_request.city,
        prompt_name="travel_chatbot_system_prompt",
        prompt_version=request.prompt_version, 
        attractions=[place.model_dumpt() for place in recommendations.attractions],
        restaurants=[place.model_dumpt() for place in recommendations.restaurants],
        activities=[place.model_dumpt() for place in recommendations.activities],
        follow_up_questions=[
            "Vill du att jag gör ett billigare upplägg?",
            "Vill du att jag fokuserar mer på mat, kultur eller natur?"
        ],
        sources=sources,
    )