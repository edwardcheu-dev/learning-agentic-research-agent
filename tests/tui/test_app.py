"""Tests for the main Textual application."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.tui.app import ResearchAssistantApp
from src.tui.events import AgentEvent


class TestResearchAssistantApp:
    """Test the main TUI application."""

    @pytest.mark.asyncio
    async def test_app_renders_with_basic_layout(self):
        """Test that the app renders with header, input, and conversation area."""
        app = ResearchAssistantApp()
        async with app.run_test():
            # Verify app started successfully
            assert app.is_running

            # Verify header is present
            header = app.query_one("Header")
            assert header is not None

            # Verify input area is present
            input_widget = app.query_one("Input")
            assert input_widget is not None
            assert input_widget.placeholder == "Type your question..."

            # Verify conversation container is present
            conversation = app.query_one("#conversation")
            assert conversation is not None

    @patch("src.tui.app.create_async_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_input_submission_calls_agent_and_displays_result(
        self, mock_agent_class, mock_create_async_client
    ):
        """Test that submitting input calls agent.run_streaming()."""
        # Mock async client and async agent
        mock_client = Mock()
        mock_create_async_client.return_value = mock_client

        # Create async generator for streaming events
        async def mock_streaming_events(query):
            yield AgentEvent(type="token", content="This is the agent's answer.")

        mock_agent = AsyncMock()
        mock_agent.run_streaming = mock_streaming_events
        mock_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            # Verify app initialized with agent
            assert app.agent is not None

            # Get input widget
            input_widget = app.query_one("Input")

            # Manually trigger input submission event
            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="What is machine learning?")
            await app.on_input_submitted(event)

            # Verify QueryDisplay was added to conversation
            query_displays = app.query("#conversation QueryDisplay")
            assert len(query_displays) == 1

            # Verify StreamingText was added to conversation
            streaming_widgets = app.query("#conversation StreamingText")
            assert len(streaming_widgets) == 1

    @patch("src.tui.app.create_async_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_app_uses_async_agent(
        self, mock_async_agent_class, mock_create_async_client
    ):
        """Test that the app can use AsyncAgent with streaming."""
        # Mock async client and async agent
        mock_client = Mock()
        mock_create_async_client.return_value = mock_client

        # Create async generator for streaming events
        async def mock_streaming_events(query):
            yield AgentEvent(type="token", content="Async agent response.")

        mock_agent = AsyncMock()
        mock_agent.run_streaming = mock_streaming_events
        mock_async_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            # Get input widget
            input_widget = app.query_one("Input")

            # Manually trigger input submission event
            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="Test query")
            await app.on_input_submitted(event)

            # Verify displays were added
            query_displays = app.query("#conversation QueryDisplay")
            assert len(query_displays) == 1
            streaming_widgets = app.query("#conversation StreamingText")
            assert len(streaming_widgets) == 1

    @patch("src.tui.app.create_async_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_app_processes_streaming_events(
        self, mock_agent_class, mock_create_async_client
    ):
        """Test that the app processes AgentEvent stream and updates StreamingText."""
        # Mock async client and async agent
        mock_client = Mock()
        mock_create_async_client.return_value = mock_client

        # Create async generator for streaming events
        async def mock_streaming_events(query):
            yield AgentEvent(type="token", content="Hello")
            yield AgentEvent(type="token", content=" world")
            yield AgentEvent(type="token", content="!")

        mock_agent = AsyncMock()
        # Make run_streaming directly return the async generator
        mock_agent.run_streaming = mock_streaming_events
        mock_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            # Get input widget
            input_widget = app.query_one("Input")

            # Manually trigger input submission event
            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="Test streaming")
            await app.on_input_submitted(event)

            # Verify StreamingText widget was mounted
            streaming_widgets = app.query("#conversation StreamingText")
            assert len(streaming_widgets) > 0

            # Verify the streaming widget received the tokens
            streaming_widget = streaming_widgets[0]
            rendered = str(streaming_widget.render())
            assert "Hello world!" in rendered

    @patch("src.tui.app.create_async_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_app_creates_thought_node_on_thought_event(
        self, mock_agent_class, mock_create_async_client
    ):
        """Test that the app creates ThoughtNode when receiving thought event."""
        # Mock async client and async agent
        mock_client = Mock()
        mock_create_async_client.return_value = mock_client

        # Create async generator with thought event
        async def mock_streaming_with_thought(query):
            yield AgentEvent(type="thought", content="I should search for info")

        mock_agent = AsyncMock()
        mock_agent.run_streaming = mock_streaming_with_thought
        mock_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            input_widget = app.query_one("Input")

            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="Test query")
            await app.on_input_submitted(event)

            # Verify ThoughtNode was created
            thought_nodes = app.query("#conversation ThoughtNode")
            assert len(thought_nodes) > 0, "Should create ThoughtNode for thought event"

    @patch("src.tui.app.create_async_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_app_creates_action_node_on_action_event(
        self, mock_agent_class, mock_create_async_client
    ):
        """Test that the app creates ActionNode when receiving action event."""
        # Mock async client and async agent
        mock_client = Mock()
        mock_create_async_client.return_value = mock_client

        # Create async generator with action event
        async def mock_streaming_with_action(query):
            yield AgentEvent(
                type="action",
                content="search_web(python)",
                metadata={"tool_name": "search_web", "tool_input": "python"},
            )

        mock_agent = AsyncMock()
        mock_agent.run_streaming = mock_streaming_with_action
        mock_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            input_widget = app.query_one("Input")

            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="Test query")
            await app.on_input_submitted(event)

            # Verify ActionNode was created
            action_nodes = app.query("#conversation ActionNode")
            assert len(action_nodes) > 0, "Should create ActionNode for action event"

    @patch("src.tui.app.create_async_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_app_creates_observation_node_on_observation_event(
        self, mock_agent_class, mock_create_async_client
    ):
        """Test that the app creates ObservationNode for observation event."""
        # Mock async client and async agent
        mock_client = Mock()
        mock_create_async_client.return_value = mock_client

        # Create async generator with observation event
        async def mock_streaming_with_observation(query):
            yield AgentEvent(
                type="observation", content="Observation: Search results found"
            )

        mock_agent = AsyncMock()
        mock_agent.run_streaming = mock_streaming_with_observation
        mock_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            input_widget = app.query_one("Input")

            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="Test query")
            await app.on_input_submitted(event)

            # Verify ObservationNode was created
            observation_nodes = app.query("#conversation ObservationNode")
            assert len(observation_nodes) > 0, (
                "Should create ObservationNode for observation event"
            )
