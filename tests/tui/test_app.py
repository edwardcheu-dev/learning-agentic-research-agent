"""Tests for the main Textual application."""

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
