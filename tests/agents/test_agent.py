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
