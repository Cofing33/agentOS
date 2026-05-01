from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog

from src.core.base_agent import BaseAgent
from src.core.models import PipelineRun, PipelineStatus

logger = structlog.get_logger()


class Pipeline:
    """Orchestrates the sequential execution of agents."""

    def __init__(self, agents: list[BaseAgent]) -> None:
        self.agents = agents

    async def run(self, goal: str) -> PipelineRun:
        run_id = uuid.uuid4().hex[:12]
        pipeline_run = PipelineRun(run_id=run_id, goal=goal, status=PipelineStatus.RUNNING)

        logger.info("pipeline_start", run_id=run_id, goal=goal, agents=len(self.agents))

        for agent in self.agents:
            context = pipeline_run.get_latest_context()
            result = await agent.run(context)
            pipeline_run.results.append(result)

            if result.status == PipelineStatus.FAILED:
                logger.error("pipeline_agent_failed", agent=agent.name, error=result.error)
                pipeline_run.status = PipelineStatus.FAILED
                pipeline_run.finished_at = datetime.now(timezone.utc)
                return pipeline_run

        pipeline_run.status = PipelineStatus.COMPLETED
        pipeline_run.finished_at = datetime.now(timezone.utc)
        logger.info("pipeline_complete", run_id=run_id)
        return pipeline_run


def build_default_pipeline() -> Pipeline:
    from src.agents.actions import ActionsAgent
    from src.agents.business_dna import BusinessDNAAgent
    from src.agents.email_campaign import EmailCampaignAgent
    from src.agents.execute import ExecuteAgent
    from src.agents.goal import GoalAgent
    from src.agents.offer import OfferAgent
    from src.agents.plan import PlanAgent
    from src.agents.quality_risk import QualityRiskAgent
    from src.agents.research import ResearchAgent
    from src.agents.website import WebsiteAgent

    return Pipeline(
        agents=[
            GoalAgent(),
            BusinessDNAAgent(),
            ResearchAgent(),
            PlanAgent(),
            OfferAgent(),
            WebsiteAgent(),
            EmailCampaignAgent(),
            ActionsAgent(),
            QualityRiskAgent(),
            ExecuteAgent(),
        ]
    )
