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
