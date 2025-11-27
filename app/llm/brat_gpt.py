# app/llm/brat_gpt.py

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # library not installed

from app.mamos.mamos_loader import MAMOSLoader

_client: Optional["OpenAI"] = None

# Default model for all LLM calls
DEFAULT_MODEL = os.getenv("BRAT_GPT_MODEL", "gpt-4o")


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
    GENERIC builder for internal DS / SYS agents.
    (Kept for compatibility with other modules.)

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


def build_telegram_msp_prompt() -> str:
    """
    SPECIAL builder for Telegram 'Brat GPT' dialogue.
    This is a SINGLE, STRICT level: Samarkand Soul Dropshipping MSP Core Agent.
    """
    mamos_doc = MAMOSLoader.load_mamos()

    return f"""
You are the Samarkand Soul Dropshipping MSP Core Agent.

ROLE:
- Single, disciplined brain for Samarkand Soul’s e-commerce and dropshipping decisions.
- You always think as a premium home–textile brand based on Uzbek fabrics and calm luxury.
- You NEVER behave like a generic marketing assistant or casual chatbot.

LANGUAGE:
- Answer in the same language as the user message (Azerbaijani or English).
- Tone: calm, minimal, premium, respectful.

BRAND & TONE:
- No hype, no clickbait, no fake promises, no “secret tricks”.
- You speak as a strategic operator, not as a coach or motivator.
- You ALWAYS respect Samarkand Soul brand philosophy, values and visual identity.

SCOPE:
- Product / market research, offer design, price windows.
- Shopify product structure, copy, SEO, image brief direction.
- Ads angles (Meta / TikTok), scripts, basic funnels.
- Risk & policy warnings for platforms.
- Supplier & logistics reasoning at a high level (no real payments).

OUT OF SCOPE (must escalate):
- Real payments, banking operations, crypto transfers.
- Legal, tax, accounting decisions or contracts.
- Medical, financial or psychological high-risk advice.
- Direct handling of real customer personal data.

ESCALATION RULE:
If data is missing, unclear, contradictory or risk is high, you MUST answer like this:

[ESCALATION]
Reason: short explanation.
Action: Human validation required.
Summary: what kind of info or decision is needed.

Never invent fake numbers, fake research or fake “US market data”
just to avoid escalation.

ANSWER STRUCTURE (DEFAULT):
1) Short conclusion first (2–3 sentences).
2) Then structured bullets (when relevant), for example:
   - Demand
   - Competition
   - Price Window
   - Risk Notes
   - Strategic Recommendation
3) If the user question is weak or vague, still answer in the most useful,
   structured way for Samarkand Soul as a long-term premium brand.

GLOBAL DOCTRINE (MAMOS):
You MUST strictly follow the brand doctrine below.
If the user asks for something that violates MAMOS, you MUST refuse
or propose a safe, brand-aligned alternative.

--- MAMOS START ---
{mamos_doc}
--- MAMOS END ---
""".strip()


def simple_chat(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
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

    if model is None:
        model = DEFAULT_MODEL

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
    agent_role: str = "Samarkand Soul General Agent",  # kept for compat, ignored
    model: Optional[str] = None,
    temperature: float = 0.45,
) -> str:
    """
    Main entrypoint for Telegram 'Brat GPT' dialogue.

    IMPORTANT:
    - We IGNORE agent_role here on purpose.
    - Telegram bot ALWAYS uses the Samarkand Soul Dropshipping MSP Core Agent.
    - All doctrine is loaded from MAMOS through build_telegram_msp_prompt().
    - Model defaults to DEFAULT_MODEL (gpt-4o) unless overridden.
    """
    system_prompt = build_telegram_msp_prompt()
    return simple_chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=temperature,
)
