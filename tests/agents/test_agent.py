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


def test_format_observation_with_label():
    """Agent should format observations with 'Observation:' label."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    result = "Some tool result here"
    formatted = agent._format_observation(result)

    assert formatted.startswith("Observation:")
    assert "Some tool result here" in formatted


def test_agent_runs_single_iteration():
    """Agent should run one iteration: send prompt, parse action, execute tool."""
    mock_client = Mock()

    # Mock LLM response with Thought and Action
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        "Thought: I should search for information\n"
        "Action: search_web: python tutorials"
    )
    mock_client.chat.completions.create.return_value = mock_response

    agent = Agent(client=mock_client, max_iterations=3)
    result = agent.run("Find me python tutorials")

    # Verify LLM was called
    assert mock_client.chat.completions.create.called

    # Verify result contains observation from tool execution
    assert "Observation:" in result
    assert "MOCK SEARCH RESULTS" in result
    assert "python tutorials" in result


def test_agent_respects_max_iterations():
    """Agent should stop after max_iterations even without final answer."""
    mock_client = Mock()

    # Mock LLM to always return actions (never final answer)
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        "Thought: Keep searching\n" "Action: search_web: more info"
    )
    mock_client.chat.completions.create.return_value = mock_response

    agent = Agent(client=mock_client, max_iterations=2)
    result = agent.run("Test query")

    # Verify LLM was called exactly max_iterations times
    assert mock_client.chat.completions.create.call_count == 2

    # Verify result contains observations from both iterations
    observation_count = result.count("Observation:")
    assert observation_count == 2
