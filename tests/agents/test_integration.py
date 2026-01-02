"""
Integration tests for the complete ReAct agent workflow.

These tests verify the end-to-end behavior of the agent running through
multiple iterations of the Thought → Action → Observation → Answer cycle.
"""

from unittest.mock import MagicMock

import pytest

from src.agents.agent import Agent


def test_end_to_end_react_workflow():
    """Test complete agent workflow from query to final answer."""
    # Setup: Mock OpenAI client with multi-turn conversation
    mock_client = MagicMock()
    mock_response_1 = MagicMock()
    mock_response_1.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: I need to search for Python programming.\nAction: search_web: Python programming"  # noqa: E501
            )
        )
    ]

    mock_response_2 = MagicMock()
    mock_response_2.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: I have the information I need.\nAnswer: Python is a popular programming language."  # noqa: E501
            )
        )
    ]

    # Configure mock to return different responses for each call
    mock_client.chat.completions.create.side_effect = [
        mock_response_1,
        mock_response_2,
    ]

    # Execute: Run agent with query
    agent = Agent(client=mock_client, max_iterations=3)
    result = agent.run("Tell me about Python programming")

    # Verify: Check the complete output contains all ReAct components
    assert "Thought: I need to search for Python programming." in result
    assert "Action: search_web: Python programming" in result
    assert "Observation: MOCK SEARCH RESULTS for 'Python programming'" in result
    assert "Thought: I have the information I need." in result
    assert "Answer: Python is a popular programming language." in result

    # Verify: Agent made exactly 2 LLM calls (one action, one answer)
    assert mock_client.chat.completions.create.call_count == 2


def test_end_to_end_multi_action_workflow():
    """Test workflow with multiple tool calls before final answer."""
    # Setup: Mock client with search → save → answer flow
    mock_client = MagicMock()

    mock_response_1 = MagicMock()
    mock_response_1.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: Let me search for AI agents.\nAction: search_web: AI agents"  # noqa: E501
            )
        )
    ]

    mock_response_2 = MagicMock()
    mock_response_2.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: I should save these findings.\nAction: save_note: AI Agents Summary | AI agents are autonomous systems."  # noqa: E501
            )
        )
    ]

    mock_response_3 = MagicMock()
    mock_response_3.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: Research complete and saved.\nAnswer: I found information about AI agents and saved it to your notes."  # noqa: E501
            )
        )
    ]

    mock_client.chat.completions.create.side_effect = [
        mock_response_1,
        mock_response_2,
        mock_response_3,
    ]

    # Execute
    agent = Agent(client=mock_client, max_iterations=3)
    result = agent.run("Research AI agents and save your findings")

    # Verify: Both tools were used
    assert "Action: search_web: AI agents" in result
    assert "Observation: MOCK SEARCH RESULTS for 'AI agents'" in result
    assert "Action: save_note:" in result
    # Note: save_note returns the full input in its message
    assert (
        "MOCK SAVE: Note 'AI Agents Summary | AI agents are autonomous systems.' saved successfully"  # noqa: E501
        in result
    )
    assert (
        "Answer: I found information about AI agents and saved it to your notes."
        in result
    )

    # Verify: Agent made 3 LLM calls
    assert mock_client.chat.completions.create.call_count == 3


def test_end_to_end_max_iterations_reached():
    """Test workflow when agent hits max iterations without providing answer."""
    # Setup: Mock client that keeps returning actions (never provides Answer)
    mock_client = MagicMock()

    # Create 3 identical responses that continue taking actions
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: I need more information.\nAction: search_web: testing"
            )
        )
    ]

    mock_client.chat.completions.create.side_effect = [
        mock_response,
        mock_response,
        mock_response,
    ]

    # Execute
    agent = Agent(client=mock_client, max_iterations=3)
    result = agent.run("Keep searching")

    # Verify: Output contains 3 iterations
    assert result.count("Action: search_web: testing") == 3
    assert result.count("Observation:") == 3

    # Verify: Agent stopped after max_iterations
    assert mock_client.chat.completions.create.call_count == 3


def test_end_to_end_with_unknown_tool_error():
    """Test workflow when agent attempts to use unknown tool.

    Note: Current implementation raises ValueError for unknown tools.
    This is expected behavior at this stage - error handling will be
    improved in future phases.
    """
    # Setup: Mock client returns action with invalid tool
    mock_client = MagicMock()

    mock_response_1 = MagicMock()
    mock_response_1.choices = [
        MagicMock(
            message=MagicMock(
                content="Thought: Let me use a tool.\nAction: invalid_tool: some input"
            )
        )
    ]

    mock_client.chat.completions.create.side_effect = [mock_response_1]

    # Execute and verify: Should raise ValueError for unknown tool
    agent = Agent(client=mock_client, max_iterations=3)

    with pytest.raises(ValueError) as exc_info:
        agent.run("Use a tool")

    assert "Unknown tool" in str(exc_info.value)
    assert "invalid_tool" in str(exc_info.value)
