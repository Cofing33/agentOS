from __future__ import annotations

import asyncio
import json
import re

import anthropic
import structlog

from src.core.config import settings

logger = structlog.get_logger()


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


def _sync_call(system_prompt: str, user_prompt: str) -> str:
    """Synchronous LLM call to be run in a thread."""
    client = get_client()
    message = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=settings.max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text.strip()


async def call_llm(
    system_prompt: str,
    user_prompt: str,
    response_format: str = "json",
) -> dict | str:
    """Call Claude and return parsed JSON or raw text. Non-blocking."""
    if response_format == "json":
        system_prompt += (
            "\n\nIMPORTANT: Respond ONLY with valid JSON. "
            "No markdown, no code fences, no extra text. "
            "Keep responses concise to fit within token limits."
        )

    logger.info("calling_llm", model=settings.anthropic_model)

    raw = await asyncio.to_thread(_sync_call, system_prompt, user_prompt)

    if response_format == "json":
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("json_parse_failed", raw=raw[:200])
            return {"raw_response": raw}

    return raw
