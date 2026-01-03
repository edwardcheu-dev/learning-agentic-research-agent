# Research Assistant - Development Commands
# Run `just --list` to see all available commands

# Default recipe (show all available commands)
default:
    @just --list

# Install dependencies and setup pre-commit hooks
setup:
    uv sync
    uv run pre-commit install
    uv run pre-commit install --hook-type commit-msg
    @echo "✅ Setup complete! Ready to develop."

# Run all code quality checks (recommended before commit)
check:
    uv run ruff check . --fix
    uv run ruff format .
    uv run pyright
    uv run pytest
    uv run pre-commit run trailing-whitespace --all-files
    uv run pre-commit run end-of-file-fixer --all-files
    @echo "✅ All checks passed! Ready to commit."

# Run only formatting
fmt:
    uv run ruff format .

# Run only linting
lint:
    uv run ruff check . --fix

# Run only type checking
typecheck:
    uv run pyright

# Run tests (skip integration)
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=src

# Run integration tests (requires ALLOW_INTEGRATION_TESTS=1)
test-integration:
    ALLOW_INTEGRATION_TESTS=1 uv run pytest -m integration

# Run all pre-commit hooks
pre-commit:
    uv run pre-commit run --all-files

# Run basic checks only (formatting, linting, type checking - NO pytest)
check-basic:
    @echo "Running basic checks (formatting, linting, type checking)..."
    uv run ruff check . --fix
    uv run ruff format .
    uv run pyright
    uv run pre-commit run trailing-whitespace --all-files
    uv run pre-commit run end-of-file-fixer --all-files
    @echo "✅ Basic checks passed!"

# TDD Workflow: Commit a failing test (skips pytest to allow TDD)
test-commit message:
    just check-basic
    git add .
    SKIP=pytest git commit -m "test: {{message}}"

# TDD Workflow: Commit implementation (runs ALL checks including pytest)
feat-commit message:
    just check
    git add .
    git commit -m "feat: {{message}}"

# Commit bug fix (runs ALL checks including pytest)
fix-commit message:
    just check
    git add .
    git commit -m "fix: {{message}}"

# Commit refactoring (runs ALL checks including pytest)
refactor-commit message:
    just check
    git add .
    git commit -m "refactor: {{message}}"

# Commit documentation (skips pytest)
docs-commit message:
    just check-basic
    git add .
    SKIP=pytest git commit -m "docs: {{message}}"

# Commit chore/config changes (skips pytest)
chore-commit message:
    just check-basic
    git add .
    SKIP=pytest git commit -m "chore: {{message}}"

# Show TDD workflow example
tdd-help:
    @echo "════════════════════════════════════════════════════════════"
    @echo "  TDD Workflow with Helper Commands"
    @echo "════════════════════════════════════════════════════════════"
    @echo ""
    @echo "1️⃣  Write failing test:"
    @echo "    just test-commit 'add test for streaming events'"
    @echo ""
    @echo "2️⃣  Implement feature:"
    @echo "    just feat-commit 'implement streaming event loop'"
    @echo ""
    @echo "3️⃣  Refactor (optional):"
    @echo "    just refactor-commit 'extract helper method'"
    @echo ""
    @echo "════════════════════════════════════════════════════════════"
    @echo "✨ This ensures tests can be committed while failing (TDD)"
    @echo "   while implementations MUST pass all tests before commit."
    @echo "════════════════════════════════════════════════════════════"

# Run the agent REPL
run:
    uv run python src/main.py

# Clean generated files
clean:
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    rm -rf **/__pycache__
    rm -rf .coverage
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    @echo "✅ Cleaned generated files."
