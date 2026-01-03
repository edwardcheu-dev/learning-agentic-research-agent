"""Async ReAct agent implementation."""

from typing import Any

from src.agents.tools import Tool, get_all_tools


class AsyncAgent:
    """An async ReAct-style reasoning agent."""

    client: Any
    max_iterations: int
    tools: list[Tool]

    def __init__(self, client: Any, max_iterations: int) -> None:
        """Initialize the async agent.

        Args:
            client: OpenAI client for LLM calls
            max_iterations: Maximum number of reasoning iterations
        """
        self.client = client
        self.max_iterations = max_iterations
        self.tools = get_all_tools()
