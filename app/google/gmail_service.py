"""
Gmail service skeleton.

Məqsəd:
- Bütün Gmail API çağırışlarını tək yerdə toplamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GmailCredentials:
    access_token: str
    user_email: str


@dataclass
class GmailMessage:
    id: str
    subject: str
    sender: str
    snippet: str


class GmailService:
    def __init__(self, creds: GmailCredentials):
        self.creds = creds

    def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Real versiyada: Gmail API ilə mail göndərilməsi.
        Hal-hazırda stub.
        """
        return {
            "status": "stub",
            "to": to,
            "subject": subject,
            "body_length": len(body),
        }

    def fetch_unread_messages(self, max_results: int = 20) -> List[GmailMessage]:
        """
        Yalnız struktur üçün nümunə nəticə.
        """
        return [
            GmailMessage(
                id="stub-1",
                subject="Nümunə mesaj",
                sender="example@example.com",
                snippet="Bu sadəcə test mesajıdır...",
            )
        ][:max_results]

    def mark_as_read(self, message_id: str) -> Dict[str, Any]:
        return {
            "status": "stub",
            "message_id": message_id,
  }
