from __future__ import annotations

import json
import re

import anthropic
import structlog

from src.core.config import settings

logger = structlog.get_logger()


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def call_llm(
    system_prompt: str,
    user_prompt: str,
    response_format: str = "json",
) -> dict | str:
    """Call Claude and return parsed JSON or raw text."""
    client = get_client()

    if response_format == "json":
        system_prompt += (
            "\n\nIMPORTANT: Respond ONLY with valid JSON. "
            "No markdown, no code fences, no extra text."
        )

    logger.info("calling_llm", model=settings.anthropic_model)

    message = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=settings.max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()

    if response_format == "json":
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("json_parse_failed", raw=raw[:200])
            return {"raw_response": raw}

    return raw
