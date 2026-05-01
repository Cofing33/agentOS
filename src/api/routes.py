from __future__ import annotations

import asyncio
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from src.core.models import PipelineRun, PipelineStatus
from src.core.pipeline import build_default_pipeline

router = APIRouter()

# In-memory storage for pipeline runs
_runs: dict[str, PipelineRun] = {}
_lock = asyncio.Lock()


class RunRequest(BaseModel):
    goal: str


class RunResponse(BaseModel):
    run_id: str
    status: str
    message: str


async def _execute_pipeline(run_id: str, goal: str) -> None:
    pipeline = build_default_pipeline()
    result = await pipeline.run(goal)
    async with _lock:
        _runs[run_id] = result


@router.post("/run", response_model=RunResponse)
async def start_pipeline(request: RunRequest, background_tasks: BackgroundTasks) -> RunResponse:
    """Start a new pipeline run with the given business goal."""
    run_id = uuid.uuid4().hex[:12]
    placeholder = PipelineRun(run_id=run_id, goal=request.goal, status=PipelineStatus.RUNNING)

    async with _lock:
        _runs[run_id] = placeholder

    background_tasks.add_task(_execute_pipeline, run_id, request.goal)

    return RunResponse(
        run_id=run_id,
        status="running",
        message="Pipeline started. Use GET /run/{run_id} to check progress.",
    )


@router.post("/run/sync")
async def run_pipeline_sync(request: RunRequest) -> dict[str, Any]:
    """Run the full pipeline synchronously and return all results."""
    pipeline = build_default_pipeline()
    result = await pipeline.run(request.goal)

    async with _lock:
        _runs[result.run_id] = result

    return result.model_dump(mode="json")


@router.get("/run/{run_id}")
async def get_run(run_id: str) -> dict[str, Any]:
    """Get the status and results of a pipeline run."""
    async with _lock:
        run = _runs.get(run_id)

    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    return run.model_dump(mode="json")


@router.get("/runs")
async def list_runs() -> list[dict[str, Any]]:
    """List all pipeline runs."""
    async with _lock:
        return [
            {
                "run_id": run.run_id,
                "status": run.status.value,
                "goal": run.goal,
                "created_at": run.created_at.isoformat(),
                "agents_completed": len(
                    [r for r in run.results if r.status == PipelineStatus.COMPLETED]
                ),
                "total_agents": 10,
            }
            for run in _runs.values()
        ]


@router.get("/agents")
async def list_agents() -> list[dict[str, str]]:
    """List all available agents in the pipeline."""
    pipeline = build_default_pipeline()
    return [
        {"name": agent.name, "description": agent.description} for agent in pipeline.agents
    ]


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "ai-agent-chain"}
