"""Request and response schemas for recommendations"""
from pydantic import BaseModel, Field
from app.schemas.place import Place

class RecommendationRequest(BaseModel):
    city: str
    days: int | None = Field(default=1, ge=1, le=14)
    budget: str | None = None #low, medium, high
    interests: list[str] = Field(default_factory=list)
    travel_group: str | None = None # solo, couple, family, friends
    family_friendly: bool | None = None #indoors, outdoors, mixed
    indoors: bool | None = None # kept for backward compatibility
    use_google_maps: bool = False

class RecommendationRequest(BaseModel):
    city: str
    attractions: list[Place] = Field(default_factory=list)
    restaurants: list[Place] = Field(default_factory=list)
    activities: list[Place] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)