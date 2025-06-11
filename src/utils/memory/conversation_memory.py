from __future__ import annotations
from typing import List, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage

class ConversationMemory:
    """Simple in-memory conversation tracker."""

    def __init__(self) -> None:
        self.history: List[Dict[str, str]] = []

    def add_turn(self, user_input: str, agent_name: str, agent_response: str, metadata: Optional[Dict] = None) -> None:
        self.history.append({
            "user_input": user_input,
            "agent_name": agent_name,
            "agent_response": agent_response,
            "metadata": metadata or {}
        })

    def get_context_for_agent(self, agent_name: str, last_n_turns: int = 3) -> str:
        turns = [h for h in self.history if h["agent_name"] == agent_name][-last_n_turns:]
        return "\n".join(
            f"Usuario: {t['user_input']}\n{agent_name}: {t['agent_response']}" for t in turns
        )

    def get_messages_for_langchain(self) -> List:
        messages = []
        for t in self.history:
            messages.append(HumanMessage(content=t["user_input"]))
            messages.append(AIMessage(content=t["agent_response"]))
        return messages

    def get_conversation_summary(self, last_n_turns: int = 2) -> str:
        turns = self.history[-last_n_turns:]
        if not turns:
            return "No hay historial de conversación disponible."
        return "\n".join(f"{t['agent_name']}: {t['agent_response']}" for t in turns)

    def clear_history(self) -> None:
        self.history.clear()
