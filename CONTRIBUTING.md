# Contributing to Research Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to this learning project.

## Learning Project Philosophy

This is a hands-on learning project designed to demonstrate core agentic AI concepts through incremental development. Contributions should:

- **Maintain educational value**: Changes should help others learn, not just add features
- **Follow the TDD workflow**: Write tests before implementation
- **Document decisions**: Explain *why* choices were made, not just *what* was done
- **Preserve transparency**: Keep the learning journey visible (checklists, logs, etc.)

## Development Workflow

This project follows a structured workflow: **Explore → Plan → Test → Implement → Document**

### Phase Workflow Pattern

For each implementation phase:

1. **EXPLORE**: Investigate relevant patterns, documentation, or existing code
2. **PLAN**: Create a checklist in `docs/checklists/phase-N.md` before writing code
3. **IMPLEMENT**: For each checklist item, follow TDD:
   - Write test first, commit with `test:` prefix
   - Write minimal implementation, commit with `feat:` prefix
   - Refactor if needed, commit with `refactor:` prefix
4. **DOCUMENT**: After completing a logical group:
   - Append summary to `docs/learning-logs/phase-N-log.md`
   - Update `CLAUDE.md` with patterns learned
   - Commit with `docs:` prefix

### Commit Message Format

All commits **must** use one of these prefixes:

- `test:` - Adding or updating tests (before implementation)
- `feat:` - New feature implementation (making tests pass)
- `fix:` - Bug fixes (correcting incorrect behavior)
- `refactor:` - Code improvement without behavior change
- `docs:` - Documentation updates
- `chore:` - Build, config, or tooling changes

**Examples**:
```bash
git commit -m "test: add ReAct loop parsing tests"
git commit -m "feat: implement action parser for ReAct agent"
git commit -m "docs: document Phase 1 tool system design"
```

Pre-commit hooks will reject commits without a valid prefix.

## Setting Up Your Development Environment

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager (NOT pip)
- POE API key (for OpenAI API access)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/edwardcheu-dev/learning-agentic-research-agent.git
cd learning-agentic-research-agent

# Install dependencies
uv sync

# Install pre-commit hooks (REQUIRED)
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Set environment variable
export POE_API_KEY="your-poe-api-key"

# Verify setup
uv run pytest
```

## Code Quality Standards

### Pre-commit Hooks (Automated)

Pre-commit hooks run automatically on every commit and enforce:

1. **Ruff** - Linting and formatting (auto-fixes)
2. **Pyright** - Type checking (basic mode)
3. **Pytest** - All tests must pass
4. **File Hygiene** - Whitespace, newlines, YAML/TOML validation
5. **Commit Message** - Validates prefix format

**Recommended workflow before committing**:
```bash
# Format and fix issues proactively
uv run ruff check . --fix
uv run ruff format .

# Run tests
uv run pytest

# Stage and commit
git add .
git commit -m "feat: your changes here"
```

This prevents pre-commit from reformatting and requiring a second commit.

**Manual hook execution** (without committing):
```bash
uv run pre-commit run --all-files
```

### Testing Requirements

**TDD Workflow** (Test-Driven Development):
1. Write test first (should fail)
2. Write minimal implementation (make test pass)
3. Refactor if needed
4. Commit each step separately

**Running tests**:
```bash
# Run all tests (integration tests skipped by default)
uv run pytest

# Run with coverage report
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/agents/test_agent.py
```

**Integration test safety**:
- Integration tests (that make real API calls) require `ALLOW_INTEGRATION_TESTS=1`
- Pre-commit hooks skip integration tests by default to prevent API costs
- Only run integration tests when explicitly intended:
  ```bash
  ALLOW_INTEGRATION_TESTS=1 pytest -m integration
  ```

**Testing standards**:
- Test files mirror source structure in `tests/` directory
- Aim for >70% code coverage (core logic should be 90%+)
- Mock LLM clients to avoid API costs during unit tests
- Use `@pytest.mark.integration` for tests that make real API calls

### Type Checking

All code must include type hints:

```python
# ✅ Good: Full type hints
def run(self, query: str) -> str:
    """Run agent on query."""
    pass

# ❌ Bad: Missing type hints
def run(self, query):
    pass
```

**Run type checker**:
```bash
uv run pyright
```

**Type hint conventions**:
- Use modern syntax: `list[str]` not `List[str]`
- Use `str | None` not `Optional[str]`
- Annotate all function parameters and return values
- Add type hints to class attributes
- Use `Any` sparingly (only for external library types)

### Code Style

**Style guide**: PEP 8 compliant, 88 character line length

**Automatic formatting**:
```bash
uv run ruff check . --fix    # Fix linting issues
uv run ruff format .         # Format code
```

Ruff automatically fixes:
- Line length (wraps at 88 characters)
- Import sorting (stdlib → third-party → local)
- Trailing whitespace
- Unused imports
- Common PEP 8 violations

## Documentation Standards

### Code Documentation

**Docstrings required** for all public functions, classes, and methods:

```python
def parse_action(self, response: str) -> tuple[str, str] | None:
    """Parse action from LLM response.

    Args:
        response: The LLM's response text

    Returns:
        Tuple of (tool_name, tool_input) if action found, None otherwise

    Raises:
        ValueError: If action format is invalid
    """
```

Use Google-style docstrings with Args, Returns, and Raises sections.

### Learning Logs

After completing checklist items, document in `docs/learning-logs/phase-N-log.md`:

- **What was built**: Describe the feature or component
- **Key decisions**: Explain *why* you chose this approach
- **Code snippets**: Show important implementations
- **Sample output**: Demonstrate the feature working

This helps others learn from your implementation journey.

## Running the Project

**Interactive REPL** (Phase 1):
```bash
uv run python src/main.py
```

**Run tests**:
```bash
uv run pytest
```

**Format and lint**:
```bash
uv run ruff check . --fix
uv run ruff format .
```

**Type check**:
```bash
uv run pyright
```

## Project Structure

Understanding the layout:

```
research-assistant/
├── src/                      # Application source code
│   ├── config.py             # Centralized configuration
│   ├── main.py               # Entry point (REPL)
│   ├── agents/               # Agent implementations
│   ├── mcp_servers/          # MCP tool servers
│   └── rag/                  # RAG components
├── tests/                    # Test suite (mirrors src/)
├── docs/
│   ├── checklists/           # Phase progress tracking
│   ├── learning-logs/        # Implementation narratives
│   └── reference/            # Guides and troubleshooting
├── scripts/                  # Utility scripts
├── data/                     # Runtime data (gitignored)
└── notes/                    # User notes (gitignored)
```

## Common Tasks

### Adding a New Feature

1. **Create checklist item** in `docs/checklists/phase-N.md`
2. **Write tests** in `tests/` (commit with `test:`)
3. **Implement feature** in `src/` (commit with `feat:`)
4. **Update documentation** in `docs/learning-logs/` (commit with `docs:`)

### Fixing a Bug

1. **Write failing test** that reproduces the bug (commit with `test:`)
2. **Fix the bug** in source code (commit with `fix:`)
3. **Verify test passes** and all other tests still pass

### Refactoring

1. **Ensure tests exist** for the code being refactored
2. **Make changes** without altering behavior (commit with `refactor:`)
3. **Verify all tests still pass**

## Getting Help

- **Questions about the codebase**: See [`CLAUDE.md`](CLAUDE.md) for comprehensive project context
- **Learning resources**: Check [`docs/reference/`](docs/reference/) for guides
- **Phase-specific help**: Review [`docs/learning-logs/MASTER_LOG.md`](docs/learning-logs/MASTER_LOG.md)

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
