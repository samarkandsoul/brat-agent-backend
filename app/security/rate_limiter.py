"""
Rate Limiter – API-nin həddən artıq istifadə olunmasının qarşısını alır.

Sadə in-memory counter.
Real variant Redis-lə olacaq, amma skeleti bu cürdür.
"""

import time
from typing import Dict


class RateLimiter:
    def __init__(self, max_calls: int = 30, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        user_requests = self.requests.setdefault(user_id, [])

        # köhnə requestləri təmizləyək
        self.requests[user_id] = [ts for ts in user_requests if ts > window_start]

        # limit keçilib?
        if len(self.requests[user_id]) >= self.max_calls:
            return False

        # yeni request qeyd edirik
        self.requests[user_id].append(now)
        return True

    def guard(self, user_id: str) -> dict:
        if not self.is_allowed(user_id):
            return {"ok": False, "error": "RATE_LIMIT_EXCEEDED"}

        return {"ok": True}
