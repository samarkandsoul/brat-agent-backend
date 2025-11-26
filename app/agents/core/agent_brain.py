# app/agents/core/agent_brain.py

"""
Agent Brain – unified connector between DS/LIFE/SYS agents and Brat GPT.

Goal:
- Give every agent the same "brain style"
- Inject MAMOS doctrine automatically
- Keep responses clean, premium and brand-aligned
"""

from typing import Optional

from app.llm.brat_gpt import brat_gpt_chat
from app.mamos.mamos_loader import MAMOSLoader


def get_mamos_preview(max_chars: int = 3000) -> str:
    """
    Helper: return a safe-sized preview of the MAMOS doctrine.
    Can be used by MSP or any agent when they want to show MAMOS to the user.
    """
    doc = MAMOSLoader.load_mamos()
    return doc[:max_chars]


class AgentBrain:
    """
    Unified brain wrapper for any Samarkand Soul agent.

    Typical usage inside a DS/LIFE/SYS module:

        from app.agents.core.agent_brain import AgentBrain

        brain = AgentBrain(agent_code="ds03", agent_label="SHOPIFY-AGENT")

        def handle_shopify_task(user_input: str) -> str:
            return brain.ask(
                user_prompt=user_input,
                extra_context="You are configuring the official Samarkand Soul Shopify store.",
            )

    The brain:
    - Always uses the MAMOS doctrine (through Brat GPT + system prompt)
    - Always speaks in a premium, clear, structured style
    """

    def __init__(
        self,
        agent_code: str,
        agent_label: str,
        default_model: str = "gpt-4o-mini",
        default_temperature: float = 0.6,
    ) -> None:
        """
        :param agent_code: short code like 'ds03', 'life01', 'sys02'
        :param agent_label: human-readable label like 'SHOPIFY-AGENT'
        :param default_model: OpenAI model name
        :param default_temperature: default creativity level
        """
        self.agent_code = agent_code.lower().strip()
        self.agent_label = agent_label.strip()
        self.agent_role = f"{self.agent_code.upper()} — {self.agent_label}"
        self.model = default_model
        self.temperature = default_temperature

    def build_user_prompt(
        self,
        user_prompt: str,
        extra_context: Optional[str] = None,
    ) -> str:
        """
        Merge the main user prompt with optional extra context.

        extra_context is used for:
        - giving more technical details
        - passing state from MSP or other agents
        """
        user_prompt = (user_prompt or "").strip()
        extra_context = (extra_context or "").strip()

        if not extra_context:
            return user_prompt

        # We keep it very explicit so the LLM understands the separation.
        return (
            "You are given additional context for this task.\n"
            "1) CONTEXT:\n"
            f"{extra_context}\n\n"
            "2) MAIN REQUEST:\n"
            f"{user_prompt}\n\n"
            "Use the context only to improve the answer. "
            "If something in the context conflicts with MAMOS or brand rules, "
            "follow MAMOS first."
        )

    def ask(
        self,
        user_prompt: str,
        extra_context: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        wrap_with_header: bool = True,
    ) -> str:
        """
        Main method used by agents to talk to Brat GPT with the MAMOS brain.

        :param user_prompt: the human-readable request / task
        :param extra_context: optional extra technical or business context
        :param temperature: override creativity level if needed
        :param model: override model name if needed
        :param wrap_with_header: if True, prepend a short header to the reply
        """
        final_temperature = self.temperature if temperature is None else temperature
        final_model = self.model if model is None else model

        merged_prompt = self.build_user_prompt(
            user_prompt=user_prompt,
            extra_context=extra_context,
        )

        raw_reply = brat_gpt_chat(
            user_prompt=merged_prompt,
            agent_role=self.agent_role,
            model=final_model,
            temperature=final_temperature,
        )

        if not wrap_with_header:
            return raw_reply

        header = f"MSP / {self.agent_role} reply:\n"
        return header + raw_reply
