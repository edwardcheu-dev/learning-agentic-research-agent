"""Tests for TUI widgets."""

from textual.app import App

from src.tui.widgets import QueryDisplay, ResponseDisplay, StreamingText


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
            # Static widget stores content in renderable which is a Rich renderable
            rendered = str(query_display.render())
            assert "What is machine learning?" in rendered


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
            # Static widget stores content in renderable which is a Rich renderable
            rendered = str(response_display.render())
            assert "Machine learning is a branch of AI..." in rendered


class TestStreamingText:
    """Test the StreamingText widget."""

    async def test_streaming_text_appends_tokens_incrementally(self):
        """Test that StreamingText appends tokens one by one."""

        class TestApp(App):
            """Test app to host StreamingText."""

            def compose(self):
                yield StreamingText()

        app = TestApp()
        async with app.run_test():
            streaming_text = app.query_one(StreamingText)

            # Initially empty
            rendered = str(streaming_text.render())
            assert rendered == ""

            # Append first token
            streaming_text.append_token("Hello")
            rendered = str(streaming_text.render())
            assert "Hello" in rendered

            # Append second token
            streaming_text.append_token(" world")
            rendered = str(streaming_text.render())
            assert "Hello world" in rendered

            # Append third token
            streaming_text.append_token("!")
            rendered = str(streaming_text.render())
            assert "Hello world!" in rendered
