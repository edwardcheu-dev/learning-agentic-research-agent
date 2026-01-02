"""Pytest configuration and fixtures for safety nets and shared utilities."""

import logging
import os
from datetime import datetime

import pytest

# Configure logging for API call tracking
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test-api-calls.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def guard_integration_tests(request):
    """Auto-run before EVERY test. Block integration tests unless explicitly enabled.

    This is the PRIMARY safety net against accidental API calls.

    Integration tests must:
    1. Be marked with @pytest.mark.integration
    2. Have ALLOW_INTEGRATION_TESTS=1 environment variable set

    If integration test runs without permission:
    - Test is SKIPPED (safe default)
    - Warning logged to test-api-calls.log
    - User must explicitly opt-in to run

    Example:
        # Safe - integration tests skipped
        pytest

        # Unsafe - requires explicit opt-in
        ALLOW_INTEGRATION_TESTS=1 pytest -m integration
    """
    # Check if test has @pytest.mark.integration marker
    marker = request.node.get_closest_marker("integration")

    if marker:
        # This is an integration test - check if allowed
        allow_integration = os.getenv("ALLOW_INTEGRATION_TESTS", "0") == "1"

        if not allow_integration:
            # 🛡️ SAFETY NET TRIGGERED: Skip integration test
            logger.warning(
                f"⚠️  SKIPPED integration test: {request.node.name} "
                f"(ALLOW_INTEGRATION_TESTS not set)"
            )
            pytest.skip(
                "Integration tests disabled. "
                "Set ALLOW_INTEGRATION_TESTS=1 to enable API calls."
            )
        else:
            # Integration test is allowed - LOG IT
            logger.info(
                f"🌐 RUNNING integration test: {request.node.name} "
                f"(API calls will be made!)"
            )


@pytest.fixture
def api_call_logger():
    """Log every API call for audit trail.

    Creates two logs:
    1. test-api-calls.log - General test logging
    2. api-call-audit.log - Dedicated API call audit (timestamp|test|model)

    Usage:
        @pytest.mark.integration
        def test_model(api_call_logger):
            api_call_logger("gpt-5.1", "test_model")
            # Make API call...
    """

    def log_api_call(model: str, test_name: str):
        timestamp = datetime.now().isoformat()
        logger.warning(
            f"💰 API CALL: model={model}, test={test_name}, time={timestamp}"
        )

        # Also write to dedicated audit file
        with open("api-call-audit.log", "a") as f:
            f.write(f"{timestamp}|{test_name}|{model}\n")

    return log_api_call
