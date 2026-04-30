"""
Recomendation service.
Primary source: backend/data/scandinavia_data.json.
Optional source: Google maps Places API when use_google_maps=True.
"""

from __future__ import annotations

from app.schemas.place import Place
from app.schemas.recommendations import RecommendationRequest, RecommendationResponse
from app.services.content_service import filter_places, get_supported_cities
from app.services.google_maps_service import google_maps_service


def _merge_unique(seed_places: list[Place], live_places: list[Place]) -> list[Place]:
    seen: set[tuple[str, str]] = set()
    combined: list[Place] = []

    for place in [*seed_places, *live_places]:
        key = (place.name.lower(), place.city.lower())
        if key in seen:
            continue
        seen.add(key)
        combined.append(place)

    return combined


async def _category_places(
    request: RecommendationRequest, category: str
) -> list[Place]:
    seed_places = filter_places(
        city=request.city,
        category=category,
        interests=request.interests,
        budget=request.budget,
        family_friendly=request.family_friendly,
        environment=request.environment,
        indoors=request.indoors,
        travel_group=request.travel_group,
    )

    live_place: list[Place] = []
    if request.use_google_maps:
        interest_text = " ".join(request.interests) if request.interests else category
        text_query = f"{interest_text} {category} in {request.city}"
        live_place = await google_maps_service.text_search(
            text_query=text_query,
            category=category,
            city=request.city,
        )
    return _merge_unique(seed_places, live_place=live_place)[:5]


async def build_recommendations(
    request: RecommendationRequest,
) -> RecommendationResponse:
    attractions = await _category_places(request, "attraction")
    restaurants = await _category_places(request, "restaurant")
    activities = await _category_places(request, "activity")

    notes: list[str] = []
    supported_cities = get_supported_cities()

    if request.city not in supported_cities:
        notes.append(
            f"City '{request.city}' is not in the manual dataset. "
            f"Supported cities: {', '.join(supported_cities)}."
        )

    if not attractions and not restaurants and not activities:
        notes.append("No matces found. Try another city or fewer filters. ")

    if request.use_google_maps and not google_maps_service.enabled:
        notes.append(
            "Google Maps API key missing or disabled. Returned manual JSON data only."
        )

    return RecommendationResponse(
        city=request.city,
        attractions=attractions,
        restaurants=restaurants,
        activities=activities,
        notes=notes,
    )
