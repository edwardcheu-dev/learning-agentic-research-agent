# Personal Research & Notes Assistant

> **For development workflow and standards**, see [CONTRIBUTING.md](CONTRIBUTING.md)
> **For public overview**, see [README.md](README.md)

## Project Overview

This is a hands-on learning project to build a multi-agent AI system that demonstrates core agentic AI concepts: agentic loops, RAG (Retrieval-Augmented Generation), MCP (Model Context Protocol), and A2A (Agent-to-Agent) communication.

The system helps users research topics, save findings to a personal knowledge base, and answer questions using RAG—all coordinated by multiple specialized agents.

## Architecture

```
User → Orchestrator Agent → [Researcher | Writer | Fact-Checker] Agents
                                        ↓
                               MCP Servers (Tools)
                          [Web Search | Filesystem | Vector Store | SQLite]
```

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
- LLM: OpenAI API via openai SDK (gpt-4.1-mini for balance of speed/cost/quality)
- MCP Framework: FastMCP
- A2A Framework: a2a-python
- Vector Store: ChromaDB
- Embeddings: HuggingFace SentenceTransformers
- Schema Validation: Pydantic (for cache validation, type safety)

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

```
research-assistant/
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── src/
│   ├── config.py
│   ├── main.py
│   ├── agents/
│   ├── mcp_servers/
│   └── rag/
├── tests/                    # Test suite (mirrors src/)
├── docs/
│   ├── checklists/           # Phase progress tracking
│   ├── learning-logs/        # Implementation narratives
│   ├── implementation_plans/ # Saved implementation plans
│   └── reference/            # Guides and troubleshooting
├── scripts/
│   └── test_poe_models.py    # Model testing script
├── data/
│   ├── chroma/               # Vector store
│   ├── memory.db             # SQLite memory
│   └── model-test-cache.json # Pydantic-validated cache
└── notes/                    # User-saved markdown notes
```

## Implementation Phases

### Phase 1: Basic Agentic Loop

Build a single agent with ReAct-style reasoning loop (Think → Act → Observe → Repeat). Implement basic tools: search_web, save_note.

### Phase 2: MCP Integration

Create MCP servers for filesystem, SQLite memory, and web search. Connect agents to tools via MCP protocol.

### Phase 3: RAG System

Implement document chunking, embedding generation, vector storage with ChromaDB, and semantic retrieval.

### Phase 4: A2A Multi-Agent

Split into specialized agents communicating via A2A protocol. Orchestrator coordinates Researcher, Writer, and Fact-Checker.

## Enhancement Tracking

Beyond the 4 MVP phases, we track post-MVP improvements in `docs/enhancements/`:

- **[schema-validation.md](docs/enhancements/schema-validation.md)**: Pydantic models, Instructor, structured outputs
- **[agent-robustness.md](docs/enhancements/agent-robustness.md)**: Prompt optimization, DSPy, error recovery
- **[observability.md](docs/enhancements/observability.md)**: MLflow tracing, structured logging, cost tracking

Enhancements use **priority labels** (P0/P1/P2) and **status labels** (Idea/Planned/In Progress/Done).

High-priority enhancements (P0/P1) may be promoted into the MVP roadmap. See [docs/enhancements/README.md](docs/enhancements/README.md) for details.

## Development Commands

All commands use uv. Never use pip directly.

**Setup (first time)**:
```bash
uv tool install just         # Install just command runner
uv sync                      # Install dependencies
just setup                   # Setup pre-commit hooks
```

**Common development commands**:
```bash
just check                   # Run all quality checks (recommended before commit)
just test                    # Run tests
just run                     # Run the agent REPL
just --list                  # Show all available commands
```

**Manual commands** (if not using just):
```bash
uv run python src/main.py    # Run the agent
uv run pytest                # Run tests
uv run pytest --cov=src      # With coverage
```

