# app/agents/tiktok_growth/trend_brain.py

"""
TrendBrain

Very simple, rule-based "brain" for now.
Later we will plug real TikTok trend data + LLM here.
For now it just returns a clean daily plan for 3 cozy home textile videos.
"""

from typing import List, Dict, Any
import datetime


class TrendBrain:
    """Plans high-level video ideas for the day."""

    def suggest_daily_plan(self, num_videos: int = 3) -> List[Dict[str, Any]]:
        """
        Return a list of high-level plans for today's videos.

        Each plan item is a dict with:
          - plan_id: unique id for the plan
          - title_hint: short internal title
          - style_tag: visual style for the video_lab
          - llm_caption_prompt: how we will ask LLM to write caption later
        """
        now_ts = int(datetime.datetime.utcnow().timestamp())
        plans: List[Dict[str, Any]] = []

        base_styles = [
            "cozy_minimal_home",
            "soft_beige_kitchen",
            "elegant_table_textile_showcase",
        ]

        for i in range(num_videos):
            style = base_styles[i % len(base_styles)]
            plan_id = f"tga_plan_{now_ts}_{i}"

            plans.append(
                {
                    "plan_id": plan_id,
                    "title_hint": f"Home textile aesthetic #{i + 1}",
                    "style_tag": style,
                    "llm_caption_prompt": (
                        "Write a very short, warm TikTok caption about cozy home textiles, "
                        "in a calm aesthetic tone. No hashtags for now."
                    ),
                }
            )

        return plans
