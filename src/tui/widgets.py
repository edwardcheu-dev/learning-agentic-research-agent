"""Custom widgets for the TUI."""

from typing import Literal

from textual.widgets import Static

StatusType = Literal["pending", "running", "done"]


class QueryDisplay(Static):
    """Widget to display user queries.

    Renders user queries with styling to differentiate from agent responses.
    """

    def __init__(self, query: str) -> None:
        """Initialize QueryDisplay with a query string.

        Args:
            query: The user's query to display.
        """
        super().__init__(f"[bold cyan]You:[/bold cyan] {query}")


class ResponseDisplay(Static):
    """Widget to display agent responses.

    Renders agent responses with styling to differentiate from user queries.
    """

    def __init__(self, response: str) -> None:
        """Initialize ResponseDisplay with a response string.

        Args:
            response: The agent's response to display.
        """
        super().__init__(f"[bold green]Agent:[/bold green] {response}")


class StreamingText(Static):
    """Widget that displays text incrementally as tokens arrive.

    Used to show LLM responses being generated in real-time, character-by-character.
    """

    def __init__(self) -> None:
        """Initialize StreamingText with empty content."""
        super().__init__("")
        self._content = ""

    def append_token(self, token: str) -> None:
        """Append a token to the streaming text.

        Args:
            token: The text token to append
        """
        self._content += token
        self.update(self._content)


class ThoughtNode(Static):
    """Widget to display agent reasoning steps with status indicators.

    Shows the agent's thought process with visual status indicators
    (pending, running, done) to track progress through the ReAct loop.
    """

    STATUS_SYMBOLS = {
        "pending": "○",  # Hollow circle
        "running": "●",  # Filled circle
        "done": "✓",  # Checkmark
    }

    STATUS_COLORS = {
        "pending": "dim",
        "running": "yellow",
        "done": "green",
    }

    def __init__(self, content: str, status: StatusType = "pending") -> None:
        """Initialize ThoughtNode with content and status.

        Args:
            content: The thought content to display
            status: The status indicator (pending, running, or done)
        """
        symbol = self.STATUS_SYMBOLS[status]
        color = self.STATUS_COLORS[status]
        formatted = f"[{color}]{symbol}[/{color}] [bold]Thought:[/bold] {content}"
        super().__init__(formatted)
        self._content_text = content
        self._status = status


class ActionNode(Static):
    """Widget to display agent actions with tool name and input.

    Shows the tool being executed along with its input parameters,
    with visual status indicators to track execution progress.
    """

    STATUS_SYMBOLS = {
        "pending": "○",  # Hollow circle
        "running": "●",  # Filled circle
        "done": "✓",  # Checkmark
    }

    STATUS_COLORS = {
        "pending": "dim",
        "running": "yellow",
        "done": "green",
    }

    def __init__(
        self, tool_name: str, tool_input: str, status: StatusType = "pending"
    ) -> None:
        """Initialize ActionNode with tool name, input, and status.

        Args:
            tool_name: The name of the tool being executed
            tool_input: The input/arguments for the tool
            status: The status indicator (pending, running, or done)
        """
        symbol = self.STATUS_SYMBOLS[status]
        color = self.STATUS_COLORS[status]
        formatted = (
            f"[{color}]{symbol}[/{color}] [bold]Action:[/bold] "
            f"{tool_name}({tool_input})"
        )
        super().__init__(formatted)
        self._tool_name = tool_name
        self._tool_input = tool_input
        self._status = status


class ObservationNode(Static):
    """Widget to display tool execution results.

    Shows the observation/result from tool execution with visual
    status indicators to track processing progress.
    """

    STATUS_SYMBOLS = {
        "pending": "○",  # Hollow circle
        "running": "●",  # Filled circle
        "done": "✓",  # Checkmark
    }

    STATUS_COLORS = {
        "pending": "dim",
        "running": "yellow",
        "done": "green",
    }

    def __init__(self, result: str, status: StatusType = "pending") -> None:
        """Initialize ObservationNode with result and status.

        Args:
            result: The observation/result to display
            status: The status indicator (pending, running, or done)
        """
        symbol = self.STATUS_SYMBOLS[status]
        color = self.STATUS_COLORS[status]
        formatted = f"[{color}]{symbol}[/{color}] [bold]Observation:[/bold] {result}"
        super().__init__(formatted)
        self._result = result
        self._status = status
