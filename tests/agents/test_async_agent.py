"""Tests for AsyncAgent class."""

from unittest.mock import Mock

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
