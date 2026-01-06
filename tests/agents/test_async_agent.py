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


@pytest.mark.asyncio
async def test_async_agent_streaming_yields_observation_event():
    """AsyncAgent.run_streaming() yields observation after tool execution."""
    mock_client = AsyncMock()

    # Mock streaming response with Thought and Action
    async def mock_stream_with_action():
        """Async generator that yields action."""
        yield Mock(choices=[Mock(delta=Mock(content="Thought: I should search\n"))])
        yield Mock(choices=[Mock(delta=Mock(content="Action: search_web: test"))])

    # Mock the streaming response
    mock_client.chat.completions.create.return_value = mock_stream_with_action()

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events from streaming
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Verify we received observation event
    observation_events = [e for e in events if e.type == "observation"]
    assert len(observation_events) > 0, "Should yield observation event"

    # Verify observation content
    obs_event = observation_events[0]
    assert "Observation:" in obs_event.content
    assert "MOCK SEARCH RESULTS" in obs_event.content


@pytest.mark.asyncio
async def test_async_agent_streaming_adds_newline_before_observation():
    """AsyncAgent.run_streaming() adds newline before observation."""
    mock_client = AsyncMock()

    # Mock streaming response with Thought and Action
    async def mock_stream_with_action():
        """Async generator that yields action."""
        yield Mock(choices=[Mock(delta=Mock(content="Thought: Search\n"))])
        yield Mock(choices=[Mock(delta=Mock(content="Action: search_web: test"))])

    # Mock the streaming response
    mock_client.chat.completions.create.return_value = mock_stream_with_action()

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events from streaming
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Find the token event just before observation
    event_types = [e.type for e in events]

    # Should have pattern: [...tokens..., "token" with "\n", "observation"]
    # The last token before observation should end with or be a newline
    obs_index = event_types.index("observation")
    token_before_obs = events[obs_index - 1]

    assert token_before_obs.type == "token"
    assert "\n" in token_before_obs.content or token_before_obs.content == "\n"


@pytest.mark.asyncio
async def test_async_agent_streaming_adds_newline_after_observation():
    """AsyncAgent.run_streaming() adds newline after observation."""
    mock_client = AsyncMock()

    # First iteration: Action that triggers tool
    async def mock_stream_first():
        """First LLM call with action."""
        yield Mock(choices=[Mock(delta=Mock(content="Thought: Search\n"))])
        yield Mock(choices=[Mock(delta=Mock(content="Action: search_web: test"))])

    # Second iteration: Final answer (no action)
    async def mock_stream_second():
        """Second LLM call with answer."""
        yield Mock(choices=[Mock(delta=Mock(content="Answer: Result"))])

    # Mock client to return different streams for each call
    call_count = 0

    async def mock_create(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return mock_stream_first()
        else:
            return mock_stream_second()

    mock_client.chat.completions.create = mock_create

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Find observation and the token after it
    event_types = [e.type for e in events]
    obs_index = event_types.index("observation")

    # Next event after observation should be a newline token
    token_after_obs = events[obs_index + 1]
    assert token_after_obs.type == "token"
    assert token_after_obs.content == "\n"


@pytest.mark.asyncio
async def test_async_agent_emits_thought_event():
    """AsyncAgent.run_streaming() should emit a thought event for Thought: sections."""
    mock_client = AsyncMock()

    # Mock streaming response with Thought and Action
    async def mock_stream_with_thought():
        """Async generator that yields thought and action."""
        yield Mock(choices=[Mock(delta=Mock(content="Thought: I"))])
        yield Mock(choices=[Mock(delta=Mock(content=" should search"))])
        yield Mock(choices=[Mock(delta=Mock(content="\nAction: search_web: test"))])

    mock_client.chat.completions.create.return_value = mock_stream_with_thought()

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events from streaming
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Verify we received a thought event
    thought_events = [e for e in events if e.type == "thought"]
    assert len(thought_events) > 0, "Should yield thought event"

    # Verify thought content
    thought_event = thought_events[0]
    assert "should search" in thought_event.content.lower()


@pytest.mark.asyncio
async def test_async_agent_emits_action_event():
    """AsyncAgent.run_streaming() should emit an action event for Action: sections."""
    mock_client = AsyncMock()

    # Mock streaming response with Thought and Action
    async def mock_stream_with_action():
        """Async generator that yields thought and action."""
        yield Mock(choices=[Mock(delta=Mock(content="Thought: Search for info\n"))])
        yield Mock(choices=[Mock(delta=Mock(content="Action: search_web: python"))])

    mock_client.chat.completions.create.return_value = mock_stream_with_action()

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events from streaming
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Verify we received an action event
    action_events = [e for e in events if e.type == "action"]
    assert len(action_events) > 0, "Should yield action event"

    # Verify action metadata
    action_event = action_events[0]
    assert "tool_name" in action_event.metadata
    assert "tool_input" in action_event.metadata
    assert action_event.metadata["tool_name"] == "search_web"
    assert action_event.metadata["tool_input"] == "python"


@pytest.mark.asyncio
async def test_async_agent_emits_events_in_correct_order():
    """AsyncAgent should emit events in order: thought -> action -> observation."""
    mock_client = AsyncMock()

    # Mock streaming response with complete ReAct turn
    async def mock_stream_complete():
        """Async generator that yields a complete turn."""
        yield Mock(choices=[Mock(delta=Mock(content="Thought: I need to search\n"))])
        yield Mock(choices=[Mock(delta=Mock(content="Action: search_web: test"))])

    mock_client.chat.completions.create.return_value = mock_stream_complete()

    agent = AsyncAgent(client=mock_client, max_iterations=3)

    # Collect events from streaming
    events = []
    async for event in agent.run_streaming("Test query"):
        events.append(event)

    # Extract event types (excluding token events for clarity)
    semantic_events = [e for e in events if e.type != "token"]
    event_types = [e.type for e in semantic_events]

    # Should have: thought, action, observation (in that order)
    assert "thought" in event_types
    assert "action" in event_types
    assert "observation" in event_types

    # Verify order
    thought_idx = event_types.index("thought")
    action_idx = event_types.index("action")
    observation_idx = event_types.index("observation")

    assert thought_idx < action_idx, "Thought should come before action"
    assert action_idx < observation_idx, "Action should come before observation"
