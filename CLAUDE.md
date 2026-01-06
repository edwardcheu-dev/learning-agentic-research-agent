# Personal Research & Notes Assistant

> **For development workflow and standards**, see CONTRIBUTING.md
> **For public overview**, see README.md

## Project Overview

This is a hands-on learning project to build a multi-agent AI system demonstrating core agentic AI concepts: agentic loops, RAG, MCP, and A2A communication.

## Architecture

```
User → TUI → AsyncAgent (ReAct Loop) → Tools → [Web Search | Filesystem | Vector Store]
```

## Tech Stack

- Python 3.12+, uv (NOT pip)
- LLM: OpenAI API via POE (gpt-4.1-mini)
- TUI: Textual, Config: Pydantic

## Quick Reference

| Command | Purpose |
|---------|---------|
| `just run` | Launch TUI |
| `just test` | Run tests |
| `just check` | Quality checks |
| `just feat-commit "msg"` | Commit implementation |

## Environment Variables

- `POE_API_KEY`: Required for OpenAI API
- `BRAVE_SEARCH_API_KEY`: Web search

## Implementation Phases

- Phase 1: ReAct agent
- Phase 2: Textual TUI (in progress)
- Phase 3-5: MCP, RAG, A2A (planned)

## Critical: POE API

Always use `max_tokens` in API calls:

```python
from src.config import MODEL_NAME, DEFAULT_MAX_TOKENS
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[...],
    max_tokens=DEFAULT_MAX_TOKENS  # REQUIRED!
)
```

See docs/reference/poe-api-troubleshooting.md for detailed guidance.

## Project Structure

```
research-assistant/
├── src/                      # Source code
│   ├── config.py             # Centralized configuration
│   ├── main.py               # Entry point
│   └── agents/               # Agent implementations
├── tests/                    # Test suite (mirrors src/)
├── docs/                     # Documentation
│   ├── checklists/           # Phase progress tracking
│   ├── learning-logs/        # Implementation narratives
│   └── reference/            # Guides and troubleshooting
└── .claude/                  # Claude Code configuration
    ├── rules/                # Modular project rules
    ├── skills/               # Auto-triggered Skills
    ├── agents/               # Custom subagents
    └── commands/             # Slash commands
```

## For AI Assistants

### Memory Architecture

- **Rules** (`.claude/rules/`): Path-specific coding conventions, loaded automatically
- **Skills** (`.claude/skills/`): Auto-triggered workflows for code review, debugging
- **Subagents** (`.claude/agents/`): Isolated context for specialized tasks
- **Commands** (`.claude/commands/`): Manual workflow invocation

### Documentation Index

| Directory | Purpose | When to Read |
|-----------|---------|--------------|
| `docs/checklists/` | Phase progress tracking | Before starting/resuming work |
| `docs/learning-logs/` | Implementation narratives | For context on past decisions |
| `docs/implementation_plans/` | Phase architecture | Before major implementations |
| `docs/enhancements/` | Post-MVP improvements | When proposing new features |
| `docs/test-plans/` | Manual verification scripts | Before manual testing |
| `docs/reference/` | Guides and troubleshooting | When stuck or need examples |

### Key Patterns

1. **Agentic Loop**: observe -> think -> act -> repeat
2. **TDD Workflow**: `test-commit` -> `feat-commit` (never together)
3. **Imports**: Always absolute from `src`
4. **Config**: All settings in `src/config.py`
