"""Tests for the basic ReAct agent."""

from unittest.mock import Mock

from src.agents.agent import Agent


def test_agent_initializes_with_client():
    """Agent should initialize with OpenAI client and tools."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    assert agent.client == mock_client
    assert agent.max_iterations == 3
    assert len(agent.tools) == 2  # search_web and save_note


def test_agent_builds_system_prompt_with_react_instructions():
    """Agent should build system prompt with ReAct format and tool descriptions."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    prompt = agent._build_system_prompt()

    # Check it's a string
    assert isinstance(prompt, str)

    # Check for ReAct-style keywords
    assert "Thought:" in prompt
    assert "Action:" in prompt
    assert "Observation:" in prompt
    assert "Answer:" in prompt

    # Check for tool descriptions
    assert "search_web" in prompt
    assert "save_note" in prompt


def test_parse_action_extracts_tool_name_and_input():
    """Parser should extract tool name and input from Action line."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    # Test basic action format
    response = "Thought: I need to search\nAction: search_web: python tutorials"
    result = agent._parse_action(response)

    assert result is not None
    tool_name, tool_input = result
    assert tool_name == "search_web"
    assert tool_input == "python tutorials"


def test_parse_action_returns_none_when_no_action():
    """Parser should return None if no Action found."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    # Test response with no action
    response = "Thought: I'm still thinking about this"
    result = agent._parse_action(response)

    assert result is None


def test_execute_tool_by_name():
    """Agent should execute tool by name with given input."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    # Execute search_web tool
    result = agent._execute_tool("search_web", "python tutorials")

    assert "MOCK SEARCH RESULTS" in result
    assert "python tutorials" in result


def test_execute_unknown_tool_raises_error():
    """Agent should raise ValueError for unknown tool names."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    # Try to execute non-existent tool
    try:
        agent._execute_tool("nonexistent_tool", "some input")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown tool" in str(e)
        assert "nonexistent_tool" in str(e)
