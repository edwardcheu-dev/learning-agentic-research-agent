"""Tests for TUI widgets."""

from textual.app import App

from src.tui.widgets import (
    ActionNode,
    ObservationNode,
    QueryDisplay,
    ResponseDisplay,
    StreamingText,
    ThoughtNode,
)


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


class TestThoughtNode:
    """Test the ThoughtNode widget."""

    async def test_thought_node_displays_content_and_status(self):
        """Test that ThoughtNode displays content with a status indicator."""

        class TestApp(App):
            """Test app to host ThoughtNode."""

            def compose(self):
                yield ThoughtNode("I need to search for information", status="running")

        app = TestApp()
        async with app.run_test():
            thought_node = app.query_one(ThoughtNode)
            assert thought_node is not None

            # Check that the thought content is displayed
            rendered = str(thought_node.render())
            assert "I need to search for information" in rendered

            # Check that status indicator is present (running state)
            assert "running" in rendered.lower() or "⋯" in rendered or "●" in rendered

    async def test_thought_node_status_pending(self):
        """Test that ThoughtNode shows pending status indicator."""

        class TestApp(App):
            """Test app to host ThoughtNode."""

            def compose(self):
                yield ThoughtNode("Waiting to process", status="pending")

        app = TestApp()
        async with app.run_test():
            thought_node = app.query_one(ThoughtNode)
            rendered = str(thought_node.render())

            # Check for pending indicator
            assert "pending" in rendered.lower() or "○" in rendered or "⊙" in rendered

    async def test_thought_node_status_done(self):
        """Test that ThoughtNode shows done status indicator."""

        class TestApp(App):
            """Test app to host ThoughtNode."""

            def compose(self):
                yield ThoughtNode("Analysis complete", status="done")

        app = TestApp()
        async with app.run_test():
            thought_node = app.query_one(ThoughtNode)
            rendered = str(thought_node.render())

            # Check for done indicator
            assert "done" in rendered.lower() or "✓" in rendered or "●" in rendered


class TestActionNode:
    """Test the ActionNode widget."""

    async def test_action_node_displays_tool_name_and_input(self):
        """Test that ActionNode displays the tool name and input."""

        class TestApp(App):
            """Test app to host ActionNode."""

            def compose(self):
                yield ActionNode(
                    tool_name="search_web",
                    tool_input="latest AI news",
                    status="running",
                )

        app = TestApp()
        async with app.run_test():
            action_node = app.query_one(ActionNode)
            assert action_node is not None

            rendered = str(action_node.render())
            # Check that tool name and input are displayed
            assert "search_web" in rendered
            assert "latest AI news" in rendered
            assert "Action" in rendered or "action" in rendered

    async def test_action_node_status_pending(self):
        """Test that ActionNode shows pending status indicator."""

        class TestApp(App):
            """Test app to host ActionNode."""

            def compose(self):
                yield ActionNode(
                    tool_name="save_note", tool_input="test note", status="pending"
                )

        app = TestApp()
        async with app.run_test():
            action_node = app.query_one(ActionNode)
            rendered = str(action_node.render())

            # Check for pending indicator
            assert "pending" in rendered.lower() or "○" in rendered or "⊙" in rendered

    async def test_action_node_status_done(self):
        """Test that ActionNode shows done status indicator."""

        class TestApp(App):
            """Test app to host ActionNode."""

            def compose(self):
                yield ActionNode(
                    tool_name="search_web", tool_input="query", status="done"
                )

        app = TestApp()
        async with app.run_test():
            action_node = app.query_one(ActionNode)
            rendered = str(action_node.render())

            # Check for done indicator
            assert "done" in rendered.lower() or "✓" in rendered or "●" in rendered


class TestObservationNode:
    """Test the ObservationNode widget."""

    async def test_observation_node_displays_result(self):
        """Test that ObservationNode displays the observation result."""

        class TestApp(App):
            """Test app to host ObservationNode."""

            def compose(self):
                yield ObservationNode(
                    "Search results: Found 5 articles about AI", status="done"
                )

        app = TestApp()
        async with app.run_test():
            observation_node = app.query_one(ObservationNode)
            assert observation_node is not None

            rendered = str(observation_node.render())
            # Check that the observation result is displayed
            assert "Search results: Found 5 articles about AI" in rendered
            assert "Observation" in rendered or "observation" in rendered

    async def test_observation_node_status_running(self):
        """Test that ObservationNode shows running status indicator."""

        class TestApp(App):
            """Test app to host ObservationNode."""

            def compose(self):
                yield ObservationNode("Processing...", status="running")

        app = TestApp()
        async with app.run_test():
            observation_node = app.query_one(ObservationNode)
            rendered = str(observation_node.render())

            # Check for running indicator
            assert "running" in rendered.lower() or "●" in rendered or "⋯" in rendered

    async def test_observation_node_status_done(self):
        """Test that ObservationNode shows done status indicator."""

        class TestApp(App):
            """Test app to host ObservationNode."""

            def compose(self):
                yield ObservationNode("Completed successfully", status="done")

        app = TestApp()
        async with app.run_test():
            observation_node = app.query_one(ObservationNode)
            rendered = str(observation_node.render())

            # Check for done indicator
            assert "done" in rendered.lower() or "✓" in rendered or "●" in rendered
