from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PipelineStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentResult(BaseModel):
    agent_name: str
    status: PipelineStatus = PipelineStatus.COMPLETED
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None


class PipelineRun(BaseModel):
    run_id: str
    status: PipelineStatus = PipelineStatus.PENDING
    goal: str
    results: list[AgentResult] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None

    def get_latest_context(self) -> dict[str, Any]:
        """Aggregate all agent outputs into a single context dict."""
        context: dict[str, Any] = {"goal": self.goal}
        for result in self.results:
            if result.status == PipelineStatus.COMPLETED:
                context[result.agent_name] = result.output
        return context
