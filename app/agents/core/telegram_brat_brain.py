# app/agents/core/telegram_brat_brain.py

"""
Telegram BRAT Dialogue Brain

Goal:
- Let Zahid Brat talk to the system using:  BRAT: ...
- Behave like a smart, premium, MAMOS-aware assistant layer on top of MSP.
- Never throw dumb "unclear request" errors.
- If the request is vague → ask 1 sharp clarifying question.
"""

from typing import Optional

from app.llm.brat_gpt import brat_gpt_chat
from app.mamos.mamos_loader import MAMOSLoader
from app.msp.msp import MSP  # adjust import path if your MSP lives elsewhere


class TelegramBratBrain:
    """
    High-level dialogue brain for Telegram.

    - Handles natural language like: "BRAT: hava necədİ?"
    - Decides when to:
        * just answer conversationally, OR
        * ask a clarifying question, OR
        * pass a cleaned command down to MSP (msp: ...).
    """

    def __init__(self, msp: MSP) -> None:
        self.msp = msp

    # ------------------------------------------------------------------
    # Prefix helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _strip_brat_prefix(text: str) -> str:
        """
        Remove 'brat' prefix if present (case-insensitive), with or without ':'.
        Examples that should all be accepted:
            'BRAT: hava necədİ?'
            'brat hava necədİ?'
            'Brat :  shopify product page'
        """
        if not text:
            return ""

        raw = text.strip()
        lower = raw.lower()

        if lower.startswith("brat"):
            # remove 'brat'
            after = raw[4:].lstrip()

            # optionally remove separators like ':' '-' '—'
            while after and after[0] in [":", "-", "—", ";"]:
                after = after[1:].lstrip()

            return after.strip()

        return raw

    @staticmethod
    def _looks_like_msp_command(text: str) -> bool:
        """
        Detect if the cleaned text already looks like a direct MSP command.
        Examples:
            'msp: mamos'
            'msp: shopify: test'
        """
        if not text:
            return False

        return text.strip().lower().startswith("msp:")

    # ------------------------------------------------------------------
    # Core prompt builder
    # ------------------------------------------------------------------
    @staticmethod
    def _build_dialogue_prompt(user_message: str) -> str:
        """
        Build a rich, MAMOS-aware prompt for Brat GPT.

        Rules we encode here:
        - Always treat the user as 'Zahid Brat'
        - Use the same language as the user message (Azerbaijani vs English)
        - If the request is vague, ask ONE smart clarifying question first
        - Never reply with generic 'your question is unclear' without a follow-up
        - Keep tone: premium, calm, smart, but friendly 'Brat' energy
        """
        mamos_doc = MAMOSLoader.load_mamos()
        if not isinstance(mamos_doc, str):
            mamos_doc = ""

        mamos_preview = mamos_doc[:4000]

        return f"""
You are **BRAT**, the official Telegram Agent Bot for the Samarkand Soul ecosystem.

You are talking to a single commander, always the same person:
- Name: Zahid Brat
- Role: System Commander and Founder of Samarkand Soul
- Style: direct, emotional, ambitious, highly strategic

You must ALWAYS:
- Respect the Samarkand Soul MAMOS doctrine (brand, tone, philosophy, safety)
- Speak in the SAME LANGUAGE as Zahid's message (Azerbaijani if he writes in Azerbaijani)
- Keep the tone: calm luxury, clear, premium, but brotherly and direct
- Avoid clickbait, fake promises, or noisy text

If Zahid's request is VAGUE or AMBIGUOUS:
- Do NOT answer immediately.
- Instead, ask ONE short, concrete clarifying question.
- Example:
    User: "BRAT: hava necədİ?"
    You:  "Zahid Brat, hansı şəhərin və hansı günün hava proqnozu lazımdır?"

If Zahid's request clearly targets a specific system domain, REACT LIKE THIS:

1) If it is about Shopify, products, offers, funnels, ads, dropshipping:
   - Treat it as a DS (Dropshipping System) topic.
   - If something is missing (e.g. which product, which market, which date),
     ask a clarifying question.

2) If it is about health, sleep, training, nutrition, balance:
   - Treat it as a LIFE topic.
   - Ask 1 question to understand his current state or goal better.

3) If it is about system, architecture, agents, Render, GitHub, security:
   - Treat it as a SYS topic.
   - Be precise, structured, and warn him about risks if needed.

VERY IMPORTANT:
- Never say generic things like "your request is unclear" alone.
- Always either:
    a) give a direct useful answer, OR
    b) ask ONE smart follow-up question that moves the task forward.

Now here is the official MAMOS doctrine preview (do NOT rewrite it, just use it as context):

[MAMOS PREVIEW START]
{mamos_preview}
[MAMOS PREVIEW END]

Commander message (from Zahid Brat):

\"\"\"{user_message}\"\"\"


Your job:
- Reply as BRAT in a single message.
- No markdown formatting is required for Telegram.
- Keep it natural and compact, but intelligent and premium.
"""

    # ------------------------------------------------------------------
    # Public API: single entrypoint for Telegram messages
    # ------------------------------------------------------------------
    def handle_message(self, raw_text: str) -> str:
        """
        Main entrypoint called from the Telegram webhook layer.

        Logic:
        1) Strip 'BRAT' prefix if present.
        2) If the remaining text is an explicit MSP command → send directly to MSP.
        3) Otherwise → handle as high-level conversation with Brat GPT + MAMOS.
        """
        if not raw_text:
            return "BRAT error: empty message."

        # 1) Remove 'BRAT' prefix if the user used it
        cleaned = self._strip_brat_prefix(raw_text)

        # 2) If the message is a direct MSP command, we just delegate
        if self._looks_like_msp_command(cleaned):
            return self.msp.process(cleaned)

        # 3) Otherwise, use Brat GPT as a dialogue brain
        prompt = self._build_dialogue_prompt(cleaned)

        try:
            reply = brat_gpt_chat(
                user_prompt=prompt,
                agent_role="Telegram BRAT Dialogue Brain",
            )
        except Exception as e:  # noqa: BLE001
            # Fallback: if LLM bridge fails, at least we don't crash Telegram
            return f"BRAT internal error: LLM bridge failed: {e}"

        return reply.strip()
