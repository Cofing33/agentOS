from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class WebsiteAgent(BaseAgent):
    name = "website"
    description = "Generates website structure, copy, and design specifications"

    def build_system_prompt(self) -> str:
        return """You are a world-class web strategist, UX designer, and copywriter.

Design a complete website strategy with copy, structure, and design specs.

Respond with JSON containing:
{
    "site_structure": {
        "pages": [
            {
                "page_name": "Page name",
                "slug": "/url-slug",
                "purpose": "What this page does",
                "sections": [
                    {
                        "section_name": "Section name",
                        "type": "hero/features/testimonials/cta/etc",
                        "headline": "Section headline",
                        "subheadline": "Supporting text",
                        "content": "Main copy for this section",
                        "cta_text": "Call to action button text",
                        "cta_link": "Where CTA leads"
                    }
                ]
            }
        ]
    },
    "design_specs": {
        "color_palette": {
            "primary": "#hex",
            "secondary": "#hex",
            "accent": "#hex",
            "background": "#hex",
            "text": "#hex"
        },
        "typography": {
            "heading_font": "Font name",
            "body_font": "Font name"
        },
        "style": "Modern/Minimal/Bold/etc"
    },
    "seo_strategy": {
        "primary_keywords": ["Keywords"],
        "meta_descriptions": {"page_name": "Meta description"},
        "content_strategy": "SEO content approach"
    },
    "tech_recommendations": {
        "platform": "Recommended platform",
        "hosting": "Hosting recommendation",
        "integrations": ["Third-party integrations"]
    }
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Design a complete website for this business:

BUSINESS DNA: {json.dumps(context.get('business_dna', {}), indent=2, ensure_ascii=False)}
OFFER: {json.dumps(context.get('offer', {}), indent=2, ensure_ascii=False)}
RESEARCH: {json.dumps(context.get('research', {}), indent=2, ensure_ascii=False)}

Create website structure with all copy, design specs, SEO strategy, and tech recommendations."""
