# Research & Notes Assistant

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![Phase 1 Complete](https://img.shields.io/badge/Phase%201-Complete-green.svg)
![Phase 2-5 Planned](https://img.shields.io/badge/Phase%202--5-Planned-yellow.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

## About This Project

A hands-on learning journey building a multi-agent AI system from scratch. This repository demonstrates core agentic AI concepts through incremental development: **ReAct loops → Textual TUI → MCP integration → RAG → A2A communication**.

**Why this project exists**: To deeply understand agentic AI by building, testing, and documenting each component step-by-step.

## Project Status

- ✅ **Phase 1 COMPLETE**: ReAct agent with web search and note-saving (422 lines of tests, 66%+ coverage)
- 📋 **Phase 2 PLANNED**: Textual TUI with streaming and progressive disclosure
- 📋 **Phase 3 PLANNED**: MCP integration (filesystem, memory, vector store) - formerly Phase 2
- 📋 **Phase 4 PLANNED**: RAG system with ChromaDB and semantic search - formerly Phase 3
- 📋 **Phase 5 PLANNED**: Multi-agent orchestration with A2A protocol - formerly Phase 4

## Quick Start

```bash
# Clone the repository
git clone https://github.com/edwardcheu-dev/learning-agentic-research-agent.git
cd learning-agentic-research-agent

# Install just command runner (requires uv package manager)
uv tool install just

# Setup project (dependencies + pre-commit hooks)
just setup

# Set required environment variables
export POE_API_KEY="your-poe-api-key"

# Run the Phase 1 agent (interactive REPL)
just run
```

Try asking: `"Search for Python programming"`

## What You Can Learn From This Repo

- **How to build a ReAct-style reasoning loop from scratch** - See the Thought → Action → Observation cycle in action
- **TDD practices for LLM-based applications** - Write tests before implementation, mock API calls strategically
- **Mocking strategies for testing AI agents** - Test multi-turn conversations without expensive API calls
- **Type-safe configuration and error handling** - Centralize settings, validate environment variables early
- **Professional Python project structure with uv** - Modern package management, proper module organization
- **Pre-commit hooks and code quality automation** - Ruff, Pyright, pytest running on every commit
- **Manual verification workflows for UX validation** - Test plans ensure user experience beyond automated tests

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
- **Phase 2**: [`docs/learning-logs/phase-2-log.md`](docs/learning-logs/phase-2-log.md) - Textual TUI (in progress)
- Phase 3-5: Coming as each phase is completed

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

**Quick commands** (via `just`):
```bash
just setup               # Install dependencies + setup hooks
just run                 # Run the agent
just test                # Run tests (integration skipped)
just check               # Run all quality checks (before commit)
just --list              # Show all available commands
```

**Post-milestone workflow** (capture insights and improvements):
```bash
/codebase-qa              # Interactive Q&A about implementation
/update-learnings         # Auto-capture architectural insights
/propose-enhancements     # Auto-extract improvement ideas
```
See [.claude/commands/](.claude/commands/) for command details.

**For complete workflow**, see [CONTRIBUTING.md](CONTRIBUTING.md):
- [Pre-commit hooks](CONTRIBUTING.md#pre-commit-hooks) - Auto-formatting, type checking, tests
- [Testing standards](CONTRIBUTING.md#testing-standards) - TDD workflow, coverage requirements
- [Code quality](CONTRIBUTING.md#code-quality-standards) - Ruff, Pyright, commit message format

## Project Structure

```
research-assistant/
├── src/                       # ✅ Phase 1 complete (agent.py, tools.py)
│   ├── agents/                # 📋 Phase 4 planned (orchestrator, specialized agents)
│   ├── mcp_servers/           # 📋 Phase 2 planned
│   └── rag/                   # 📋 Phase 3 planned
├── tests/                     # ✅ 422 lines, 66%+ coverage
├── docs/                      # Learning logs, checklists, reference guides
├── scripts/                   # Model testing and validation
├── data/                      # Vector store, memory (gitignored)
└── notes/                     # User notes (gitignored)
```

**Legend**: ✅ Complete | 📋 Planned

For detailed structure, see [CLAUDE.md#project-structure](CLAUDE.md#project-structure)

## For AI Engineers

See [`CLAUDE.md`](CLAUDE.md) for complete project context optimized for AI assistants - implementation patterns, testing strategies, POE API troubleshooting, and navigation guide.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development workflow, TDD practices, commit conventions, and code quality standards.

## License

Apache 2.0 - See [LICENSE](LICENSE) file

---

**Learning Resources**:
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629) - Original research on Reasoning and Acting
- [MCP Documentation](https://modelcontextprotocol.io/) - Model Context Protocol specification
- [A2A Protocol](https://github.com/a2aproject/A2A) - Agent-to-Agent protocol for multi-agent communication (Phase 4)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python) - Official Python SDK for A2A protocol
