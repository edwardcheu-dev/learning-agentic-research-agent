# Personal Research & Notes Assistant

## Project Overview

This is a hands-on learning project to build a multi-agent AI system that demonstrates core agentic AI concepts: agentic loops, RAG (Retrieval-Augmented Generation), MCP (Model Context Protocol), and A2A (Agent-to-Agent) communication.

The system helps users research topics, save findings to a personal knowledge base, and answer questions using RAG—all coordinated by multiple specialized agents.

## Architecture

User → Orchestrator Agent → [Researcher | Writer | Fact-Checker] Agents
                                        ↓
                               MCP Servers (Tools)
                          [Web Search | Filesystem | Vector Store | SQLite]

### Agents (A2A)

- Orchestrator: Plans tasks, routes to specialized agents, aggregates results
- Researcher: Searches the web for information
- Writer: Synthesizes findings into notes
- Fact-Checker: Validates claims against the knowledge base using RAG

### MCP Servers

- Filesystem: Read/write markdown notes in notes/ directory
- Vector Store: ChromaDB for embeddings and semantic search (RAG)
- SQLite: Conversation memory and metadata
- Web Search: Brave Search API

## Tech Stack

- Python: 3.12+
- Package Manager: uv (NOT pip)
- LLM: OpenAI API via openai SDK (gpt-5.1 recommended)
- MCP Framework: FastMCP
- A2A Framework: a2a-python
- Vector Store: ChromaDB
- Embeddings: HuggingFace SentenceTransformers

## Troubleshooting

### POE API Important Notes

⚠️ **CRITICAL**: When using POE API, always set `max_tokens` parameter in API calls to prevent:
- Runaway image generation
- Timeout errors
- Excessive token usage

Use the centralized constant:
```python
from src.config import DEFAULT_MAX_TOKENS, MODEL_NAME

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[...],
    max_tokens=DEFAULT_MAX_TOKENS  # Always include this!
)
```

For detailed troubleshooting, model selection guidance, and common issues:
- **[POE API Troubleshooting Guide](docs/reference/poe-api-troubleshooting.md)** - Comprehensive model comparison, common issues, and solutions

## Project Structure

research-assistant/
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .claude/
│   └── commands/
│       └── start-phase.md
├── src/
│   ├── config.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── researcher.py
│   │   ├── writer.py
│   │   └── fact_checker.py
│   ├── mcp_servers/
│   │   ├── __init__.py
│   │   ├── filesystem_server.py
│   │   ├── vectorstore_server.py
│   │   └── memory_server.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── chunking.py
│   │   └── retriever.py
│   └── main.py
├── scripts/
│   ├── CLAUDE.md           # AI agent context
│   ├── README.md           # Human documentation
│   └── test_poe_models.py  # Model testing script
├── docs/
│   ├── checklists/
│   │   ├── phase-1.md
│   │   ├── phase-2.md
│   │   ├── phase-3.md
│   │   └── phase-4.md
│   ├── learning-logs/
│   │   ├── MASTER_LOG.md
│   │   ├── phase-1-log.md
│   │   ├── phase-2-log.md
│   │   ├── phase-3-log.md
│   │   └── phase-4-log.md
│   ├── model-comparison-*.md  # Generated model test reports
│   └── reference/
│       ├── claude-code-tips.md
│       ├── poe-api-troubleshooting.md
│       ├── sample-prompts.md
│       └── workflow-guide.md
├── notes/
├── data/
│   ├── chroma/
│   └── memory.db
└── tests/

## Development Commands

All commands use uv. Never use pip directly.

Install dependencies:
    uv sync

Add a new dependency:
    uv add <package>

Add a dev dependency:
    uv add --dev <package>

Run the main application:
    uv run python src/main.py

Run a specific MCP server:
    uv run python src/mcp_servers/filesystem_server.py

Run tests:
    uv run pytest

Run tests with coverage:
    uv run pytest --cov=src

## Scripts

The `scripts/` directory contains utility scripts for testing and validation.

### Model Testing

**Test POE API models for ReAct agent compatibility**:
```bash
uv run python scripts/test_poe_models.py
```

