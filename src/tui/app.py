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

        # Clear the input field
        input_widget = self.query_one(Input)
        input_widget.value = ""

        # Get conversation container
        conversation = self.query_one("#conversation")

        # Display user query
        conversation.mount(QueryDisplay(query))

        # Create streaming text widget for tokens
        streaming_widget = StreamingText()
        conversation.mount(streaming_widget)

        # Stream agent response token by token
        async for agent_event in self.agent.run_streaming(query):
            if agent_event.type == "token":
                streaming_widget.append_token(agent_event.content)
            elif agent_event.type == "thought":
                # Extract and preserve Answer text before clearing
                current_text = streaming_widget._content
                answer_text = ""
                if "Answer:" in current_text:
                    # Find the Answer section and preserve it
                    answer_index = current_text.find("Answer:")
                    answer_text = current_text[answer_index:]

                # Clear streaming widget to hide raw Thought/Action text
                streaming_widget.clear()

                # Restore Answer text if found
                if answer_text:
                    streaming_widget.append_token(answer_text)

                # Create ThoughtNode for thought events
                thought_node = ThoughtNode(agent_event.content, status="done")
                conversation.mount(thought_node)
            elif agent_event.type == "action":
                # Create ActionNode for action events
                tool_name = agent_event.metadata.get("tool_name", "unknown")
                tool_input = agent_event.metadata.get("tool_input", "")
                action_node = ActionNode(tool_name, tool_input, status="done")
                conversation.mount(action_node)
            elif agent_event.type == "observation":
                # Create ObservationNode for observation events
                observation_node = ObservationNode(agent_event.content, status="done")
                conversation.mount(observation_node)
