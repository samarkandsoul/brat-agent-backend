"""
Google Calendar plan generator skeleton.

Məqsəd:
- Günlük / həftəlik plan skeleton-u
- Sonra GCalService ilə real calendara yazıla bilər
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from .gcal_service import CalendarEvent, GCalService


@dataclass
class DayPlanInput:
    date: datetime
    focus_theme: str  # məsələn: "Creative work", "Ops", "Health"
    deep_work_blocks: int = 2


class GCalPlanGenerator:
    def __init__(self, gcal: GCalService):
        self.gcal = gcal

    def generate_day_plan(self, config: DayPlanInput) -> List[CalendarEvent]:
        events: List[CalendarEvent] = []
        base = config.date.replace(hour=10, minute=0, second=0, microsecond=0)

        # Deep work blokları
        for i in range(config.deep_work_blocks):
            start = base + timedelta(hours=2 * i)
            end = start + timedelta(hours=1, minutes=30)
            events.append(
                CalendarEvent(
                    id=f"deep-work-{i}",
                    title=f"Deep Work – {config.focus_theme}",
                    start=start,
                    end=end,
                    description="Telefon off, yalnız fokus işi.",
                )
            )

        # Axşam review
        review_start = base.replace(hour=19)
        events.append(
            CalendarEvent(
                id="daily-review",
                title="Daily Review & Planning",
                start=review_start,
                end=review_start + timedelta(minutes=30),
                description="Bu günün yekunu, sabahın planı.",
            )
        )

        return events

    def push_day_plan_to_calendar(self, config: DayPlanInput) -> int:
        events = self.generate_day_plan(config)
        for ev in events:
            self.gcal.create_event(ev)
        return len(events)
