from __future__ import annotations

from typing import Any

from src.core.base_agent import BaseAgent


class GoalAgent(BaseAgent):
    name = "goal"
    description = "Clarifies and structures the business goal into actionable objectives"

    def build_system_prompt(self) -> str:
        return """You are a world-class business strategist and goal-setting expert.

Your task is to take a raw business goal/idea and transform it into a structured,
clear, and actionable goal framework.

Respond with JSON containing:
{
    "primary_goal": "Clear one-sentence primary goal",
    "vision": "2-3 sentence vision statement",
    "objectives": ["List of 3-5 specific, measurable objectives"],
    "success_metrics": ["List of KPIs to measure success"],
    "target_audience": "Who is this for",
    "timeline": "Suggested timeline",
    "constraints": ["Any constraints or assumptions identified"]
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Analyze and structure the following business goal:

GOAL: {context['goal']}

Transform this into a structured goal framework with clear objectives,
success metrics, target audience, and timeline."""

    def post_process(self, raw_output: dict | str, context: dict[str, Any]) -> dict[str, Any]:
        if isinstance(raw_output, dict):
            return raw_output
        return {"primary_goal": context["goal"], "raw_analysis": str(raw_output)}
