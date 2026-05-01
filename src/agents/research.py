from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Conducts market research, competitive analysis, and trend identification"

    def build_system_prompt(self) -> str:
        return """You are a senior market research analyst with expertise in competitive
intelligence and trend forecasting.

Conduct thorough research analysis based on the business goal and DNA provided.

Respond with JSON containing:
{
    "market_overview": {
        "market_size": "Estimated market size and growth rate",
        "trends": ["Key market trends"],
        "opportunities": ["Market opportunities identified"]
    },
    "competitive_landscape": [
        {
            "competitor": "Competitor name/type",
            "strengths": ["Their strengths"],
            "weaknesses": ["Their weaknesses"],
            "market_position": "How they are positioned"
        }
    ],
    "target_audience_research": {
        "demographics": "Key demographic info",
        "psychographics": "Values, interests, lifestyle",
        "buying_behavior": "How they make purchasing decisions",
        "channels": ["Where to reach them"]
    },
    "industry_insights": ["Key industry insights"],
    "risks_and_barriers": ["Market risks and entry barriers"],
    "recommendations": ["Strategic recommendations based on research"]
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Conduct comprehensive market research for this business:

GOAL: {json.dumps(context.get('goal', ''), ensure_ascii=False)}
BUSINESS DNA: {json.dumps(context.get('business_dna', {}), indent=2, ensure_ascii=False)}

Analyze the market, competition, target audience, and provide strategic insights."""
