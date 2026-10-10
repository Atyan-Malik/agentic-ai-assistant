
from collections import defaultdict

from agent.prompts import get_system_prompt
from agent.schemas import Message


class ConversationContext:
    """Manage message history for individual conversations."""

    def __init__(self, max_history: int = 20):
        self.max_history = max(1, max_history)
        self._histories: dict[str, list[Message]] = defaultdict(list)

    def get_messages(self, session_id: str) -> list[Message]:
        """Return system instructions and recent conversation history."""
        history = self._histories[session_id]

        # Keep only the latest user/assistant messages.
        recent_history = history[-self.max_history * 2:]

        return [
            Message(role="system", content=get_system_prompt()),
            *recent_history,
        ]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        """Add a user or assistant message to a conversation."""
        if role not in {"user", "assistant"}:
            raise ValueError("Only user and assistant messages can be stored.")

        history = self._histories[session_id]
        history.append(Message(role=role, content=content))

        # Bound memory usage for this initial implementation.
        del history[:-self.max_history * 2]

    def clear(self, session_id: str) -> None:
        """Clear a specific conversation."""
        self._histories.pop(session_id, None)

    def clear_all(self) -> None:
        """Clear all conversations."""
        self._histories.clear()
