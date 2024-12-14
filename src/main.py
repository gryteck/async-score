from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import health


app = FastAPI(
    title="auth_api",
    docs_url="/docs",
    openapi_url="/src/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(health.router, prefix="", tags=["health"])


if __name__ == "__main__":
    import logging
    from core.logger import LOGGING

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
