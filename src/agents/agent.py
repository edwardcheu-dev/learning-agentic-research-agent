"""Basic ReAct agent implementation."""

from typing import Any

from src.agents.tools import Tool, get_all_tools
from src.config import MODEL_NAME


class Agent:
    """A ReAct-style reasoning agent."""

    client: Any
    max_iterations: int
    tools: list[Tool]

    def __init__(self, client: Any, max_iterations: int) -> None:
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

Always start with a Thought, then take an Action, wait for the Observation,
and repeat until you can provide a final Answer.
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

    def _format_observation(self, result: str) -> str:
        """Format tool result as an observation.

        Args:
            result: Tool execution result

        Returns:
            Formatted observation string with label
        """
        return f"Observation: {result}"

    def run(self, query: str) -> str:
        """Run the agent on a query using ReAct loop.

        Args:
            query: User's question or request

        Returns:
            String containing the conversation history with all reasoning steps
        """
        # Build system prompt
        system_prompt = self._build_system_prompt()

        # Initialize conversation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]

        conversation = f"User: {query}\n\n"

        # ReAct loop
        for iteration in range(self.max_iterations):
            # Call LLM
            response = self.client.chat.completions.create(
                model=MODEL_NAME, messages=messages
            )

            llm_response = response.choices[0].message.content
            conversation += f"{llm_response}\n\n"

            # Parse action
            action = self._parse_action(llm_response)

            # If no action, agent has provided final answer
            if action is None:
                break

            # Execute tool
            tool_name, tool_input = action
            tool_result = self._execute_tool(tool_name, tool_input)

            # Format observation
            observation = self._format_observation(tool_result)
            conversation += f"{observation}\n\n"

            # Add to conversation for next iteration
            messages.append({"role": "assistant", "content": llm_response})
            messages.append({"role": "user", "content": observation})

        return conversation.strip()
