from fastapi import FastAPI

from app.api.routes import chat, health, recommendations

app = FastAPI(title="Travel Chabot API")

# include routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(health.router, tags=["Health"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])


@app.get("/")
def root():
    return {"message": "API running"}



