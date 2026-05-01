from __future__ import annotations

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.core.config import settings

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        structlog.get_level_from_name(settings.log_level)
    ),
)

app = FastAPI(
    title="AI Agent Chain",
    description=(
        "Fully automated AI agent pipeline: "
        "Goal → Business DNA → Research → Plan → Offer → "
        "Website → Email → Actions → Quality/Risk → Execute + Work Finder"
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "AI Agent Chain",
        "version": "0.1.0",
        "docs": "/docs",
        "description": (
            "Send a POST to /api/run/sync with {\"goal\": \"your business goal\"} "
            "to run the full 10-agent pipeline."
        ),
    }


def main() -> None:
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )


if __name__ == "__main__":
    main()
