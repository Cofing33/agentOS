from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class ExecuteAgent(BaseAgent):
    name = "execute"
    description = "Creates execution roadmap and identifies new work/growth opportunities"

    def build_system_prompt(self) -> str:
        return """You are a senior business execution strategist and growth hacker.

Based on ALL previous analysis, create a final execution plan and identify
new work opportunities and growth channels.

Respond with JSON containing:
{
    "execution_roadmap": {
        "day_1": ["Exact steps to take on day 1"],
        "week_1": ["Prioritized tasks for week 1"],
        "month_1": ["Key deliverables for month 1"],
        "quarter_1": ["Quarterly goals and milestones"]
    },
    "work_finder": {
        "client_acquisition_channels": [
            {
                "channel": "Channel name",
                "strategy": "How to use it",
                "expected_results": "What to expect",
                "cost": "Cost estimate",
                "timeline": "When to start"
            }
        ],
        "partnership_opportunities": [
            {
                "partner_type": "Type of partner",
                "approach": "How to approach them",
                "value_exchange": "What each side gets"
            }
        ],
        "content_marketing_plan": {
            "platforms": ["Where to publish"],
            "content_types": ["Types of content"],
            "frequency": "How often",
            "topics": ["Content topics"]
        },
        "networking_strategy": "How to network effectively",
        "referral_program": {
            "structure": "How the referral program works",
            "incentives": "What referrers get"
        }
    },
    "growth_opportunities": [
        {
            "opportunity": "Description",
            "potential_revenue": "Revenue potential",
            "effort": "high/medium/low",
            "timeline": "When to pursue"
        }
    ],
    "scaling_plan": {
        "triggers": ["When to scale"],
        "how_to_scale": ["Scaling strategies"],
        "resources_needed": ["What's needed to scale"]
    },
    "final_summary": "Executive summary of everything — the complete business launch blueprint"
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        sections = []
        for key in ["goal", "business_dna", "research", "plan", "offer",
                     "website", "email_campaign", "actions", "quality_risk"]:
            if key in context:
                dumped = json.dumps(context[key], indent=2, ensure_ascii=False)
                sections.append(f"{key.upper()}: {dumped}")

        all_context = "\n\n".join(sections)

        return f"""Create the final execution plan and find new work/growth opportunities:

{all_context}

Provide a concrete execution roadmap, client acquisition strategies,
growth opportunities, and a scaling plan. This is the final output that
ties everything together into an actionable blueprint."""
