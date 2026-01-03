# Contributing to Research Assistant

> **For AI assistant context**, see [CLAUDE.md](CLAUDE.md)
> **For project overview**, see [README.md](README.md)

Thank you for your interest in contributing! This document provides guidelines for contributing to this learning project.

## Table of Contents

- [Learning Project Philosophy](#learning-project-philosophy)
- [Development Workflow](#development-workflow)
- [Commit Message Format](#commit-message-format)
- [Setting Up Your Development Environment](#setting-up-your-development-environment)
- [Code Quality Standards](#code-quality-standards)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [Testing Standards](#testing-standards)
  - [Type Checking](#type-checking)
  - [Code Style](#code-style)
- [Integration Test Safety](#integration-test-safety)
- [Testing Patterns for LLM Code](#testing-patterns-for-llm-code)
- [Documentation Standards](#documentation-standards)
- [Project Structure](#project-structure)
- [Common Tasks](#common-tasks)

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

1. **EXPLORE**: Use subagents to investigate relevant patterns, docs, or existing code
2. **PLAN**: Create a checklist in `docs/checklists/phase-N.md` before any code
3. **IMPLEMENT**: For each checklist item, follow TDD:
   - Write test first, commit with prefix `test:`
   - Write minimal implementation, commit with prefix `feat:`
   - Refactor if needed, commit with prefix `refactor:`
4. **DOCUMENT**: After each logical group of commits:
   - Append summary to `docs/learning-logs/phase-N-log.md`
   - Update `CLAUDE.md` with patterns learned
   - Commit with prefix `docs:`

### Context Management

- Use `/clear` between major checklist items to keep context focused
- Use subagents for investigation tasks before implementation
- Keep the current phase checklist open as a working scratchpad
- Reference `docs/reference/` for tips and sample prompts

### Learning Logs

After completing a logical group of checklist items:

1. Append a summary to the current phase log (`docs/learning-logs/phase-N-log.md`)
2. Include: what was built, key decisions, code snippets, sample output
3. Periodically update `MASTER_LOG.md` to aggregate all phase logs into a coherent narrative

The `MASTER_LOG.md` should read like a tutorial: "Read this to understand how this repo works."

## Commit Message Format

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
- [just](https://github.com/casey/just) command runner (install via `uv tool install just`)
- POE API key (for OpenAI API access)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/edwardcheu-dev/learning-agentic-research-agent.git
cd learning-agentic-research-agent

# Install just command runner
uv tool install just

# Setup project (dependencies + pre-commit hooks)
just setup

# Set environment variable
export POE_API_KEY="your-poe-api-key"

# Verify setup
just test
```

## Code Quality Standards

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit and enforce:

1. **Ruff** - Linting and formatting (auto-fixes)
2. **Pyright** - Type checking (basic mode)
3. **Pytest** - All tests must pass
4. **File Hygiene** - Whitespace, newlines, YAML/TOML validation
5. **Commit Message** - Validates prefix format

**Recommended workflow before committing**:
```bash
# Run all quality checks (includes formatting, linting, type checking, tests, and file fixers)
just check

# Stage and commit
git add .
git commit -m "feat: your changes here"
```

The `just check` command runs all pre-commit hooks proactively, preventing the need for a second commit due to auto-fixes.

**Manual hook execution** (without committing):
```bash
uv run pre-commit run --all-files
```

**Skip hooks** (NOT recommended):
```bash
git commit --no-verify
```

### Common Commands

Available commands via `just`:

```bash
just --list              # Show all available commands
just setup               # Install dependencies and setup hooks
just check               # Run all quality checks (recommended before commit)
just test                # Run tests
just test-cov            # Run tests with coverage
just fmt                 # Format code only
just lint                # Lint code only
just typecheck           # Type check only
just run                 # Run the agent REPL
just clean               # Clean generated files
```

For detailed command implementations, see [`Justfile`](Justfile) in the project root.

### Testing Standards

**TDD Workflow** (Test-Driven Development):
1. Write test first (should fail)
2. Write minimal implementation (make test pass)
3. Refactor if needed
4. Commit each step separately

**Running tests**:
```bash
# Run all tests (integration tests skipped by default)
just test

# Run with coverage report
just test-cov

# Run specific test file (use uv directly)
uv run pytest tests/agents/test_agent.py

# Run integration tests (requires ALLOW_INTEGRATION_TESTS=1)
just test-integration
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

## Integration Test Safety

Multi-layer protection against accidental API calls during testing:

**Layer 1: Environment Variable Gate** (PRIMARY):
- Integration tests require `ALLOW_INTEGRATION_TESTS=1`
- Auto-skip via `tests/conftest.py` fixture
- Logged when skipped

**Layer 2: Pre-commit Configuration** (SECONDARY):
- Runs: `pytest -m "not integration"`
- Skips all `@pytest.mark.integration` tests

**Layer 3: pytest.ini Default** (TERTIARY):
- Default: `-m "not integration"` in `pyproject.toml`
- Safe even if pytest run manually without flags

**Safe (no API calls)**:
```bash
pytest                    # Default: skips integration
git commit -m "..."       # Pre-commit skips integration
```

**Unsafe (makes API calls)**:
```bash
# Requires explicit opt-in
ALLOW_INTEGRATION_TESTS=1 pytest -m integration
```

**If safety net triggers**:
```
⚠️  SKIPPED integration test: test_model_integration (ALLOW_INTEGRATION_TESTS not set)
```
This is CORRECT behavior - safety net is working!

## Testing Patterns for LLM Code

### Mocking OpenAI/LLM Clients

```python
from unittest.mock import MagicMock

def test_agent_calls_llm():
    """Test agent behavior with mocked LLM client."""
    # Create mock client
    mock_client = MagicMock()

    # Create nested mock for OpenAI response structure
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="LLM response text"))
    ]
    mock_client.chat.completions.create.return_value = mock_response

    # Test code that uses client
    agent = Agent(client=mock_client)
    result = agent.run("query")

    # Verify behavior
    assert mock_client.chat.completions.create.called
```

### Multi-Turn Conversation Testing

```python
def test_multi_turn_conversation():
    """Use side_effect for multiple LLM calls."""
    mock_client = MagicMock()

    # Define sequence of responses
    response_1 = MagicMock()
    response_1.choices = [MagicMock(message=MagicMock(content="First response"))]

    response_2 = MagicMock()
    response_2.choices = [MagicMock(message=MagicMock(content="Second response"))]

    # Use side_effect for sequential returns
    mock_client.chat.completions.create.side_effect = [response_1, response_2]

    # Verify call count
    assert mock_client.chat.completions.create.call_count == 2
```

### Verification Strategies

- Use count assertions (`call_count`, `result.count("text")`) to verify behavior without over-specifying implementation
- Avoid asserting exact strings - check for key phrases or patterns
- Test both success and error paths

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
