# TDD Workflow

## Commit Pattern

1. Write failing test: `just test-commit "add test for X"`
2. Implement feature: `just feat-commit "implement X"`
3. Refactor if needed: `just refactor-commit "refactor X"`

## Never Do

- `git add . && git commit -m "feat: ..."` (skips checks)
- Commit test+implementation together
- Use pip (always use `uv`)
- Skip pre-commit hooks

## Helper Commands

| Command | Purpose |
|---------|---------|
| `just test-commit "msg"` | Commit failing tests (TDD step 1) |
| `just feat-commit "msg"` | Commit implementation (TDD step 2) |
| `just fix-commit "msg"` | Commit bug fixes |
| `just docs-commit "msg"` | Commit documentation |

## Why This Matters

- Prevents pre-commit hook failures and re-commits
- Enforces TDD workflow (separate test/implementation commits)
- Makes git history clean and educational
