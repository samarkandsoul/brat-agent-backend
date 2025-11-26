# app/agents/ds/ds22_image_auto_agent.py

from dataclasses import dataclass
from typing import List, Dict, Any
import json

from app.mamos.mamos_loader import MAMOSLoader
from app.llm.brat_gpt import brat_gpt_chat


@dataclass
class ImageIdea:
    product_name: str
    use_case: str = ""
    style_notes: str = ""
    extra_info: str = ""


class ImageAutoAgent:
    """
    DS-22 — IMAGE AUTO AGENT

    Goal:
      • Take a short text command (product name + use case + style notes)
      • Use MAMOS + Brat GPT to generate:
          - main AI image prompt
          - 3–5 alternative prompts / shot ideas
          - suggested file names
          - alt-text suggestions
          - small creative notes

    This version only generates text. In the future we can plug in:
      - real AI image generator
      - Shopify image upload
      - Drive folder saving
    """

    def __init__(self) -> None:
        self.mamos = MAMOSLoader.load_mamos()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _build_llm_prompt(self, idea: ImageIdea) -> str:
        """
        Build a strict instruction for Brat GPT.
        We ask for JSON so we can parse reliably.
        """
        base = f"""
You are the IMAGE AUTO AGENT for the Samarkand Soul brand.

Brand essence (from MAMOS, shortened):
Samarkand Soul is a premium home textile brand that brings the spirit of Samarkand
into modern homes. Cultural depth, premium craftsmanship, minimalist aesthetics,
warm emotional storytelling. The tone is calm, elegant, premium and warm.

Task:
Generate an AI image plan for the product:

Product name: {idea.product_name}
Use case: {idea.use_case or "not specified"}
Style notes: {idea.style_notes or "not specified"}
Extra info: {idea.extra_info or "none"}

Rules:
- Images must always feel premium, minimalist and warm.
- No kitsch, no aggressive colors, no cheap stock-photo feeling.
- Focus on emotional family atmosphere, rituals around the table, light & shadows.
- Do NOT mention text overlays in the prompt (no typography, no big written slogans).

Return a SINGLE JSON object with this exact structure:

{{
  "main_prompt": "string – best single prompt for AI image generator",
  "alt_prompts": [
    "string – alternative angle 1",
    "string – alternative angle 2",
    "string – alternative angle 3"
  ],
  "filenames": [
    "string – suggested filename for main image (no spaces, use-dashes)",
    "string – suggested filename for second image",
    "string – suggested filename for third image"
  ],
  "alt_text": [
    "string – alt text for main image (max 140 chars)",
    "string – alt text for second image (max 140 chars)",
    "string – alt text for third image (max 140 chars)"
  ],
  "notes": "string – short creative notes about mood / lighting / composition"
}}

Important:
- JSON only, no markdown, no explanation text outside JSON.
"""
        return base

    def _call_llm(self, idea: ImageIdea) -> Dict[str, Any]:
        prompt = self._build_llm_prompt(idea)

        raw = brat_gpt_chat(
            user_prompt=prompt,
            agent_role="Samarkand Soul Image Auto Agent",
        )

        # Sometimes models wrap JSON in text — try to extract first {...}
        text = raw.strip()
        # crude cleanup
        if text.startswith("```"):
            text = text.strip("`")
            # if it started with ```json, remove the language tag
            text = text.replace("json", "", 1).strip()

        try:
            data = json.loads(text)
        except Exception:
            # Fallback: return minimal structure
            return {
                "main_prompt": text,
                "alt_prompts": [],
                "filenames": [],
                "alt_text": [],
                "notes": "LLM JSON parsing failed, using raw text as main_prompt.",
            }

        return data

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_image_plan(self, idea: ImageIdea) -> str:
        """
        Main entrypoint called from MSP.

        Returns a Telegram-friendly formatted string summarizing
        the image prompts and suggestions.
        """
        data = self._call_llm(idea)

        main_prompt = data.get("main_prompt", "").strip()
        alt_prompts: List[str] = data.get("alt_prompts", []) or []
        filenames: List[str] = data.get("filenames", []) or []
        alt_text: List[str] = data.get("alt_text", []) or []
        notes = data.get("notes", "").strip()

        # Build reply text
        lines: List[str] = []
        lines.append("DS-22 — IMAGE AUTO AGENT reply:")
        lines.append("")
        lines.append(f"Product: {idea.product_name}")
        if idea.use_case:
            lines.append(f"Use case: {idea.use_case}")
        if idea.style_notes:
            lines.append(f"Style notes: {idea.style_notes}")
        lines.append("")

        if main_prompt:
            lines.append("Main AI Prompt:")
            lines.append(main_prompt)
            lines.append("")

        if alt_prompts:
            lines.append("Alternative Prompts:")
            for i, p in enumerate(alt_prompts, start=1):
                lines.append(f"{i}. {p}")
            lines.append("")

        if filenames:
            lines.append("Suggested Filenames:")
            for f in filenames:
                lines.append(f"- {f}")
            lines.append("")

        if alt_text:
            lines.append("Alt-text Suggestions:")
            for t in alt_text:
                lines.append(f"- {t}")
            lines.append("")

        if notes:
            lines.append("Creative Notes:")
            lines.append(notes)

        return "\n".join(lines)
