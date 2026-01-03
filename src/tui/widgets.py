"""Custom widgets for the TUI."""

from textual.widgets import Static


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
