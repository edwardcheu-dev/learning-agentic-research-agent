---
paths: src/**/*.py
---

# POE API Patterns

## Critical Rules

- ALWAYS use `max_tokens` parameter in API calls (prevents runaway generation)
- Import from centralized config: `from src.config import MODEL_NAME, DEFAULT_MAX_TOKENS`
- Use `gpt-5.1` for latest compliant ReAct OpenAI model

## Code Template

```python
from src.config import MODEL_NAME, DEFAULT_MAX_TOKENS, get_api_key

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[...],
    max_tokens=DEFAULT_MAX_TOKENS  # REQUIRED!
)
```

## Common Issues

- Missing `max_tokens` causes timeout errors and excessive token usage
- See `docs/reference/poe-api-troubleshooting.md` for detailed guidance
