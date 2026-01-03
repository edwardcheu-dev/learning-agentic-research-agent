"""Tests for TUI widgets."""

import pytest
from textual.app import App

from src.tui.widgets import QueryDisplay, ResponseDisplay


class TestQueryDisplay:
    """Test the QueryDisplay widget."""

    async def test_query_display_renders_user_query(self):
        """Test that QueryDisplay renders the user query."""

        class TestApp(App):
            """Test app to host QueryDisplay."""

            def compose(self):
                yield QueryDisplay("What is machine learning?")

        app = TestApp()
        async with app.run_test():
            query_display = app.query_one(QueryDisplay)
            assert query_display is not None
            # Check that the query text is in the widget's rendered output
            assert "What is machine learning?" in query_display.renderable


class TestResponseDisplay:
    """Test the ResponseDisplay widget."""

    async def test_response_display_renders_response(self):
        """Test that ResponseDisplay renders the agent's response."""

        class TestApp(App):
            """Test app to host ResponseDisplay."""

            def compose(self):
                yield ResponseDisplay("Machine learning is a branch of AI...")

        app = TestApp()
        async with app.run_test():
            response_display = app.query_one(ResponseDisplay)
            assert response_display is not None
            # Check that the response text is in the widget's rendered output
            assert "Machine learning is a branch of AI..." in response_display.renderable
