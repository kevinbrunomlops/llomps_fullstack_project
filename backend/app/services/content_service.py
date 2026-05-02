"""
Loads and filters backend/data/scandinavia_data.json.
This is the primary source for MVP recommendations and MLFLOW evaluation.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app.core.config import get_settings
from app.schemas.place import Place


DATASET_FILENAME = "scandinavia_data.json"


@lru_cache
def load_dataset() -> dict[str, Any]:
    settings = get_settings()
    data_file = settings.data_path / DATASET_FILENAME

    if not data_file.exists():
        raise FileNotFoundError(
            f"Could not find {DATASET_FILENAME} in {settings.data_path}. " 
            "Place your generate JSON file in backend/data/."
        )
    
    with data_file.open(encoding="utf-8") as file:
        return json.load(file)
    

@lru_cache
def load_places() -> list[Place]:
    dataset = load_dataset()
    places: list[Place] = []

    for city_block in dataset.get("cities",[]):
        city = city_block.get("city")
        country = city_block.get("country")

        for raw_place in city_block.get("places",[]):
            places.append(
                Place(
                    **raw_place,
                    city=city,
                    country=country
                )
            )
    
    return places
    
    
@lru_cache
def get_supported_cities() -> list[str]:
    dataset = load_dataset()
    return dataset.get("supported_cities", [])


@lru_cache
def get_supported_categories() -> list[str]:
    dataset = load_dataset()
    return dataset.get("categories", [])


def _normalize(value:str | None) -> str:
    return (value or "").strip().lower()


def _matches_interests(place: Place, interests: list[str] | None) -> bool:
    if not interests:
        return True
    
    searchable_values = [
        place.name,
        place.category,
        place.description or "",
        place.area or "",
        *(place.subcategories or []),
        *(place.tags or []),
        *(place.travel_styles or []),
    ]     
    searchable_text = " ".join(searchable_values).lower()

    return any(_normalize(interest) in searchable_text for interest in interests)


def _score_place(
    place:Place,
    *,
    interests:list[str] | None = None,
    budget:str | None = None,
    family_friendly:bool | None = None,
    environment:str | None = None,
    travel_group:str | None = None,   
)-> int:
  score = place.priority_score or 0

  if interests and _matches_interests(place, interests):
      score += 30

  if budget and _normalize(place.budget_level) ==_normalize(budget):
      score += 20
 
  if environment:
      requested_environment =_normalize(environment)
      place_environment =_normalize(place.environment)

  if place_environment == requested_environment:
      score += 15
  elif place_environment == "mixed":
      score +=8

  if travel_group and _normalize(travel_group) in {_normalize(style) for style in place.travel_styles
  }:
      score += 10

  if family_friendly is not None and place.family_friendly== family_friendly:
      score += 10

  return score


def filter_places(
        *,
        city: str | None = None,
        category: str | None = None,
        interests: list[str] | None = None,
        budget: str | None = None,
        family_friendly: bool | None = None,
        environment: str | None = None,
        indoors: bool | None = None,
        travel_group: str | None
) -> list[Place]:
    """
    Filter manual dataset places.

    `indoors` is kept for backward compatibility with the earlier API.
    If `enviroment` is not provided:
    - indoors=True -> environment='indoors'
    - indoors=False -> environment='outdoors'
    """
    if environment is None and indoors is not None:
        environment = "indoors" if indoors else "outdoors"

    matches: list[Place] = []

    for place in load_places():
        if city and _normalize(place.city) != _normalize(city):
            continue

        if category and _normalize(place.category) != _normalize(category):
            continue

        if budget and _normalize(place.budget_level) != _normalize(budget):
            continue

        if family_friendly is not None and place.family_friendly != family_friendly:
            continue

        if environment:
            requested_environment = _normalize(environment)
            place_environment = _normalize(place.environment)
            # "mixed" can work for both indoors and outdoors requests.
            if place_environment not in {requested_environment, "mixed"}:
                continue

        if travel_group and _normalize(travel_group) not in { 
            _normalize(style) for style in place.travel_styles
        }:
            continue

        if not _matches_interests(place, interests):
            continue

        matches.append(place)

    return sorted(
            matches,
            key=lambda item: (item.priority_score or 0, item.recommended_duration_hours or 0),
            reverse=True,
        )


def format_places_for_prompt(places: list[Place]) -> str:
    if not places:
        return "No matching places found in the manual Scandinavia dataset."
    
    rows: list[str]= []
    for place in places:
        rows.append(
            "- "
            f"{place.name} | city={place.city} | country={place.country or 'unknown'} |"            
            f"category{place.category} | subcategories={', '.join(place.subcategories) or 'n/a'} | "
            f"budget{place.budget_level or place.price_level or 'unknow'} | "
            f"family_friendly{place.family_friendly} | environment={place.environement or 'unknow'}| "
            f"area{place.area or place.address or 'unknown'} | "
            f"duration_hours={place.recommended_duration_hours or 'n/a'}  | "
            f"tags{', '.join(place.tags) or 'n/a'} | "
            f"source={place.source_type} | description={place.description or 'n/a'}"
        )
    return "\n".join(rows)