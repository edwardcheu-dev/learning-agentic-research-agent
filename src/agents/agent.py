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

    def _build_system_prompt(self) -> str:
        """Build the system prompt with ReAct instructions and tool descriptions.

        Returns:
            System prompt string with ReAct format and available tools
        """
        tool_descriptions = "\n".join(
            f"- {tool.name}: {tool.description}" for tool in self.tools
        )

        return f"""You are a ReAct (Reasoning and Acting) agent.

Answer the user's question by following this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name: input]
Observation: [Result from the tool]
... (repeat Thought/Action/Observation as needed)
Answer: [Final answer to the user's question]

Available tools:
{tool_descriptions}

Always start with a Thought, then take an Action, wait for the Observation, and repeat until you can provide a final Answer.
"""
