"""Event system for TUI agent communication."""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class AgentEvent:
    """Event emitted by AsyncAgent during streaming execution.

    Used to communicate agent state changes to the TUI for real-time visualization.

    Attributes:
        type: The type of event (thought/action/observation/answer/token)
        content: The content of the event (text, tool name, result, etc.)
        metadata: Additional context (e.g., tool inputs, step numbers)
    """

    type: Literal["thought", "action", "observation", "answer", "token"]
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
