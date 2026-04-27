from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}