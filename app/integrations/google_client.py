# app/integrations/google_client.py

from __future__ import annotations

import base64
import json
import os
from email.message import EmailMessage
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials


# ======================================================
#  CONFIG & CONSTANTS
# ======================================================

GOOGLE_TOKEN_JSON_ENV = "GOOGLE_TOKEN_JSON"
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
]


class GoogleClientError(Exception):
    pass


# ======================================================
#  INTERNAL — CREDENTIALS LOADER
# ======================================================

def _load_credentials(scopes: List[str]) -> Credentials:
    """
    Load OAuth credentials from:
    1) GOOGLE_TOKEN_JSON (Render)
    2) token.json (local)
    """
    raw = os.getenv(GOOGLE_TOKEN_JSON_ENV)
    if raw:
        try:
            data = json.loads(raw)
            return Credentials.from_authorized_user_info(data, scopes=scopes)
        except Exception as e:
            raise GoogleClientError(f"Invalid GOOGLE_TOKEN_JSON: {e}") from e

    if os.path.exists(GOOGLE_TOKEN_FILE):
        try:
            return Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, scopes=scopes)
        except Exception as e:
            raise GoogleClientError(f"Failed to load token.json: {e}") from e

    raise GoogleClientError(
        "Missing Google OAuth token. Set GOOGLE_TOKEN_JSON in Render dashboard."
    )


def _gmail():
    creds = _load_credentials(GMAIL_SCOPES)
    try:
        return build("gmail", "v1", credentials=creds)
    except Exception as e:
        raise GoogleClientError(f"Gmail init error: {e}") from e


def _calendar():
    creds = _load_credentials(CALENDAR_SCOPES)
    try:
        return build("calendar", "v3", credentials=creds)
    except Exception as e:
        raise GoogleClientError(f"Calendar init error: {e}") from e


# ======================================================
#  GMAIL — READ EMAILS
# ======================================================

def list_recent_emails(max_results: int = 10, query: str = "") -> List[Dict[str, Any]]:
    service = _gmail()

    try:
        resp = service.users().messages().list(
            userId="me",
            maxResults=max_results,
            q=query or None,
        ).execute()
    except Exception as e:
        raise GoogleClientError(f"Gmail list error: {e}") from e

    messages = resp.get("messages", []) or []
    results = []

    for m in messages:
        msg_id = m.get("id")
        if not msg_id:
            continue

        try:
            msg = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg_id,
                    format="metadata",
                    metadataHeaders=["From", "Subject", "Date"],
                )
                .execute()
            )
        except Exception:
            continue

        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}

        results.append({
            "id": msg_id,
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
        })

    return results


# ======================================================
#  FORMATTER — FOR MSP (This was missing)
# ======================================================

def format_email_list_for_msp(emails: List[Dict[str, Any]]) -> str:
    """
    Convert Gmail messages into pretty Markdown for Telegram.
    """
    if not emails:
        return "📭 No emails found."

    lines = ["📨 *Recent Emails:*", ""]
    for e in emails:
        lines.append(f"*From:* {e['from']}")
        lines.append(f"*Subject:* {e['subject']}")
        lines.append(f"*Date:* {e['date']}")
        lines.append(f"*Snippet:* {e['snippet']}")
        lines.append("———")

    return "\n".join(lines)


# ======================================================
#  GMAIL — SEND EMAIL
# ======================================================

def send_email(to_email: str, subject: str, body_text: str) -> str:
    service = _gmail()

    msg = EmailMessage()
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body_text)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    try:
        sent = service.users().messages().send(
            userId="me",
            body={"raw": raw},
        ).execute()
    except Exception as e:
        raise GoogleClientError(f"Gmail send error: {e}") from e

    return sent.get("id", "")


# ======================================================
#  CALENDAR — READ EVENTS
# ======================================================

def list_upcoming_events(max_results: int = 10) -> List[Dict[str, Any]]:
    service = _calendar()

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()

    try:
        result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
    except Exception as e:
        raise GoogleClientError(f"Calendar list error: {e}") from e

    return result.get("items", [])


# ======================================================
#  CALENDAR FORMATTER — FOR MSP (missing)
# ======================================================

def format_calendar_for_msp(events: List[Dict[str, Any]]) -> str:
    if not events:
        return "📅 No upcoming events."

    lines = ["📅 *Upcoming Events:*", ""]
    for ev in events:
        start = ev.get("start", {}).get("dateTime") or ev.get("start", {}).get("date")
        end = ev.get("end", {}).get("dateTime") or ev.get("end", {}).get("date")

        lines.append(f"*{ev.get('summary', '(no title)')}*")
        lines.append(f"Start: {start}")
        lines.append(f"End: {end}")
        if ev.get("location"):
            lines.append(f"Location: {ev['location']}")
        lines.append("———")

    return "\n".join(lines)
