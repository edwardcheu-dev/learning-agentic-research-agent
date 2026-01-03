"""Tests for the main Textual application."""

from unittest.mock import Mock, patch

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
    @patch("src.tui.app.Agent")
    async def test_input_submission_calls_agent_and_displays_result(
        self, mock_agent_class, mock_create_client
    ):
        """Test that submitting input calls agent.run() and displays the result."""
        # Mock client and agent
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_agent = Mock()
        mock_agent.run = Mock(return_value="This is the agent's answer.")
        mock_agent_class.return_value = mock_agent

        app = ResearchAssistantApp()
        async with app.run_test() as pilot:
            # Verify app initialized with agent
            assert app.agent is not None

            # Type a question into the input field
            input_widget = app.query_one("Input")
            input_widget.value = "What is machine learning?"

            # Submit the input
            await pilot.press("enter")

            # Wait for UI to update
            await pilot.pause()

            # Verify agent.run was called with the query
            mock_agent.run.assert_called_once_with("What is machine learning?")

            # Verify QueryDisplay was added to conversation
            query_displays = app.query("#conversation QueryDisplay")
            assert len(query_displays) == 1

            # Verify ResponseDisplay was added to conversation
            response_displays = app.query("#conversation ResponseDisplay")
            assert len(response_displays) == 1
