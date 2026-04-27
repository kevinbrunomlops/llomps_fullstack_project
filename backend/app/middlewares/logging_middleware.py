from time import perf_counter

from fastapi import FastAPI, Request
from starlette.responses import Response

def logging_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_request(request: Request, call_next) -> Response:
        start = perf_counter()
        response = await call_next(request)
        duration_ms = round((perf_counter() - start) * 1000, 2)
        print(
            f"[{request.method}] {request.url.path} status ={response.status_code} duration_ms=({duration_ms})"
        )
        return response  