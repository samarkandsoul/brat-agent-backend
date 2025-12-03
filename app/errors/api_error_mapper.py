"""
API Error Mapper – Sistemdaxili error kodlarını API-friendly formata çevirir.
"""

class ApiErrorMapper:
    ERROR_MAP = {
        "UNAUTHORIZED": {"code": 401, "message": "Authorization failed"},
        "RATE_LIMIT_EXCEEDED": {"code": 429, "message": "Too many requests"},
        "UNKNOWN_COMMAND": {"code": 400, "message": "Unknown command"},
        "NOT_IMPLEMENTED": {"code": 501, "message": "Not implemented"},
        "INVALID_PAYLOAD": {"code": 422, "message": "Invalid payload"},
        "PERMISSION_DENIED": {"code": 403, "message": "Permission denied"},
    }

    @classmethod
    def map_error(cls, error_key: str) -> dict:
        return cls.ERROR_MAP.get(
            error_key,
            {"code": 500, "message": "Internal server error"},
                 )
