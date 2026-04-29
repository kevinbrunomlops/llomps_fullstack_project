"""Requests and repsonse schemas for chat endpoint."""

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str
    city: str | None = None
    days: int | None = Field(default=1, ge=1, le=14)
    budget: str | None = None # low, medium, high
    interests: list[str] = Field(default_factory=list)
    travel_group: str | None = None # solo, couple, family, friends
    family_friendly: bool | None = None
    environment: str | None = None # indoors, outdoors, mixed
    indoors: bool | None = None
    use_google_maps: bool = False
    prompt_version: str 

class ChatResponse(BaseModel):
    answer: str
    city: str | None = None
    prompt_name: str
    prompt_version: str
    attractions: list[dict] = Field(default_factory=list)
    restaurants: list[dict] = Field(default_factory=list)
    activities: list[dict] = Field(default_factory=list)
    follow_up_questions: list[dict] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)

