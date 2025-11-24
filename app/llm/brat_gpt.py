# app/llm/brat_gpt.py

import os
from openai import OpenAI

# OPENAI_API_KEY mühit dəyişənindən oxunur
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are GPT Brat, an AI mentor and co-founder for Zahid Brat.
- Speak in the same language as the user (Azerbaijani or Turkish or English).
- Be clear, practical and friendly.
- Explain technical things step by step, but without walls of text.
- If you don't know something or have no access (like hidden logs, local files), say it honestly.
- Help with coding, system design, business strategy, and debugging.
"""


def brat_gpt_chat(user_message: str) -> str:
    """
    Sadə wrapper: bir mesaj alır, bir cavab qaytarır.
    Hələlik yaddaş saxlamırıq, sonra əlavə edərik.
    """

    if not client.api_key:
        return "BratGPT error: OPENAI_API_KEY serverdə qurulmayıb."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        # Burda xəta olsa, heç olmasa izah edək
        return f"BratGPT LLM error: {e}"
