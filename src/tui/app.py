"""Main Textual application for the research assistant TUI."""

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Input

from src.agents.async_agent import AsyncAgent
from src.client import create_async_client
from src.config import DEFAULT_MAX_ITERATIONS
from src.tui.widgets import QueryDisplay, StreamingText


class ResearchAssistantApp(App):
    """Main TUI application for the research assistant.

    Provides a terminal-based user interface with:
    - Header with keyboard shortcut hints
    - Scrollable conversation area
    - Input field for user queries
    - Footer with status information
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        """Initialize the TUI app with async agent."""
        super().__init__()
        # Create async OpenAI client and async agent
        client = create_async_client()
        self.agent = AsyncAgent(client=client, max_iterations=DEFAULT_MAX_ITERATIONS)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ScrollableContainer(id="conversation")
        yield Input(placeholder="Type your question...")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission with streaming (async).

        Args:
            event: Input submission event containing the user's query.
        """
        query = event.value
        if not query.strip():
            return

        # Clear the input field
        input_widget = self.query_one(Input)
        input_widget.value = ""

        # Get conversation container
        conversation = self.query_one("#conversation")

        # Display user query
        conversation.mount(QueryDisplay(query))

        # Create streaming text widget
        streaming_widget = StreamingText()
        conversation.mount(streaming_widget)

        # Stream agent response token by token
        async for agent_event in self.agent.run_streaming(query):
            if agent_event.type == "token":
                streaming_widget.append_token(agent_event.content)
