"""
Auth Guard – sadə token yoxlama skeletonu.

Burada məqsəd: hər request-in içində düzgün auth token varmı?
İndi sadə skeleton verirəm – real token sistemi sonra əlavə ediləcək.
"""

from typing import Optional


class AuthGuard:
    def __init__(self, valid_tokens: Optional[list] = None) -> None:
        self.valid_tokens = valid_tokens or []

    def is_authorized(self, token: Optional[str]) -> bool:
        if not token:
            return False
        return token in self.valid_tokens

    def require_auth(self, token: Optional[str]) -> dict:
        if not self.is_authorized(token):
            return {"ok": False, "error": "UNAUTHORIZED"}

        return {"ok": True}
