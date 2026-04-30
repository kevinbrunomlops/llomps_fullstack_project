from fastapi import APIRouter, HTTPException

from app.agent.travel_agent import run_travel_agent
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("",response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        return await run_travel_agent(request)
    except Exception as exc: # pragma no cover - thin API layer
        raise HTTPException(status_code=500, detail=str(exc)) from exc

