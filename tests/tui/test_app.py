"""Tests for the main Textual application."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.tui.app import ResearchAssistantApp


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

    @patch("src.tui.app.create_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_input_submission_calls_agent_and_displays_result(
        self, mock_agent_class, mock_create_client
    ):
        """Test that submitting input calls agent.run() and displays the result."""
        # Mock client and async agent
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_agent = AsyncMock()
        mock_agent.run = AsyncMock(return_value="This is the agent's answer.")
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

            # Verify agent.run was called with the query
            mock_agent.run.assert_called_once_with("What is machine learning?")

            # Verify QueryDisplay was added to conversation
            query_displays = app.query("#conversation QueryDisplay")
            assert len(query_displays) == 1

            # Verify ResponseDisplay was added to conversation
            response_displays = app.query("#conversation ResponseDisplay")
            assert len(response_displays) == 1

    @patch("src.tui.app.create_client")
    @patch("src.tui.app.AsyncAgent")
    async def test_app_uses_async_agent(
        self, mock_async_agent_class, mock_create_client
    ):
        """Test that the app can use AsyncAgent instead of Agent."""
        # Mock client and async agent
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_agent = AsyncMock()
        mock_agent.run = AsyncMock(return_value="Async agent response.")
        mock_async_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test():
            # Get input widget
            input_widget = app.query_one("Input")

            # Manually trigger input submission event
            from textual.widgets import Input

            event = Input.Submitted(input_widget, value="Test query")
            await app.on_input_submitted(event)

            # Verify agent.run was called with the query
            mock_agent.run.assert_called_once_with("Test query")

            # Verify displays were added
            query_displays = app.query("#conversation QueryDisplay")
            assert len(query_displays) == 1
            response_displays = app.query("#conversation ResponseDisplay")
            assert len(response_displays) == 1
