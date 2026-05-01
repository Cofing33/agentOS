from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class PlanAgent(BaseAgent):
    name = "plan"
    description = "Creates a detailed strategic business plan with milestones"

    def build_system_prompt(self) -> str:
        return """You are a senior business strategist and planning expert.

Create a comprehensive, actionable business plan based on all prior analysis.

Respond with JSON containing:
{
    "executive_summary": "Brief executive summary",
    "phases": [
        {
            "phase_number": 1,
            "name": "Phase name",
            "duration": "e.g., Weeks 1-4",
            "objectives": ["Phase objectives"],
            "key_activities": ["Specific activities"],
            "deliverables": ["What will be produced"],
            "resources_needed": ["Resources required"],
            "budget_estimate": "Cost estimate"
        }
    ],
    "revenue_projections": {
        "month_1_3": "Revenue estimate",
        "month_4_6": "Revenue estimate",
        "month_7_12": "Revenue estimate"
    },
    "key_partnerships": ["Strategic partnerships to pursue"],
    "technology_stack": ["Recommended technologies/tools"],
    "team_structure": ["Roles needed"],
    "milestones": [
        {
            "milestone": "Description",
            "target_date": "When",
            "success_criteria": "How to measure"
        }
    ]
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Create a detailed business plan based on all gathered intelligence:

GOAL: {json.dumps(context.get('goal', ''), ensure_ascii=False)}
BUSINESS DNA: {json.dumps(context.get('business_dna', {}), indent=2, ensure_ascii=False)}
RESEARCH: {json.dumps(context.get('research', {}), indent=2, ensure_ascii=False)}

Develop a phased, actionable plan with clear milestones and resource requirements."""
