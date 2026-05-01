from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class ActionsAgent(BaseAgent):
    name = "actions"
    description = "Breaks down the plan into concrete, prioritized action items"

    def build_system_prompt(self) -> str:
        return """You are a project management expert who excels at breaking down
complex plans into concrete, actionable tasks.

Create a detailed action plan with prioritized tasks, dependencies, and assignments.

Respond with JSON containing:
{
    "immediate_actions": [
        {
            "action": "What to do",
            "priority": "critical/high/medium/low",
            "category": "marketing/tech/operations/legal/finance",
            "estimated_time": "Time estimate",
            "dependencies": ["What must be done first"],
            "tools_needed": ["Tools or resources required"],
            "expected_outcome": "What success looks like"
        }
    ],
    "week_1_actions": [
        {
            "action": "What to do",
            "priority": "critical/high/medium/low",
            "category": "Category",
            "estimated_time": "Time estimate",
            "assigned_to": "Role responsible"
        }
    ],
    "month_1_actions": [
        {
            "action": "What to do",
            "priority": "Priority",
            "category": "Category",
            "milestone": "Which milestone this supports"
        }
    ],
    "automation_opportunities": [
        {
            "process": "What can be automated",
            "tool": "Recommended automation tool",
            "impact": "Time/cost saved"
        }
    ],
    "daily_habits": ["Daily actions for consistent progress"],
    "weekly_reviews": ["What to review weekly"]
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Break down everything into concrete action items:

GOAL: {json.dumps(context.get('goal', ''), ensure_ascii=False)}
PLAN: {json.dumps(context.get('plan', {}), indent=2, ensure_ascii=False)}
OFFER: {json.dumps(context.get('offer', {}), indent=2, ensure_ascii=False)}
WEBSITE: {json.dumps(context.get('website', {}), indent=2, ensure_ascii=False)}
EMAIL: {json.dumps(context.get('email_campaign', {}), indent=2, ensure_ascii=False)}

Create immediate, week-1, and month-1 action lists with priorities and dependencies."""