**For complete development workflow**, see [CONTRIBUTING.md#development-workflow](CONTRIBUTING.md#development-workflow)

## Key Patterns to Follow

1. **Agentic Loop**: Always implement observe → think → act → repeat cycle
2. **MCP Tools**: Each tool is a function decorated with @mcp.tool()
3. **A2A Communication**: Agents expose capabilities via Agent Cards and communicate via tasks
4. **RAG Pipeline**: chunk → embed → store → retrieve → augment prompt

## Environment Variables

This project expects the following environment variables to be set in your shell (e.g., .zshrc):

- POE_API_KEY: Required for OpenAI API access
- BRAVE_SEARCH_API_KEY: Used for web search

These should already be available if you've configured your shell correctly.
Do not hardcode API keys in any source files.

To verify they're set:
```bash
echo $POE_API_KEY
```

## For AI Assistants: How to Navigate This Codebase

### Where to Find Things

**Implementations:**
- Core logic: `src/agents/`, `src/mcp_servers/`, `src/rag/`
- Configuration: `src/config.py` (centralized settings)
- Entry point: `src/main.py`

**Tests:**
- Test structure mirrors `src/` exactly
- `tests/agents/`, `tests/` directories
- Integration tests marked with `@pytest.mark.integration`

**Documentation:**
- Implementation plans: `docs/implementation_plans/phase-N.md`
- Progress tracking: `docs/checklists/phase-N.md`
- Learning narratives: `docs/learning-logs/phase-N-log.md`
- Master tutorial: `docs/learning-logs/MASTER_LOG.md`
- Enhancement tracking: `docs/enhancements/` (post-MVP improvements)

**For workflow details**, see [CONTRIBUTING.md](CONTRIBUTING.md):
- [Development Workflow](CONTRIBUTING.md#development-workflow) - TDD cycle, commit prefixes
- [Code Quality Standards](CONTRIBUTING.md#code-quality-standards) - Pre-commit hooks, testing, type checking
- [Integration Test Safety](CONTRIBUTING.md#integration-test-safety) - 4-layer protection against API costs
- [Testing Patterns](CONTRIBUTING.md#testing-patterns-for-llm-code) - Mocking LLM clients
- [Documentation Standards](CONTRIBUTING.md#documentation-standards) - Docstrings, learning logs

## Development Patterns

### Code Organization Principles

**Public vs Private Methods:**
- Public methods: No underscore prefix, part of class API, require docstrings
- Private methods: `_underscore` prefix, internal helpers, docstrings optional but recommended
- Example: `Agent.run()` is public, `Agent._parse_action()` is private

**Factory Functions:**
```python
def get_search_web_tool() -> Tool:
    """Factory function for creating search_web tool."""
    return Tool(
        name="search_web",
        description="Search the web for information",
        function=_search_web_impl
    )
```
- Use factory functions for object creation when you need flexibility
- Makes testing easier (can mock factory instead of constructor)

**Import Conventions:**
- Use absolute imports from `src`: `from src.agents.tools import Tool`
- Never use relative imports (`.tools`, `..config`)
- Prevents import errors when running tests or scripts from different directories

**Module Structure:**
- `src/` contains all source code
- `tests/` mirrors `src/` structure (e.g., `tests/agents/test_tools.py` tests `src/agents/tools.py`)
- `docs/` contains documentation, checklists, logs
- `data/` contains runtime data (databases, vector stores, caches)
- `scripts/` contains utility scripts (testing, validation)

### Error Handling Conventions

**Exception Types:**
- `ValueError`: Invalid inputs, unknown resources (e.g., unknown tool name)
- `FileNotFoundError`: Missing files or directories
- `KeyError`: Missing configuration or environment variables (wrap in `ValueError` with helpful message)
- `RuntimeError`: Unexpected runtime conditions

**When to Raise vs Catch:**
- Early phases: Let exceptions bubble up for fast failure and debugging
- Later phases: Add graceful error recovery (e.g., retry logic, fallbacks)
- Always validate at system boundaries (environment variables, user input, external APIs)

**Error Messages:**
```python
# BAD: Generic message
raise ValueError("Invalid tool")

# GOOD: Specific, actionable message
raise ValueError(f"Unknown tool: {tool_name}. Available tools: {available_tools}")
```

**Environment Variable Validation:**
```python
def get_api_key() -> str:
    """Get API key from environment with validation."""
    api_key = os.getenv("POE_API_KEY")
    if not api_key:
        raise ValueError(
            "POE_API_KEY environment variable not set. "
            "Please set it in your shell configuration (e.g., .zshrc)."
        )
    return api_key
```

### Configuration Management

**CRITICAL: Always Use Centralized Config:**
- ALL global settings MUST be defined in `src/config.py`
- NEVER hardcode model names, API URLs, or defaults in other files
- Import constants: `from src.config import MODEL_NAME, API_BASE_URL`

**Pattern for Adding New Config:**
1. Add constant to `src/config.py` with type hint
2. Add docstring explaining purpose
3. Update CLAUDE.md Configuration section
4. Import and use in other modules

**Environment Variables:**
- Access via getter functions (e.g., `get_api_key()`) for validation
- Never use `os.getenv()` directly in application code
- Validate early (at startup, not during execution)

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
    model=MODEL_NAME,  # gpt-4.1-mini
    messages=[{
        "role": "user",
        "content": "Your prompt here"
    }],
    max_tokens=DEFAULT_MAX_TOKENS  # CRITICAL for POE API
)

print(chat.choices[0].message.content)
```

**Available Configuration Constants:**

- `MODEL_NAME`: The OpenAI model to use (`"gpt-4.1-mini"`)
- `DEFAULT_MAX_ITERATIONS`: Default max ReAct loop iterations (`3`)
- `DEFAULT_MAX_TOKENS`: Default max_tokens for API calls (`1000`) - **REQUIRED for POE API**
- `API_BASE_URL`: POE API base URL (`"https://api.poe.com/v1"`)
- `get_api_key()`: Function that retrieves and validates `POE_API_KEY` from environment

**Benefits of Centralized Config:**
- Single source of truth for all settings
- Prevents inconsistencies (e.g., using wrong model)
- Type hints for better IDE support
- Easy to update settings project-wide

## Important Notes

- Use uv for ALL package management, never pip
- Use uv run to execute Python scripts
- MCP servers run as separate processes
- Vector store persists to data/chroma/
- All notes are markdown files in notes/
- **Model selection**: See [scripts/README.md](scripts/README.md) for model testing workflow before changing `MODEL_NAME`
- **Model testing reports**: Generated in `docs/model-comparison-*.md` for historical reference
- **Integration tests**: Require `ALLOW_INTEGRATION_TESTS=1` to prevent accidental API costs (see [CONTRIBUTING.md#integration-test-safety](CONTRIBUTING.md#integration-test-safety))
