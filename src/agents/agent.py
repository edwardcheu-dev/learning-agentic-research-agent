"""Basic ReAct agent implementation."""

from src.agents.tools import get_all_tools


class Agent:
    """A ReAct-style reasoning agent."""

    def __init__(self, client, max_iterations: int):
        """Initialize the agent.

        Args:
            client: OpenAI client for LLM calls
            max_iterations: Maximum number of reasoning iterations
        """
        self.client = client
        self.max_iterations = max_iterations
        self.tools = get_all_tools()
