"""Tests for placeholder tool implementations."""

from src.agents.tools import Tool


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
