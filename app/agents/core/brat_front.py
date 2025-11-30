# app/agents/core/brat_front.py

"""
Brat Front Layer – Telegram 'BRAT:' messages router.

Goal:
- User always talks with:  BRAT: ...
- Front layer decides:
    • is this MSP command?
    • is this general GPT chat?
    • is extra clarification needed?
- Always answer in dialog style:
    ZAHID BRAT: ...   (input)
    BRAT: ...         (reply)
"""

from typing import Literal, Tuple

from app.llm.brat_gpt import brat_gpt_chat
from app.msp import MSP
from app.mamos.mamos_loader import MAMOSLoader


RouterDecision = Literal["DIRECT_ANSWER", "MSP_COMMAND", "CLARIFY"]


def _clean_brat_prefix(raw_text: str) -> str:
    """
    Remove 'BRAT:' or 'brat:' prefix (and Samarkand Soul macro if used).
    """
    text = (raw_text or "").strip()

    # Köhnə makro dəstəyi: "SAMARKAND SOUL SAMARKAND SOUL: ..."
    lower = text.lower()
    if lower.startswith("samarkand soul samarkand soul:"):
        text = text.split(":", 1)[1].strip()
        lower = text.lower()

    # Əsas prefix: "BRAT:"
    if lower.startswith("brat:"):
        text = text.split(":", 1)[1].strip()

    return text


def _router_llm_decision(user_body: str) -> Tuple[RouterDecision, str]:
    """
    Ask Brat GPT how to handle this BRAT message.

    Returns:
        (decision, payload)

        decision = "DIRECT_ANSWER"  → payload = final answer text
        decision = "MSP_COMMAND"    → payload = pure MSP text (e.g. 'msp: mamos')
        decision = "CLARIFY"        → payload = clarification question text
    """
    mamos_preview = MAMOSLoader.load_mamos()
    if isinstance(mamos_preview, str) and mamos_preview.startswith("[MAMOS ERROR]"):
        mamos_preview = (
            "MAMOS doctrine is temporarily unavailable. "
            "Act with calm, safe, premium logic."
        )

    system_brief = (
        "You are BRAT FRONT ROUTER for the Samarkand Soul ecosystem.\n"
        "You NEVER speak as the final assistant. You ONLY decide what to do.\n\n"
        "You know that the system has:\n"
        "- MSP core with many commands like 'msp: mamos', 'msp: shopify: ...', etc.\n"
        "- General GPT chat mode (Samarkand Soul branded chat).\n"
        "- Escalation / clarification discipline from MAMOS.\n\n"
        "Short MAMOS doctrine preview:\n"
        f"{mamos_preview[:1500]}\n\n"
        "ROUTING RULES:\n"
        "1) If the user text ALREADY starts with 'msp:' (case-insensitive),\n"
        "   you must route it as MSP_COMMAND with the body exactly as MSP expects.\n"
        "2) If the user clearly asks about an operation that SHOULD be handled by MSP\n"
        "   (Shopify, DS agents, DriveAgent, Gmail, Calendar, Web research, etc.),\n"
        "   you should convert the request into a concrete 'msp: ...' command\n"
        "   and return MSP_COMMAND.\n"
        "3) If the user question is clearly a simple conversation, explanation,\n"
        "   brainstorming or motivation request (no explicit system action),\n"
        "   you answer it yourself as DIRECT_ANSWER in premium calm luxury style.\n"
        "4) If the request is too vague to act safely (e.g. 'hava necəsə?'),\n"
        "   return CLARIFY and ask ONE precise follow-up question.\n"
        "   The question must be short and concrete.\n\n"
        "IMPORTANT:\n"
        "- You must ALWAYS return in a strict machine-readable format.\n"
        "- No markdown, no extra text, no greetings.\n"
        "- Do not invent real payments or do risky operations.\n\n"
        "OUTPUT FORMAT (no quotes):\n"
        "  DECISION: <DIRECT_ANSWER | MSP_COMMAND | CLARIFY>\n"
        "  PAYLOAD: <your text here in a single line>\n"
    )

    user_brief = (
        "User BRAT message:\n"
        f"{user_body}\n\n"
        "Now decide following the rules and output exactly two lines."
    )

    # brat_gpt_chat-də ayrıca system_prompt yoxdur → hamısını user_prompt-a qatırıq
    raw = brat_gpt_chat(
        user_prompt=system_brief + "\n\n" + user_brief,
        agent_role="BRAT_FRONT_ROUTER",
        model="gpt-4o-mini",
        temperature=0.3,
    )

    decision: RouterDecision = "DIRECT_ANSWER"
    payload = ""

    for line in raw.splitlines():
        line = line.strip()
        upper = line.upper()
        if upper.startswith("DECISION:"):
            val = line.split(":", 1)[1].strip().upper()
            if val in {"DIRECT_ANSWER", "MSP_COMMAND", "CLARIFY"}:
                decision = val  # type: ignore[assignment]
        elif upper.startswith("PAYLOAD:"):
            payload = line.split(":", 1)[1].strip()

    if not payload:
        decision = "CLARIFY"  # type: ignore[assignment]
        payload = (
            "Zahid Brat, sualın çox ümumidir. Zəhmət olmasa daha konkret izah et."
        )

    return decision, payload


def process_brat_message(raw_text: str, sender_label: str = "ZAHID BRAT") -> str:
    """
    Main entrypoint for Telegram 'BRAT:' messages.

    - Cleans prefix
    - Asks router LLM how to handle it
    - Either:
        * calls MSP,
        * answers directly via GPT,
        * or asks a clarification question.
    - Always returns text starting with 'BRAT:'
    """
    body = _clean_brat_prefix(raw_text)

    if not body:
        return (
            "BRAT: Zahid Brat, mesaj boşdur. "
            "Zəhmət olmasa sualını və ya tapşırığını yaz."
        )

    # Əgər artıq 'msp:' ilə başlayırsa – birbaşa MSP-yə ötür
    if body.lower().startswith("msp:"):
        msp = MSP()
        reply = msp.process(body)
        return f"BRAT: {reply}"

    decision, payload = _router_llm_decision(body)

    # --- CLARIFY: follow-up sual ver ---
    if decision == "CLARIFY":
        return f"BRAT: {payload}"

    # --- MSP_COMMAND: MSP core-a route et ---
    if decision == "MSP_COMMAND":
        msp_command = payload
        if not msp_command.lower().startswith("msp:"):
            msp_command = "msp: " + msp_command.strip()

        msp = MSP()
        reply = msp.process(msp_command)
        return f"BRAT: {reply}"

    # --- DIRECT_ANSWER: birbaşa GPT ilə cavabla ---
    if decision == "DIRECT_ANSWER":
        answer = payload

        # Router çox qısa cavab verdiyi halda – cavabı genişləndirmək üçün GPT çağırırıq
        if len(answer) < 40:
            prompt = (
                "You are BRAT, the official Samarkand Soul assistant.\n"
                "Answer the commander in calm luxury, realistic and clear style.\n"
                f"Question from {sender_label}:\n{body}\n\n"
                "If there is any risk or ambiguity, mention it briefly but still answer."
            )
            answer = brat_gpt_chat(
                user_prompt=prompt,
                agent_role="BRAT_DIRECT_CHAT",
                model="gpt-4o-mini",
                temperature=0.6,
            )

        return f"BRAT: {answer}"

    # Fallback (normalda bura düşməməlidir)
    return (
        "BRAT: Sistem router cavabını düzgün anlamadı. "
        "Zəhmət olmasa sualını bir az daha aydın yaz."
)
