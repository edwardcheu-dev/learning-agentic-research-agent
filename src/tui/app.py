"""Main Textual application for the research assistant TUI."""

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Input


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

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ScrollableContainer(id="conversation")
        yield Input(placeholder="Type your question...")
        yield Footer()