This script:
- Tests multiple models (gpt-4.1, gpt-4.1-mini, gpt-5.1, etc.)
- Validates ReAct format compliance
- Measures reliability and performance
- Generates comparison report in `docs/model-comparison-{date}.md`

**Configure models to test**:
Edit `scripts/test_poe_models.py` and modify the `MODELS_TO_TEST` list.

**When to run**:
- Before changing `MODEL_NAME` in `src/config.py`
- When POE API adds new models
- If experiencing model instability
- To validate model selection for production

See [scripts/README.md](scripts/README.md) for detailed usage and [scripts/CLAUDE.md](scripts/CLAUDE.md) for AI agent context.

## Implementation Phases

### Phase 1: Basic Agentic Loop

Build a single agent with ReAct-style reasoning loop (Think → Act → Observe → Repeat). Implement basic tools: search_web, save_note.

### Phase 2: MCP Integration

Create MCP servers for filesystem, SQLite memory, and web search. Connect agents to tools via MCP protocol.

### Phase 3: RAG System

Implement document chunking, embedding generation, vector storage with ChromaDB, and semantic retrieval.

### Phase 4: A2A Multi-Agent

Split into specialized agents communicating via A2A protocol. Orchestrator coordinates Researcher, Writer, and Fact-Checker.

## Development Workflow

This project follows a structured learning workflow combining exploration, planning, TDD, and atomic commits.

### Phase Workflow Pattern

For each implementation phase:

1. EXPLORE: Use subagents to investigate relevant patterns, docs, or existing code
2. PLAN: Create a checklist in docs/checklists/phase-N.md before any code
3. IMPLEMENT: For each checklist item, follow TDD:
   - Write test first, commit with prefix `test:`
   - Write implementation, commit with prefix `feat:`
   - Refactor if needed, commit with prefix `refactor:`
4. DOCUMENT: After each logical group of commits:
   - Append summary to docs/learning-logs/phase-N-log.md
   - Update CLAUDE.md with patterns learned
   - Commit with prefix `docs:`

### Commit Message Prefixes

- `test:` - Adding or updating tests (before implementation)
- `feat:` - New feature implementation (making tests pass)
- `fix:` - Bug fixes (correcting incorrect behavior)
- `refactor:` - Code improvement without behavior change
- `docs:` - Documentation updates
- `chore:` - Build, config, or tooling changes

### Learning Logs

After completing a logical group of checklist items:

1. Append a summary to the current phase log (docs/learning-logs/phase-N-log.md)
2. Include: what was built, key decisions, code snippets, sample output
3. Periodically update MASTER_LOG.md to aggregate all phase logs into a coherent narrative

The MASTER_LOG.md should read like a tutorial: "Read this to understand how this repo works."

### Context Management

- Use /clear between major checklist items to keep context focused
- Use subagents for investigation tasks before implementation
- Keep the current phase checklist open as a working scratchpad
- Reference docs/reference/ for tips and sample prompts

## Key Patterns to Follow

1. Agentic Loop: Always implement observe → think → act → repeat cycle
2. MCP Tools: Each tool is a function decorated with @mcp.tool()
3. A2A Communication: Agents expose capabilities via Agent Cards and communicate via tasks
4. RAG Pipeline: chunk → embed → store → retrieve → augment prompt

## Environment Variables

This project expects the following environment variables to be set in your shell (e.g., .zshrc):

- POE_API_KEY: Required for OpenAI API access
- BRAVE_SEARCH_API_KEY: Used for web search

These should already be available if you've configured your shell correctly.
Do not hardcode API keys in any source files.

To verify they're set:
    echo $POE_API_KEY

## Code Quality & Testing

This project enforces code quality through automated tools and TDD practices.

### Pre-commit Hooks (Automated)

Pre-commit hooks run automatically on every commit to ensure code quality:

**Setup** (one-time):
    uv run pre-commit install
    uv run pre-commit install --hook-type commit-msg

**Hooks Enforced:**
1. **Ruff** - Auto-fixes linting and formatting issues
2. **Pyright** - Type checking (configured for "basic" mode)
3. **Pytest** - Runs all tests before allowing commit
4. **File Hygiene** - Trims whitespace, ensures newlines, validates YAML/TOML
5. **Commit Message Validation** - Requires prefix: `test:`, `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`

