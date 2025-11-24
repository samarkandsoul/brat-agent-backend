# app/llm/brat_gpt.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
Sən Zahid Brat üçün şəxsi AI Brat köməkçisən.
Ton: səmimi, ağıllı, bir az zarafatcıllı, amma ciddi strateq.
Texniki mövzularda addım-addım izah ver, problemi gizlətmə.
Nəyi edə bilmirsənsə, dürüst de və səbəbini izah et.
Cümlələrin çox uzun olmasın, Azərbaycan dilində danış.
"""

_conversations = {}

def brat_gpt_chat(user_id: str, user_message: str) -> str:
    history = _conversations.get(user_id, [])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.4,
    )

    answer = response.choices[0].message.content

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": answer})
    _conversations[user_id] = history[-10:]

    return answer
