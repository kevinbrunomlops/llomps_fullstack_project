from __future__ import annotations

from typing import Any

import httpx

from app.core.config import get_settings
from app.schemas.place import place

PLACES_TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

class GoogleMapsService:
    def __init__(self) -> None:
        self.settings = get_settings()
    
    @property
def enabled(self) -> bool:
    return self.settings.use_google_maps and bool(self.settings.google_maps_api_key)

async def text_search(self, *, text_query: str, category: str, city: str) -> list[Place]:
    if not self.enabled:
        return []
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": self.settings.google_maps_api_key,
        # Keep fields small to reduce cost.
        "X-Goog-FieldMask": (
            "places.displayName,places.formattedAddress,places.rating"
            "places.priceLevel,places.primaryType,places.regularOpeningHours"
        ),
    }
    payload: dict[str, Any] = {
        "textQuery": text_query,
        "pageSize": self.settings.google_maps_max_results,
    }

    async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
        response = await client.post(PLACES_TEXT_SEARCH_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    places: list[Place] = []
    for item in data.get("places", []):
        display_name = item.get("displayName",{}).get("text", "Unknown place")
        opening_hours = item.get("regularOpeningHours", {}).get("weekdayDescriptions", [])
        primary_type = item.get("primaryType")

        places.append(
            Place(
                id=None,
                name=display_name,
                city=city,
                country=None,
                category=category,
                subcategories=[primary_type] if primary_type else [],
                description=f"Live Google Maps result for {category} in {city}.",
                budget_level=None,
                family_friendly=None,
                environment=None,
                travel_styles=[],
                recommended_duration_hours=None,
                best_seasons=[],
                area=None,
                tags=[primary_type] if primary_type else [],
                priority_score=1,
                source_type="google_maps",
                address=item.get("formattedAddress"),
                rating=item.get("rating"),
                price_level=item.get("priceLevel"),
                opening_hours=opening_hours,
            )
        )
        return places

google_maps_service = GoogleMapsService()