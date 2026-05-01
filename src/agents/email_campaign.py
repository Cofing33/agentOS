from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class EmailCampaignAgent(BaseAgent):
    name = "email_campaign"
    description = "Creates email marketing sequences and campaigns"

    def build_system_prompt(self) -> str:
        return """You are an expert email marketer and copywriter specializing in
automated email sequences and campaigns.

Create a complete email marketing strategy with ready-to-use email copy.

Respond with JSON containing:
{
    "welcome_sequence": [
        {
            "email_number": 1,
            "subject_line": "Subject",
            "preview_text": "Preview text",
            "send_delay": "When to send (e.g., immediately, +1 day)",
            "purpose": "Goal of this email",
            "body": "Full email body (use markdown for formatting)",
            "cta": "Call to action"
        }
    ],
    "nurture_sequence": [
        {
            "email_number": 1,
            "subject_line": "Subject",
            "send_delay": "When to send",
            "purpose": "Goal",
            "body": "Full email body",
            "cta": "Call to action"
        }
    ],
    "sales_sequence": [
        {
            "email_number": 1,
            "subject_line": "Subject",
            "send_delay": "When to send",
            "purpose": "Goal",
            "body": "Full email body",
            "cta": "Call to action"
        }
    ],
    "re_engagement_emails": [
        {
            "trigger": "When to send",
            "subject_line": "Subject",
            "body": "Email body"
        }
    ],
    "email_platform_recommendation": "Recommended email platform",
    "segmentation_strategy": "How to segment the email list",
    "kpis": ["Email marketing KPIs to track"]
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        return f"""Create a complete email marketing strategy:

BUSINESS DNA: {json.dumps(context.get('business_dna', {}), indent=2, ensure_ascii=False)}
OFFER: {json.dumps(context.get('offer', {}), indent=2, ensure_ascii=False)}
WEBSITE: {json.dumps(context.get('website', {}), indent=2, ensure_ascii=False)}

Design welcome, nurture, sales, and re-engagement email sequences with full copy."""
