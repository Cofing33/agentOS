from __future__ import annotations

import json
from typing import Any

from src.core.base_agent import BaseAgent


class QualityRiskAgent(BaseAgent):
    name = "quality_risk"
    description = "Reviews all outputs for quality, identifies risks, and suggests improvements"

    def build_system_prompt(self) -> str:
        return """You are a senior quality assurance and risk management expert.

Review ALL outputs from previous agents. Identify quality issues, risks, gaps,
and provide improvement recommendations.

Respond with JSON containing:
{
    "overall_quality_score": 85,
    "quality_assessment": {
        "strengths": ["What's strong in the overall plan"],
        "weaknesses": ["Areas that need improvement"],
        "gaps": ["Missing elements or blind spots"]
    },
    "risk_analysis": [
        {
            "risk": "Risk description",
            "category": "market/financial/operational/legal/technical",
            "probability": "high/medium/low",
            "impact": "high/medium/low",
            "mitigation": "How to mitigate this risk"
        }
    ],
    "legal_compliance": {
        "requirements": ["Legal/regulatory requirements to address"],
        "warnings": ["Potential legal issues"]
    },
    "financial_risks": {
        "burn_rate_concern": "Assessment of financial sustainability",
        "revenue_reality_check": "Are revenue projections realistic",
        "recommendations": ["Financial recommendations"]
    },
    "improvement_suggestions": [
        {
            "area": "Which part to improve",
            "current_issue": "What's wrong",
            "suggestion": "How to fix it",
            "priority": "high/medium/low"
        }
    ],
    "go_no_go_recommendation": {
        "decision": "GO/CONDITIONAL_GO/NO_GO",
        "reasoning": "Why",
        "conditions": ["Conditions that must be met (if conditional)"]
    }
}"""

    def build_user_prompt(self, context: dict[str, Any]) -> str:
        sections = []
        for key in ["goal", "business_dna", "research", "plan", "offer",
                     "website", "email_campaign", "actions"]:
            if key in context:
                dumped = json.dumps(context[key], indent=2, ensure_ascii=False)
                sections.append(f"{key.upper()}: {dumped}")

        all_context = "\n\n".join(sections)

        return f"""Review ALL outputs from the pipeline and provide quality/risk assessment:

{all_context}

Be thorough and critical. Identify every risk, gap, and improvement opportunity."""
