"""Tests for placeholder tool implementations."""

from src.agents.tools import Tool, get_save_note_tool, get_search_web_tool


def test_placeholder():
    """Verify pytest is working."""
    assert True


def test_tool_has_name_and_description():
    """Tools must have name, description, and callable function."""
    tool = Tool(
        name="test_tool", description="A test tool", function=lambda x: x
    )
    assert tool.name == "test_tool"
    assert tool.description == "A test tool"
    assert callable(tool.function)


def test_search_web_tool_returns_mock_results():
    """search_web tool returns placeholder search results."""
    tool = get_search_web_tool()
    result = tool.function("python tutorials")

    assert "MOCK SEARCH RESULTS" in result
    assert "python tutorials" in result
    assert tool.name == "search_web"
    assert "search" in tool.description.lower()


def test_save_note_tool_returns_confirmation():
    """save_note tool returns confirmation message."""
    tool = get_save_note_tool()
    result = tool.function("title: test\ncontent: hello")

    assert "MOCK SAVE" in result
    assert "test" in result
    assert tool.name == "save_note"
