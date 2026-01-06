---
paths: src/**/*.py
---

# Code Style

## Imports

- Use absolute imports from `src`: `from src.agents.tools import Tool`
- Never use relative imports (`.tools`, `..config`)
- Prevents import errors when running tests or scripts from different directories

## Methods

- Public methods: no underscore, require docstrings
- Private methods: `_underscore` prefix, docstrings optional
- Example: `Agent.run()` is public, `Agent._parse_action()` is private

## Configuration

- Centralized config in `src/config.py`
- Never hardcode model names, URLs, or defaults
- Import constants: `from src.config import MODEL_NAME, API_BASE_URL`

## Factory Functions

```python
def get_search_web_tool() -> Tool:
    """Factory function for creating search_web tool."""
    return Tool(name="search_web", ...)
```

- Use factory functions for object creation when you need flexibility
- Makes testing easier (can mock factory instead of constructor)
