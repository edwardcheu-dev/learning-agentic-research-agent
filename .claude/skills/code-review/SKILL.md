---
name: code-review
description: Reviews code for quality, security, and project conventions. Use proactively after writing or modifying code, or when asked to review.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Skill

When reviewing code, check:

## Project-Specific Rules

1. **API calls**: Verify `max_tokens` included in all POE API calls
2. **Imports**: Absolute from `src`, no relative imports
3. **Config**: No hardcoded values (use `src/config.py`)
4. **Types**: Type hints on all parameters and returns
5. **Docstrings**: Required on public methods

## TDD Compliance

- Tests should exist before implementation
- Commit prefixes: `test:`, `feat:`, `fix:`, `refactor:`

## Security

- No exposed secrets or API keys
- Input validation at boundaries

## Output Format

Provide feedback organized by priority:

- **Critical** (must fix): Security issues, missing max_tokens, broken functionality
- **Warning** (should fix): Missing type hints, hardcoded values
- **Suggestion** (consider): Code style improvements, refactoring opportunities

Include specific examples of how to fix issues.
