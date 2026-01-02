"""Tool interface and placeholder implementations for Phase 1."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    """Represents a tool the agent can use."""

    name: str
    description: str
    function: Callable[[str], str]
