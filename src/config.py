"""
Centralized configuration for the Research Assistant.

⚠️ IMPORTANT: This is the ONLY place for global configuration settings.

This module provides a single source of truth for all configuration
constants including model settings, API configuration, and defaults.

DO NOT hardcode configuration values anywhere else in the codebase.
All modules must import settings from this file to ensure consistency.

When adding new global configuration:
1. Add the constant here with type hints
2. Add docstring explaining its purpose
3. Update CLAUDE.md Configuration section with the new constant
4. Import and use the constant in other modules

Examples:
    from src.config import MODEL_NAME, get_api_key

    client = openai.OpenAI(
        api_key=get_api_key(),
        base_url=API_BASE_URL
    )
"""

import os

# Model configuration
MODEL_NAME: str = "gpt-5-mini"
"""The OpenAI model to use for agent reasoning."""

DEFAULT_MAX_ITERATIONS: int = 3
"""Default maximum number of ReAct loop iterations."""

# API configuration
API_BASE_URL: str = "https://api.poe.com/v1"
"""Base URL for the POE API."""


def get_api_key() -> str:
    """Get the POE API key from environment variables.

    Returns:
        The POE API key string.

    Raises:
        ValueError: If POE_API_KEY environment variable is not set.
    """
    api_key = os.getenv("POE_API_KEY")
    if not api_key:
        raise ValueError(
            "POE_API_KEY environment variable not set. "
            "Please set it in your shell configuration (e.g., .zshrc)."
        )
    return api_key
