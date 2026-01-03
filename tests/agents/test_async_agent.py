"""Tests for AsyncAgent class."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.agents.async_agent import AsyncAgent


@pytest.mark.asyncio
async def test_async_agent_initialization():
    """Test that AsyncAgent initializes with same parameters as Agent."""
    client = Mock()
    max_iterations = 5

    agent = AsyncAgent(client=client, max_iterations=max_iterations)

    assert agent.client == client
    assert agent.max_iterations == max_iterations
    assert len(agent.tools) > 0  # Should fetch tools from get_all_tools()


@pytest.mark.asyncio
async def test_async_agent_run_returns_conversation():
    """AsyncAgent.run() should return conversation with ReAct steps."""
    mock_client = AsyncMock()

    # Mock LLM response with Thought and Action
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[
        0
    ].message.content = (
        "Thought: I should search for information\nAction: search_web: python tutorials"
    )
    mock_client.chat.completions.create.return_value = mock_response

    agent = AsyncAgent(client=mock_client, max_iterations=3)
    result = await agent.run("Find me python tutorials")

    # Verify LLM was called
    assert mock_client.chat.completions.create.called

    # Verify result contains observation from tool execution
    assert "Observation:" in result
    assert "MOCK SEARCH RESULTS" in result
    assert "python tutorials" in result
