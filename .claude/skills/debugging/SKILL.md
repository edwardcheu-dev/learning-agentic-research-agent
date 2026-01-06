---
name: debugging
description: Diagnoses errors, test failures, and unexpected behavior. Use proactively when encountering any issues or error messages.
allowed-tools: Read, Grep, Glob, Bash
---

# Debugging Skill

## Debugging Process

1. Capture error message and stack trace
2. Search for error location: `grep -r "error message" src/`
3. Check recent changes: `git log --oneline -10`
4. Read surrounding code context
5. Form hypothesis and test

## Project-Specific Tips

- Use `just test` to run tests (not pytest directly)
- Integration tests require `ALLOW_INTEGRATION_TESTS=1`
- Check `src/config.py` for configuration issues
- AsyncAgent requires AsyncOpenAI client
- Always verify `max_tokens` is set in API calls

## Common Issues

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| Timeout | Missing `max_tokens` | Add `max_tokens=DEFAULT_MAX_TOKENS` |
| Import error | Relative imports | Use absolute imports from `src` |
| API key error | Missing env var | Check `POE_API_KEY` is set |

## Output Format

- Root cause explanation
- Affected files and lines
- Suggested fix with code example
- Prevention recommendations
