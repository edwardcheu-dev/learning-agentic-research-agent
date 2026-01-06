---
paths: tests/**/*.py
---

# Testing Conventions

## Patterns

- Mock OpenAI client with MagicMock for nested response structure
- Use `side_effect` for multi-turn conversation testing
- Integration tests require `ALLOW_INTEGRATION_TESTS=1`
- Test file structure mirrors `src/` exactly

## Commands

- `just test` - Run unit tests
- `just test-integration` - Run integration tests (requires env var)
- `just test-cov` - Run with coverage

## Mocking LLM Clients

```python
from unittest.mock import MagicMock

mock_client = MagicMock()
mock_client.chat.completions.create.return_value = MagicMock(
    choices=[MagicMock(message=MagicMock(content="response"))]
)
```
