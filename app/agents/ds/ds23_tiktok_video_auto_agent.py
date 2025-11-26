# app/agents/ds/ds23_tiktok_video_auto_agent.py

from dataclasses import dataclass
from typing import Optional

from app.llm.brat_gpt import brat_gpt_chat


@dataclass
class TikTokVideoIdea:
    """
    Raw command parsed from MSP for DS-23.

    Example MSP text:
      msp: video: Samarkand Soul Ikat Tablecloth | warm beige ikat, cozy ritual | women 28–45 EU/US | 30s POV ASMR

    Fields:
      product_name   -> Samarkand Soul Ikat Tablecloth
      style_brief    -> warm beige ikat, cozy ritual
      target_audience-> women 28–45 EU/US
      extra_notes    -> 30s POV ASMR
    """
    product_name: str
    style_brief: str = ""
    target_audience: str = ""
    extra_notes: str = ""


class TikTokVideoAutoAgent:
    """
    DS-23 – TikTok Video Auto Agent

    Generates a full TikTok/UCG-style video plan for a given product idea,
    fully aligned with the Samarkand Soul MAMOS doctrine.
    """

    def build_prompt(self, idea: TikTokVideoIdea) -> str:
        """
        Build the user prompt that will be sent through brat_gpt_chat().
        MAMOS is injected automatically inside brat_gpt_chat.
        """
        return f"""
You are DS-23 TikTok Video Auto Agent for the Samarkand Soul brand.

Your job:
  - Create a COMPLETE TikTok video concept for a premium home textile product.
  - Follow MAMOS: premium, calm, elegant, emotionally warm, no cheap tactics.
  - Focus on cozy, authentic, ritual-like moments around the dining table.

INPUT:
  Product name: {idea.product_name}
  Visual / style brief: {idea.style_brief or "(none provided)"}
  Target audience: {idea.target_audience or "(not specified)"}
  Extra notes (angle, length, format): {idea.extra_notes or "(none)"}

OUTPUT FORMAT (markdown text):

1. Title / Concept Name
2. One-Sentence Overview
3. Hook Ideas (3 variants)
4. Story Flow (step-by-step, 6–10 beats)
5. Shot List
   - For each shot: (Shot #, framing, what happens, motion, duration)
6. On-Screen Text Ideas
7. Voiceover / Spoken Script (if relevant)
8. Sound Design
   - music type (lofi / ambient / traditional Samarkand-inspired, etc.)
   - key sound details (ASMR table sounds, fabric movement, etc.)
9. CTA (Call To Action)
10. Suggested Hashtags (Samarkand Soul tone, no spam)

Rules:
- Keep everything aligned with premium, minimalist, emotionally warm branding.
- No cringe, no aggressive “buy now” shouting.
- Emphasize: table as a ritual, family / loved ones, calm evening, quality fabric.
""".strip()

    def generate_video_plan(self, idea: TikTokVideoIdea) -> str:
        """
        Call brat_gpt_chat with a MAMOS-aware system prompt and return
        the final formatted reply ready for Telegram.
        """
        prompt = self.build_prompt(idea)
        reply = brat_gpt_chat(
            user_prompt=prompt,
            agent_role="DS-23 TikTok Video Auto Agent",
            model="gpt-4o-mini",
            temperature=0.7,
        )

        header = "DS-23 — TIKTOK VIDEO AUTO AGENT reply:\n\n"
        return header + reply


def generate_tiktok_video_plan_from_text(raw_text: str) -> str:
    """
    Helper used directly by MSP.

    raw_text example (without 'msp: video:'):
      "Samarkand Soul Ikat Tablecloth | warm beige ikat, cozy ritual | women 28–45 EU/US | 30s POV ASMR"

    We parse it into TikTokVideoIdea and call the agent.
    """
    parts = [p.strip() for p in (raw_text or "").split("|")]

    product_name = parts[0] if len(parts) > 0 else ""
    style_brief = parts[1] if len(parts) > 1 else ""
    target_audience = parts[2] if len(parts) > 2 else ""
    extra_notes = " | ".join(parts[3:]) if len(parts) > 3 else ""

    if not product_name:
        return (
            "DS-23 error: product name is empty.\n"
            "Format:\n"
            "  msp: video: Product name | style / angle | target audience | extra notes\n"
        )

    idea = TikTokVideoIdea(
        product_name=product_name,
        style_brief=style_brief,
        target_audience=target_audience,
        extra_notes=extra_notes,
    )

    agent = TikTokVideoAutoAgent()
    return agent.generate_video_plan(idea)
