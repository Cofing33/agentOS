from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class OfferAgent(BaseAgent):
    name = "offer"
    description = "Designs compelling product/service offers and pricing strategy"

    def build_system_prompt(self) -> str:
        return """You are an expert in product strategy, pricing, and offer design.

Create irresistible offers that align with the business goals and target market.

Respond with JSON containing:
{
    "core_offer": {
        "name": "Product/service name",
        "description": "What it is",
        "key_benefits": ["Main benefits"],
        "features": ["Key features"],
        "pricing": {
            "model": "Pricing model (subscription/one-time/freemium/etc)",
            "tiers": [
                {
                    "tier_name": "Name",
                    "price": "Price",
                    "includes": ["What's included"],
                    "ideal_for": "Who this tier is for"
                }
            ]
        }
    },
    "upsells": [
        {
            "name": "Upsell name",
            "description": "What it is",
            "price": "Price"
        }
    ],
    "lead_magnet": {
        "type": "Type of lead magnet",
        "title": "Title",
        "description": "What they get for free"
    },
    "guarantees": ["Risk reversals and guarantees"],
    "social_proof_strategy": "How to build social proof",
    "launch_offer": {
        "description": "Special launch offer",
        "discount": "Launch discount",
        "urgency": "Time-limited element"
    }
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Design compelling offers for this business:

GOAL: {json.dumps(context.get('goal', ''), ensure_ascii=False)}
BUSINESS DNA: {json.dumps(context.get('business_dna', {}), indent=2, ensure_ascii=False)}
RESEARCH: {json.dumps(context.get('research', {}), indent=2, ensure_ascii=False)}
PLAN: {json.dumps(context.get('plan', {}), indent=2, ensure_ascii=False)}

Create offers with pricing tiers, upsells, lead magnets, and a launch strategy."""
