"""
Global Error Handler – Brat sistemində bütün gözlənilməz error-lar buradan keçir.
"""

import traceback


class GlobalErrorHandler:
    @staticmethod
    def handle_error(e: Exception) -> dict:
        return {
            "ok": False,
            "error": str(e),
            "trace": traceback.format_exc(),
        }
