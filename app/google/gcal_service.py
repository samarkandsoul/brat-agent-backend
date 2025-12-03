"""
Google Calendar service skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class GCalCredentials:
    access_token: str
    calendar_id: str


@dataclass
class CalendarEvent:
    id: str
    title: str
    start: datetime
    end: datetime
    description: str | None = None


class GCalService:
    def __init__(self, creds: GCalCredentials):
        self.creds = creds

    def create_event(self, event: CalendarEvent) -> Dict[str, Any]:
        # TODO: real Google Calendar API call
        return {
            "status": "stub",
            "event_title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat(),
        }

    def list_events(self, from_time: datetime, to_time: datetime) -> List[CalendarEvent]:
        # Stub – boş siyahı qaytarır
        return []
