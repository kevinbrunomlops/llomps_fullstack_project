from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router
from app.api.routes.recommendation import router as recommendation_router


app = FastAPI(title="LLMOPS Fullstack API")

app.include_router(health_router)
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(
    recommendation_router,
    prefix="/recommendations",
    tags=["recommendations"],
)