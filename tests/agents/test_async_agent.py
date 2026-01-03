"""Tests for AsyncAgent class."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.agents.async_agent import AsyncAgent
from src.tui.events import AgentEvent


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


@pytest.mark.asyncio
async def test_async_agent_run_streaming_yields_agent_events():
    """AsyncAgent.run_streaming() should yield AgentEvent for each token."""
    mock_client = AsyncMock()

    # Mock streaming response with multiple chunks
    async def mock_stream_iter():
        """Async generator that yields streaming chunks."""
        # Token chunks
        yield Mock(choices=[Mock(delta=Mock(content="Hello"))])
        yield Mock(choices=[Mock(delta=Mock(content=" world"))])
        yield Mock(choices=[Mock(delta=Mock(content="!"))])

    # Mock the streaming response
    mock_streaming_response = mock_stream_iter()
    mock_client.chat.completions.create.return_value = mock_streaming_response

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events from streaming
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Verify we received AgentEvent objects
    assert all(isinstance(event, AgentEvent) for event in events)

    # Verify we got token events
    token_events = [e for e in events if e.type == "token"]
    assert len(token_events) > 0

    # Verify token content matches streaming chunks
    token_contents = [e.content for e in token_events]
    assert "Hello" in token_contents
    assert " world" in token_contents
    assert "!" in token_contents
