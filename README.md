# Research & Notes Assistant

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![Phase 1 Complete](https://img.shields.io/badge/Phase%201-Complete-green.svg)
![Phase 2-4 Planned](https://img.shields.io/badge/Phase%202--4-Planned-yellow.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

## About This Project

A hands-on learning journey building a multi-agent AI system from scratch. This repository demonstrates core agentic AI concepts through incremental development: **ReAct loops → MCP integration → RAG → A2A communication**.

**Why this project exists**: To deeply understand agentic AI by building, testing, and documenting each component step-by-step.

## Project Status

- ✅ **Phase 1 COMPLETE**: ReAct agent with web search and note-saving (422 lines of tests, 66%+ coverage)
- 📋 **Phase 2 PLANNED**: MCP integration (filesystem, memory, vector store)
- 📋 **Phase 3 PLANNED**: RAG system with ChromaDB and semantic search
- 📋 **Phase 4 PLANNED**: Multi-agent orchestration with A2A protocol

## Quick Start

```bash
# Clone the repository
git clone https://github.com/edwardcheu-dev/learning-agentic-research-agent.git
cd learning-agentic-research-agent

# Install dependencies (requires uv package manager)
uv sync

# Set required environment variables
export POE_API_KEY="your-poe-api-key"

# Run the Phase 1 agent (interactive REPL)
uv run python src/main.py
```

Try asking: `"Search for Python programming"`

## What You Can Learn From This Repo

- **How to build a ReAct-style reasoning loop from scratch** - See the Thought → Action → Observation cycle in action
- **TDD practices for LLM-based applications** - Write tests before implementation, mock API calls strategically
- **Mocking strategies for testing AI agents** - Test multi-turn conversations without expensive API calls
- **Type-safe configuration and error handling** - Centralize settings, validate environment variables early
- **Professional Python project structure with uv** - Modern package management, proper module organization
- **Pre-commit hooks and code quality automation** - Ruff, Pyright, pytest running on every commit

## Demo: Phase 1 Agent in Action

```
User: Search for Python programming

Thought: I need to search for information about Python programming.
Action: search_web: Python programming

Observation: MOCK SEARCH RESULTS for 'Python programming':
1. Example result about Python programming
2. Another result for Python programming

Thought: I have the search results. I can now provide an answer.
Answer: Python is a popular high-level programming language known for
its readability and versatility.
```

**Note**: Phase 1 uses mock tool implementations. Phase 2+ will connect to real MCP servers for actual web search and note storage.

## Learning Journey Documentation

**Start here**: [`docs/learning-logs/MASTER_LOG.md`](docs/learning-logs/MASTER_LOG.md) - Complete walkthrough of what was built and why

**Phase logs** (detailed implementation notes):
- **Phase 1**: [`docs/learning-logs/phase-1-log.md`](docs/learning-logs/phase-1-log.md) - ReAct loop implementation
- Phase 2-4: Coming as each phase is completed

**Checklists**: [`docs/checklists/`](docs/checklists/) - Track progress through each phase

**Reference guides**: [`docs/reference/`](docs/reference/)
- [POE API Troubleshooting](docs/reference/poe-api-troubleshooting.md) - Model testing and common issues
- [Workflow Guide](docs/reference/workflow-guide.md) - Development patterns and TDD practices
- [Claude Code Tips](docs/reference/claude-code-tips.md) - Effective AI pair programming

## Architecture

```
User → Agent (ReAct Loop) → Tools → [Web Search | Filesystem | Vector Store | Memory]
         ↓
    Thought → Action → Observation → Answer
```

**Phase 1 (Current)**:
- Single ReAct agent with mock tools
- ReAct pattern: LLM reasons explicitly before acting

**Future Phases**:
- Phase 2: Replace mocks with MCP servers (FastMCP)
- Phase 3: Add RAG with ChromaDB for semantic search over saved notes
- Phase 4: Multi-agent coordination (Orchestrator → Researcher, Writer, Fact-Checker)

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (NOT pip)
- **LLM**: OpenAI API via POE (gpt-4.1-mini for balance of speed/cost/quality)
- **Testing**: pytest with comprehensive mocking (422 lines of tests)
- **Type Checking**: Pyright (basic mode)
- **Code Quality**: Ruff (linting + formatting), pre-commit hooks
- **Future Tech**: FastMCP (Phase 2), ChromaDB + HuggingFace embeddings (Phase 3), a2a-python (Phase 4)

## Development Workflow

**Install dependencies**:
```bash
uv sync
```

**Run the agent**:
```bash
uv run python src/main.py
```

**Run tests** (all integration tests skipped by default to prevent API costs):
```bash
uv run pytest
```

**Run tests with coverage**:
```bash
uv run pytest --cov=src
```

**Format and lint** (recommended before committing):
```bash
uv run ruff check . --fix
uv run ruff format .
```

**Type check**:
```bash
uv run pyright
```

Pre-commit hooks run automatically on `git commit` to enforce:
- Code formatting (Ruff)
- Type checking (Pyright)
- Tests passing (pytest, integration tests skipped)
- Commit message format (`feat:`, `test:`, `docs:`, `fix:`, `refactor:`, `chore:`)

## Project Structure

```
research-assistant/
├── src/
│   ├── config.py              # Centralized configuration
│   ├── main.py                # Interactive REPL entry point
│   ├── agents/
│   │   ├── agent.py           # ✅ Phase 1: ReAct agent implementation
│   │   ├── tools.py           # ✅ Phase 1: Tool system with mocks
│   │   ├── orchestrator.py    # 📋 Phase 4: Multi-agent coordinator
│   │   ├── researcher.py      # 📋 Phase 4: Web research specialist
│   │   ├── writer.py          # 📋 Phase 4: Note synthesis agent
│   │   └── fact_checker.py    # 📋 Phase 4: RAG-based validation
│   ├── mcp_servers/           # 📋 Phase 2: MCP tool servers
│   │   ├── filesystem_server.py
│   │   ├── vectorstore_server.py
│   │   └── memory_server.py
│   └── rag/                   # 📋 Phase 3: RAG components
│       ├── embeddings.py
│       ├── chunking.py
│       └── retriever.py
├── tests/                     # ✅ Comprehensive test suite (422 lines)
├── docs/
│   ├── learning-logs/         # Implementation narratives
│   ├── checklists/            # Phase progress tracking
│   └── reference/             # Guides and troubleshooting
├── scripts/
│   └── test_poe_models.py     # Model testing and validation
├── data/
│   ├── chroma/                # Vector store (Phase 3)
│   └── memory.db              # SQLite memory (Phase 2)
└── notes/                     # User-saved markdown notes
```

Legend: ✅ Complete | 📋 Planned

## For AI Engineers

See [`CLAUDE.md`](CLAUDE.md) for complete project context optimized for AI assistants like Claude Code. It contains:
- Implementation patterns and conventions
- Testing strategies for LLM applications
- POE API troubleshooting and model selection
- Code quality standards and pre-commit hooks
- Phase-by-phase implementation guide

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:
- Development workflow and TDD practices
- Commit message conventions
- Code quality standards
- How to run tests safely without API costs

## License

Apache 2.0 - See [LICENSE](LICENSE) file

---

**Learning Resources**:
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629) - Original research on Reasoning and Acting
- [MCP Documentation](https://modelcontextprotocol.io/) - Model Context Protocol specification
- [A2A Protocol](https://github.com/a2aproject/A2A) - Agent-to-Agent protocol for multi-agent communication (Phase 4)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python) - Official Python SDK for A2A protocol
