from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class BusinessDNAAgent(BaseAgent):
    name = "business_dna"
    description = "Defines the core business identity, values, and differentiators"

    def build_system_prompt(self) -> str:
        return """You are an expert business analyst specializing in brand strategy and
business identity.

Your task is to define the "Business DNA" — the core identity, values, positioning,
and unique differentiators of the business.

Respond with JSON containing:
{
    "business_name_suggestions": ["3 suggested business names"],
    "mission_statement": "Concise mission statement",
    "core_values": ["List of 4-5 core values with brief descriptions"],
    "unique_value_proposition": "What makes this business unique",
    "brand_personality": {
        "tone": "Professional/Casual/Bold/etc",
        "voice_attributes": ["List of brand voice attributes"]
    },
    "target_market_segments": [
        {
            "segment": "Segment name",
            "description": "Brief description",
            "pain_points": ["Key pain points this segment has"]
        }
    ],
    "competitive_advantages": ["List of key competitive advantages"],
    "business_model": "How the business will make money"
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        goal_data = context.get("goal", {})
        goal_analysis = context.get("goal", {})
        if isinstance(goal_analysis, str):
            goal_analysis = {"primary_goal": goal_analysis}

        return f"""Based on the following structured goal, define the complete Business DNA:

GOAL: {json.dumps(goal_data, indent=2, ensure_ascii=False)}
GOAL ANALYSIS: {json.dumps(goal_analysis, indent=2, ensure_ascii=False)}

Create a comprehensive business identity framework."""
