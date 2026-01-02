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

    def _parse_action(self, response: str) -> tuple[str, str] | None:
        """Parse action from LLM response.

        Args:
            response: LLM response text

        Returns:
            Tuple of (tool_name, tool_input) if action found, None otherwise
        """
        # Look for "Action: " in the response
        if "Action:" not in response:
            return None

        # Extract the action line
        for line in response.split("\n"):
            if line.strip().startswith("Action:"):
                # Remove "Action: " prefix
                action_text = line.strip()[7:].strip()

                # Split on first ":" to separate tool_name from input
                if ":" in action_text:
                    tool_name, tool_input = action_text.split(":", 1)
                    return (tool_name.strip(), tool_input.strip())

        return None

    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool by name with the given input.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Input string to pass to the tool

        Returns:
            Result string from the tool execution

        Raises:
            ValueError: If tool_name is not found
        """
        # Find the tool by name
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.function(tool_input)

        # Tool not found
        raise ValueError(f"Unknown tool: {tool_name}")
