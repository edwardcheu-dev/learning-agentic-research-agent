"""Main Textual application for the research assistant TUI."""

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Input

from src.agents.agent import Agent
from src.client import create_client
from src.config import DEFAULT_MAX_ITERATIONS
from src.tui.widgets import QueryDisplay, ResponseDisplay


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
        """Initialize the TUI app with agent."""
        super().__init__()
        # Create OpenAI client and agent
        client = create_client()
        self.agent = Agent(client=client, max_iterations=DEFAULT_MAX_ITERATIONS)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ScrollableContainer(id="conversation")
        yield Input(placeholder="Type your question...")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission.

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

        # Run agent and display response
        response = self.agent.run(query)
        conversation.mount(ResponseDisplay(response))
