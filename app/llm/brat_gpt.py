# app/llm/brat_gpt.py

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # library not installed


from app.mamos.mamos_loader import MAMOSLoader

_client: Optional["OpenAI"] = None


def _get_client() -> Optional["OpenAI"]:
    """
    Create a single OpenAI client instance.
    If OPENAI_API_KEY is missing or library is not installed, return None.
    """
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    if OpenAI is None:
        return None

    _client = OpenAI(api_key=api_key)
    return _client


def build_system_prompt(agent_role: str = "Samarkand Soul General Agent") -> str:
    """
    Build a unified system prompt for any agent using the MAMOS doctrine.
    agent_role example: "DS-03 Shopify Agent" or "DS-06 Creative Scriptwriter".
    """
    mamos_doc = MAMOSLoader.load_mamos()

    return f"""
You are {agent_role} inside the Samarkand Soul ecosystem.

You MUST strictly follow the brand doctrine (MAMOS) below.
Never break its rules about premium quality, customer respect,
platform compliance and long-term brand building.

If the user asks for something that violates MAMOS, you MUST refuse
or propose a safe, brand-aligned alternative.

--- MAMOS START ---
{mamos_doc}
--- MAMOS END ---
""".strip()


def simple_chat(
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> str:
    """
    Basic chat helper.
    If OPENAI_API_KEY or OpenAI library is missing, return a clear info message.
    """
    client = _get_client()
    if client is None:
        return (
            "LLM info: OPENAI_API_KEY or OpenAI library not found. "
            "LLM is currently in DEMO mode. 🔌"
        )

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        content = resp.choices[0].message.content or ""
        return content.strip()
    except Exception as e:  # pylint: disable=broad-except
        return f"LLM error: {e}"


def brat_gpt_chat(
    user_prompt: str,
    agent_role: str = "Samarkand Soul General Agent",
    model: str = "gpt-4o-mini",
    temperature: float = 0.6,
) -> str:
    """
    Main entrypoint for Telegram 'Brat GPT' dialogue.
    This function is used in the Agent Backend:

        from app.llm.brat_gpt import brat_gpt_chat

    It automatically injects the MAMOS doctrine into the system prompt.
    """
    system_prompt = build_system_prompt(agent_role=agent_role)
    return simple_chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=temperature,
    )
