"""Integration tests for POE API model validation.

These tests make REAL API calls to POE and cost money!

They are marked with @pytest.mark.integration and will NOT run unless:
1. ALLOW_INTEGRATION_TESTS=1 environment variable is set
2. tests are run with: pytest -m integration

The safety net (tests/conftest.py) will skip these tests by default.

Usage:
    # Safe - skips integration tests
    pytest

    # Unsafe - makes real API calls (costs money!)
    ALLOW_INTEGRATION_TESTS=1 pytest -m integration
"""

import pytest

from src.agents.agent import Agent
from src.config import API_BASE_URL, DEFAULT_MAX_TOKENS, MODEL_NAME, get_api_key


@pytest.mark.integration
def test_configured_model_is_available(api_call_logger):
    """Test that the configured model exists and responds to POE API calls.

    This makes a REAL API call!
    """
    import openai

    api_call_logger(MODEL_NAME, "test_configured_model_is_available")

    client = openai.OpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL,
    )

    # Simple API call to verify model exists
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Say 'test successful' and nothing else."},
        ],
        max_tokens=50,
        timeout=10,
    )

    result = response.choices[0].message.content
    assert result is not None
    assert len(result) > 0
    assert "test" in result.lower()


@pytest.mark.integration
def test_configured_model_follows_react_format(api_call_logger):
    """Test that the configured model produces valid ReAct output.

    This makes a REAL API call!
    """
    import openai

    api_call_logger(MODEL_NAME, "test_configured_model_follows_react_format")

    client = openai.OpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL,
    )

    system_prompt = """You are a ReAct (Reasoning and Acting) agent.

Answer the user's question by following this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name: input]

Available tools:
- search_web: Search the web for information

Always start with a Thought, then take an Action."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": "Use search_web to find information about Python",
            },
        ],
        max_tokens=DEFAULT_MAX_TOKENS,
        timeout=20,
    )

    result = response.choices[0].message.content

    # Validate ReAct format
    assert "Thought:" in result, "Model should include 'Thought:' in ReAct format"
    assert "Action:" in result, "Model should include 'Action:' in ReAct format"
    assert "search_web" in result, "Model should use the search_web tool"


@pytest.mark.integration
def test_configured_model_works_with_agent(api_call_logger):
    """Test that the configured model integrates with Agent class end-to-end.

    This makes REAL API calls!
    """
    import openai

    api_call_logger(MODEL_NAME, "test_configured_model_works_with_agent")

    client = openai.OpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL,
    )

    agent = Agent(client=client, max_iterations=1)

    # Run agent with simple query
    result = agent.run("What is 2+2?")

    # Validate output exists and contains user query
    assert result is not None
    assert "User:" in result or "2+2" in result
    assert len(result) > 0


@pytest.mark.integration
@pytest.mark.slow
def test_configured_model_reliability(api_call_logger):
    """Test that the configured model meets minimum reliability threshold.

    Runs 3 queries and expects at least 50% success rate.

    This makes MULTIPLE REAL API calls!
    """
    import openai

    api_call_logger(MODEL_NAME, "test_configured_model_reliability")

    client = openai.OpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL,
    )

    test_queries = [
        "Say 'test 1' and nothing else.",
        "Say 'test 2' and nothing else.",
        "Say 'test 3' and nothing else.",
    ]

    success_count = 0
    for query in test_queries:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a test assistant."},
                    {"role": "user", "content": query},
                ],
                max_tokens=50,
                timeout=10,
            )

            result = response.choices[0].message.content
            if result and len(result) > 0:
                success_count += 1

        except Exception:
            # Count as failure, continue testing
            pass

    # Require at least 50% success rate (2 out of 3)
    success_rate = success_count / len(test_queries)
    assert success_rate >= 0.5, (
        f"Model reliability too low: {success_rate:.0%} "
        f"(expected >= 50%, got {success_count}/{len(test_queries)} successes)"
    )
