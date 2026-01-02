"""
Tests for the centralized configuration module.
"""

import os
from unittest.mock import patch

import pytest


def test_config_has_model_name():
    """Config should define MODEL_NAME constant."""
    from src.config import MODEL_NAME

    assert MODEL_NAME == "gpt-4.1-mini"
    assert isinstance(MODEL_NAME, str)


def test_config_has_default_max_iterations():
    """Config should define DEFAULT_MAX_ITERATIONS constant."""
    from src.config import DEFAULT_MAX_ITERATIONS

    assert DEFAULT_MAX_ITERATIONS == 3
    assert isinstance(DEFAULT_MAX_ITERATIONS, int)


def test_config_has_default_max_tokens():
    """Config should define DEFAULT_MAX_TOKENS constant."""
    from src.config import DEFAULT_MAX_TOKENS

    assert DEFAULT_MAX_TOKENS == 1000
    assert isinstance(DEFAULT_MAX_TOKENS, int)


def test_config_has_api_base_url():
    """Config should define API_BASE_URL constant."""
    from src.config import API_BASE_URL

    assert API_BASE_URL == "https://api.poe.com/v1"
    assert isinstance(API_BASE_URL, str)


def test_get_api_key_returns_key_from_env():
    """get_api_key should return POE_API_KEY from environment."""
    from src.config import get_api_key

    with patch.dict(os.environ, {"POE_API_KEY": "test-key-123"}):
        key = get_api_key()
        assert key == "test-key-123"


def test_get_api_key_raises_when_not_set():
    """get_api_key should raise ValueError when POE_API_KEY not set."""
    from src.config import get_api_key

    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            get_api_key()

        assert "POE_API_KEY" in str(exc_info.value)
        assert "not set" in str(exc_info.value)
