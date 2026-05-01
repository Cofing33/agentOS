from __future__ import annotations

import abc
from datetime import datetime, timezone
from typing import Any

import structlog

from src.core.llm import call_llm
from src.core.models import AgentResult, PipelineStatus

logger = structlog.get_logger()


class BaseAgent(abc.ABC):
    """Base class for all pipeline agents."""

    name: str = "base_agent"
    description: str = ""

    @abc.abstractmethod
    def build_system_prompt(self) -> str:
        """Return the system prompt for this agent."""

    @abc.abstractmethod
    def build_user_prompt(self, context: dict[str, Any]) -> str:
        """Build the user prompt from pipeline context."""

    def post_process(self, raw_output: dict | str, context: dict[str, Any]) -> dict[str, Any]:
        """Optional post-processing of LLM output."""
        if isinstance(raw_output, dict):
            return raw_output
        return {"content": raw_output}

    async def run(self, context: dict[str, Any]) -> AgentResult:
        """Execute the agent."""
        logger.info("agent_start", agent=self.name)
        started = datetime.now(timezone.utc)

        try:
            system_prompt = self.build_system_prompt()
            user_prompt = self.build_user_prompt(context)
            raw = await call_llm(system_prompt, user_prompt)
            output = self.post_process(raw, context)

            logger.info("agent_complete", agent=self.name)
            return AgentResult(
                agent_name=self.name,
                status=PipelineStatus.COMPLETED,
                output=output,
                started_at=started,
                finished_at=datetime.now(timezone.utc),
            )
        except Exception as e:
            logger.error("agent_failed", agent=self.name, error=str(e))
            return AgentResult(
                agent_name=self.name,
                status=PipelineStatus.FAILED,
                error=str(e),
                started_at=started,
                finished_at=datetime.now(timezone.utc),
            )
