"""Main Textual application for the research assistant TUI."""

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Input

from src.agents.async_agent import AsyncAgent
from src.client import create_async_client
from src.config import DEFAULT_MAX_ITERATIONS
from src.tui.widgets import (
    ActionNode,
    ObservationNode,
    QueryDisplay,
    StreamingText,
    ThoughtNode,
)


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

        # Prevent event bubbling to avoid duplicate handler calls
        event.stop()

        # Clear the input field
        input_widget = self.query_one(Input)
        input_widget.value = ""

        # Get conversation container
        conversation = self.query_one("#conversation")

        # Display user query
        conversation.mount(QueryDisplay(query))

        # Track streaming widget - only create it when needed for Answer
        streaming_widget = None
        answer_detected = False

        # Stream agent response token by token
        async for agent_event in self.agent.run_streaming(query):
            if agent_event.type == "token":
                # Check if this token contains "Answer:" to detect final answer phase
                if not answer_detected and "Answer:" in agent_event.content:
                    answer_detected = True
                    # Create and mount StreamingText widget at this point (after nodes)
                    streaming_widget = StreamingText()
                    conversation.mount(streaming_widget)

                # Only append tokens if we're in the answer phase
                if answer_detected and streaming_widget:
                    streaming_widget.append_token(agent_event.content)
            elif agent_event.type == "thought":
                # Create ThoughtNode for thought events
                thought_node = ThoughtNode(agent_event.content, status="done")
                conversation.mount(thought_node)
            elif agent_event.type == "action":
                # Skip ActionNode for "Answer" (shown in StreamingText instead)
                tool_name = agent_event.metadata.get("tool_name", "unknown")
                if tool_name == "Answer":
                    continue

                # Create ActionNode for actual tool actions
                tool_input = agent_event.metadata.get("tool_input", "")
                action_node = ActionNode(tool_name, tool_input, status="done")
                conversation.mount(action_node)
            elif agent_event.type == "observation":
                # Create ObservationNode for observation events
                observation_node = ObservationNode(agent_event.content, status="done")
                conversation.mount(observation_node)
