"""OpenAI client creation for the research assistant."""

import openai

from src.config import API_BASE_URL, get_api_key


def create_client() -> openai.OpenAI:
    """Create OpenAI client configured for POE API.

    Returns:
        Configured OpenAI client instance

    Raises:
        ValueError: If POE_API_KEY environment variable is not set
    """
    return openai.OpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL,
    )


def create_async_client() -> openai.AsyncOpenAI:
    """Create async OpenAI client configured for POE API.

    Returns:
        Configured async OpenAI client instance

    Raises:
        ValueError: If POE_API_KEY environment variable is not set
    """
    return openai.AsyncOpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL,
    )
