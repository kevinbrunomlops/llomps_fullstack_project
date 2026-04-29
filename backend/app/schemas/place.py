""" 
Place schema for the Scandinavia travel chatbot.
Matches backend/data/scandinavia_data.json and also supports Google Maps enrichment
"""
from pydantic import BaseModel, Field

class Place(BaseModel):
    id: str | None = None
    name: str
    city: str
    country: str | None = None
    category: str
    subcategories: list[str] = Field(default_factory=list)
    description: str | None = None
    
    # Manual dataset field
    budget_level: str | None = None
    family_friendly: bool | None = None
    environment: str | None = None # indoors, outdoors, mixed
    travel_styles: list[str] = Field(default_factory=list)
    recommended_duration_hours: float | None = None
    best_seasons: list[str] = Field(default_factory=list)
    area: str | None = None
    tags: list[str] = Field(default_factory=list)
    priority_score: int | None = None
    source_type: str = "manual"

    # Optional live-data/enrichment field
    address: str | None = None
    rating: float | None = None
    price_level: str | None = None
    opening_hours: list[str] = Field(default_factory=list)

@property
def source(self) -> str:
    """Backward-compatible source name used by ChatResponse."""
    return self.sourc_type