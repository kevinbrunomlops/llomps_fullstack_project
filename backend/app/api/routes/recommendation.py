




from fastapi import APIRouter, HTTPException

from app.schemas.recommendations import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import build_recommendations

router = APIRouter()


@router.post("t", response_model=RecommendationResponse)
async def recommendations(request: RecommendationRequest) ->RecommendationResponse:
    try:
        return await build_recommendations(request)
    except Exception as exc: # pragma: no cover -thin API layer
        raise HTTPException(status_code=500, detail=str(exc)) from exc