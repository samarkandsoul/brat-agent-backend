# app/integrations/google_client.py

"""
Google Client – Gmail & Calendar helper for Samarkand Soul agents.

Goal:
- Give DS / SYS agents a simple way to talk to Gmail & Google Calendar.
- Hide OAuth / credentials complexity behind a clean API.
- Work both on local dev and on Render.

Auth model:
- We assume you already created OAuth credentials in Google Cloud
  and generated an authorized user token.

There are three ways to provide the token:

1) Environment variable (recommended for Render):
   - GOOGLE_TOKEN_JSON = full JSON of the authorized user credentials
     (same structure as token.json from Google's quickstart).

2) Token file:
   - GOOGLE_TOKEN_FILE points to token.json (default: "token.json").
   - File must be present in the container.

3) (Optional for local dev only) – interactive flow:
   - You can extend this module later to use InstalledAppFlow if needed.
"""

from __future__ import annotations

import base64
import json
import os
from email.message import EmailMessage
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# =========================
#  CONFIG
# =========================

# Default file paths (can be overridden via env)
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
GOOGLE_TOKEN_JSON_ENV = "GOOGLE_TOKEN_JSON"

# Scopes
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]
CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    # later you can add write scope:
    # "https://www.googleapis.com/auth/calendar.events"
]


class GoogleClientError(Exception):
    """Any Gmail/Calendar integration error."""
    pass


# =========================
#  INTERNAL: CREDENTIALS
# =========================

def _load_credentials(scopes: List[str]) -> Credentials:
    """
    Load OAuth credentials from env or file.

    Priority:
    1) GOOGLE_TOKEN_JSON env (Render-friendly)
    2) GOOGLE_TOKEN_FILE path (defaults to "token.json")

    Raises GoogleClientError if nothing is configured.
    """
    # 1) Env JSON (best for cloud)
    token_json = os.getenv(GOOGLE_TOKEN_JSON_ENV)
    if token_json:
        try:
            data = json.loads(token_json)
            return Credentials.from_authorized_user_info(data, scopes=scopes)
        except Exception as e:
            raise GoogleClientError(
                f"Failed to parse GOOGLE_TOKEN_JSON: {e}"
            ) from e

    # 2) Local token file
    if os.path.exists(GOOGLE_TOKEN_FILE):
        try:
            return Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, scopes=scopes)
        except Exception as e:
            raise GoogleClientError(
                f"Failed to load token from {GOOGLE_TOKEN_FILE}: {e}"
            ) from e

    # 3) No token → error
    raise GoogleClientError(
        "No Google OAuth token configured. "
        "Set GOOGLE_TOKEN_JSON or provide a token file."
    )


def _build_gmail_service():
    """Create a Gmail service client."""
    creds = _load_credentials(GMAIL_SCOPES)
    try:
        service = build("gmail", "v1", credentials=creds)
    except Exception as e:
        raise GoogleClientError(f"Failed to create Gmail service: {e}") from e
    return service


def _build_calendar_service():
    """Create a Calendar service client."""
    creds = _load_credentials(CALENDAR_SCOPES)
    try:
        service = build("calendar", "v3", credentials=creds)
    except Exception as e:
        raise GoogleClientError(f"Failed to create Calendar service: {e}") from e
    return service


# =========================
#  GMAIL – READ
# =========================

def list_recent_emails(
    max_results: int = 10,
    query: str = "",
) -> List[Dict[str, Any]]:
    """
    List recent emails from the primary Gmail inbox.

    :param max_results: maximum number of messages to fetch
    :param query: optional Gmail search query (e.g. 'is:unread subject:order')
    :return: list of dicts: {id, threadId, snippet, from, subject, date}
    """
    service = _build_gmail_service()

    try:
        response = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max_results, q=query)
            .execute()
        )
    except HttpError as e:
        raise GoogleClientError(f"Gmail list error: {e}") from e
    except Exception as e:
        raise GoogleClientError(f"Gmail list unknown error: {e}") from e

    messages = response.get("messages", []) or []
    if not messages:
        return []

    results: List[Dict[str, Any]] = []
    for msg_meta in messages:
        msg_id = msg_meta.get("id")
        if not msg_id:
            continue

        try:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg_id, format="metadata", metadataHeaders=[
                    "From",
                    "Subject",
                    "Date",
                ])
                .execute()
            )
        except Exception:
            # Skip broken messages, but keep going
            continue

        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        results.append(
            {
                "id": msg_id,
                "threadId": msg.get("threadId"),
                "snippet": msg.get("snippet", ""),
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": headers.get("Date", ""),
            }
        )

    return results


# =========================
#  GMAIL – SEND
# =========================

def send_email(
    to_email: str,
    subject: str,
    body_text: str,
    from_email: Optional[str] = None,
) -> str:
    """
    Send a simple plain-text email via Gmail.

    :param to_email: recipient address
    :param subject: email subject
    :param body_text: plain text body
    :param from_email: optional "From" header override
    :return: Gmail message ID
    """
    service = _build_gmail_service()

    msg = EmailMessage()
    msg["To"] = to_email
    msg["Subject"] = subject
    if from_email:
        msg["From"] = from_email

    msg.set_content(body_text)

    encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    body = {"raw": encoded}

    try:
        sent = (
            service.users()
            .messages()
            .send(userId="me", body=body)
            .execute()
        )
    except HttpError as e:
        raise GoogleClientError(f"Gmail send error: {e}") from e
    except Exception as e:
        raise GoogleClientError(f"Gmail send unknown error: {e}") from e

    return sent.get("id", "")


# =========================
#  CALENDAR – READ
# =========================

def list_upcoming_events(
    max_results: int = 10,
    calendar_id: str = "primary",
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    order_by_start_time: bool = True,
) -> List[Dict[str, Any]]:
    """
    List upcoming events from Google Calendar.

    :param max_results: maximum number of events
    :param calendar_id: usually 'primary'
    :param time_min: ISO datetime string; if None, Google uses now()
    :param time_max: ISO datetime string; optional upper bound
    :param order_by_start_time: whether to order by startTime
    :return: list of dicts with event summary, start, end, id
    """
    service = _build_calendar_service()

    params: Dict[str, Any] = {
        "calendarId": calendar_id,
        "maxResults": max_results,
        "singleEvents": True,
    }
    if time_min:
        params["timeMin"] = time_min
    if time_max:
        params["timeMax"] = time_max
    if order_by_start_time:
        params["orderBy"] = "startTime"

    try:
        events_result = service.events().list(**params).execute()
    except HttpError as e:
        raise GoogleClientError(f"Calendar list error: {e}") from e
    except Exception as e:
        raise GoogleClientError(f"Calendar list unknown error: {e}") from e

    events = events_result.get("items", []) or []
    result: List[Dict[str, Any]] = []

    for ev in events:
        result.append(
            {
                "id": ev.get("id"),
                "summary": ev.get("summary", ""),
                "start": ev.get("start", {}),
                "end": ev.get("end", {}),
                "location": ev.get("location", ""),
            }
        )

    return result
