# app/llm/brat_gpt.py

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # library yoxdursa, error mesajı verəcəyik


_client: Optional["OpenAI"] = None


def _get_client() -> Optional["OpenAI"]:
    """
    OpenAI client-i tək nüsxə kimi yaradır.
    OPENAI_API_KEY yoxdursa, None qaytarır.
    """
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    if OpenAI is None:
        # Kitabxana quraşdırılmayıb
        return None

    _client = OpenAI(api_key=api_key)
    return _client


def simple_chat(
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> str:
    """
    Sadə chat helper.
    OPENAI_API_KEY və ya openai kitabxanası yoxdursa, aydın error mətnı qaytarır.
    """
    client = _get_client()
    if client is None:
        return (
            "DS-01 info: OPENAI_API_KEY və ya OpenAI kitabxanası tapılmadı. "
            "Hazırda DS-01 DEMO rejimindədir. 🔌"
        )

    try:
        # Yeni OpenAI clientində klassik chat.completions interfeysi hələ də dəstəklənir.
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        content = resp.choices[0].message.content or ""
        return content.strip()
    except Exception as e:  # pylint: disable=broad-except
        return f"DS-01 OpenAI xətası: {e}"