**Manual Commands:**
    uv run pre-commit run --all-files    # Run all hooks without committing
    git commit --no-verify                # Skip hooks (NOT recommended)

### Testing (TDD Workflow)

Write tests BEFORE implementation:
    uv run pytest                # Run all tests
    uv run pytest --cov=src      # Run with coverage report

- Test files mirror source structure in `tests/` directory
- Follow the pattern: test first (red) → implement (green) → refactor
- Aim for >70% code coverage

### Type Checking

All code includes type hints:
    uv run pyright               # Run type checker manually

- Function parameters and return types must be annotated
- Class attributes should have type hints
- Use `Any` sparingly (only for external library types)
- Configuration: `[tool.pyright]` in `pyproject.toml`

### Code Style

**Recommended workflow** (run BEFORE committing):
```bash
uv run ruff check . --fix      # Auto-fix linting issues
uv run ruff format .           # Auto-format code (line length, imports, etc.)
git add .                      # Stage the formatted files
git commit -m "..."            # Now pre-commit will pass quickly
```

This prevents pre-commit from reformatting and requiring a second commit.

**Style guidelines**:
- Line length: 88 characters (auto-fixed by Ruff)
- Import ordering: stdlib → third-party → local (auto-fixed by Ruff)
- Style guide: PEP 8 compliant

**What Ruff fixes automatically**:
- Lines exceeding 88 characters (wraps them)
- Import sorting and organization
- Trailing whitespace
- Unused imports
- Common PEP 8 violations

**Manual formatting** (if you forget to run before commit):
Ruff runs automatically via pre-commit hooks, but will require re-committing the formatted files.

### API Call Safety Net

**Multi-layer protection against accidental API calls during testing**:

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

**Layer 4: Logging & Audit Trail** (DETECTION):
- `test-api-calls.log`: All test output
- `api-call-audit.log`: API call timestamps
- Post-commit hook checks for violations

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

**Verify safety net**:
```bash
# Should be empty after commit (if no integration tests ran)
cat api-call-audit.log
```

**If safety net triggers**:
```
⚠️  SKIPPED integration test: test_model_integration (ALLOW_INTEGRATION_TESTS not set)
```
This is CORRECT behavior - safety net is working!

### Development Patterns

Patterns established during development will be documented here.

## Important Notes

- Use uv for ALL package management, never pip
- Use uv run to execute Python scripts
- MCP servers run as separate processes
- Vector store persists to data/chroma/
- All notes are markdown files in notes/
- **Model selection**: Use `scripts/test_poe_models.py` to validate before changing models
- **Model testing reports**: Generated in `docs/model-comparison-*.md` for historical reference
- **Integration tests**: Require `ALLOW_INTEGRATION_TESTS=1` to prevent accidental API costs

## Configuration

All configuration is centralized in `src/config.py` for consistency:

```python
from src.config import MODEL_NAME, API_BASE_URL, get_api_key
import openai

# Create OpenAI client using centralized config
client = openai.OpenAI(
    api_key=get_api_key(),  # Validates POE_API_KEY is set
    base_url=API_BASE_URL,  # https://api.poe.com/v1
)

# Use centralized model name
chat = client.chat.completions.create(
    model=MODEL_NAME,  # gpt-5.1
    messages=[{
        "role": "user",
        "content": "Your prompt here"
    }],
    max_tokens=DEFAULT_MAX_TOKENS  # CRITICAL for POE API
)

print(chat.choices[0].message.content)
```

**Available Configuration Constants:**

- `MODEL_NAME`: The OpenAI model to use (`"gpt-5.1"`)
- `DEFAULT_MAX_ITERATIONS`: Default max ReAct loop iterations (`3`)
- `DEFAULT_MAX_TOKENS`: Default max_tokens for API calls (`1000`) - **REQUIRED for POE API**
- `API_BASE_URL`: POE API base URL (`"https://api.poe.com/v1"`)
- `get_api_key()`: Function that retrieves and validates `POE_API_KEY` from environment

**Benefits of Centralized Config:**
- Single source of truth for all settings
- Prevents inconsistencies (e.g., using wrong model)
- Type hints for better IDE support
- Easy to update settings project-wide
