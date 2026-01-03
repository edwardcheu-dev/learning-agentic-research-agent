# Research & Notes Assistant

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![Phase 1 Complete](https://img.shields.io/badge/Phase%201-Complete-green.svg)
![Phase 2 50% Complete](https://img.shields.io/badge/Phase%202-50%25%20Complete-orange.svg)
![Phase 3-5 Planned](https://img.shields.io/badge/Phase%203--5-Planned-yellow.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

## About This Project

A hands-on learning journey building a multi-agent AI system from scratch. This repository demonstrates core agentic AI concepts through incremental development: **ReAct loops → Textual TUI → MCP integration → RAG → A2A communication**.

**Why this project exists**: To deeply understand agentic AI by building, testing, and documenting each component step-by-step.

## Project Status

- ✅ **Phase 1 COMPLETE**: ReAct agent with web search and note-saving (422 lines of tests, 66%+ coverage)
- 🔄 **Phase 2 IN PROGRESS (50%)**: Textual TUI with async agent, streaming tokens, and basic UI shell (Groups 1-4 complete, 5-8 pending)
- 📋 **Phase 3 PLANNED**: MCP integration (filesystem, memory, vector store)
- 📋 **Phase 4 PLANNED**: RAG system with ChromaDB and semantic search
- 📋 **Phase 5 PLANNED**: Multi-agent orchestration with A2A protocol

## Phase 2 Progress Details

**Completed Groups (50%)**:
- ✅ GROUP 1: Dependencies (textual, rich)
- ✅ GROUP 2: Basic TUI Shell (header, input, conversation container)
- ✅ GROUP 3: Async Agent Foundation (AsyncAgent class with async/await)
- ✅ GROUP 4: Streaming LLM Tokens (AgentEvent stream, character-by-character display)

**Pending Groups**:
- ⏸️ GROUP 5: ReAct Step Visualization (ThoughtNode, ActionNode, ObservationNode)
- ⏸️ GROUP 6: Progressive Disclosure (collapsible sections)
- ⏸️ GROUP 7: Keyboard Navigation (F1 help, F2 logs, Ctrl+L clear)
- ⏸️ GROUP 8: Documentation & Finalization

**Manual Verifications**:
- ✅ Group 2: Basic TUI rendering and input submission ([test plan](docs/test-plans/phase-2-group-2.md)) - Verified 2026-01-04
- ✅ Group 4: Token streaming performance ([test plan](docs/test-plans/phase-2-group-4.md)) - Verified 2026-01-04

See [`docs/checklists/phase-2.md`](docs/checklists/phase-2.md) for detailed progress tracking.

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

# Run the agent with TUI (default, Phase 2)
just run

# OR run with REPL interface (Phase 1)
just run --repl
```

**TUI mode**: Launches Textual-based interface with streaming token display
**REPL mode**: Classic command-line interface with full Thought/Action/Observation output

Try asking: `"Search for Python programming"`

## What You Can Learn From This Repo

- **How to build a ReAct-style reasoning loop from scratch** - See the Thought → Action → Observation cycle in action
- **Building async agents with streaming output** - AsyncAgent with AsyncOpenAI, token-by-token streaming
- **Textual TUI development patterns** - Event-driven UI, progressive widgets, async handlers
- **TDD practices for LLM-based applications** - Write tests before implementation, mock API calls strategically
- **Mocking strategies for testing AI agents** - Test multi-turn conversations without expensive API calls
- **Type-safe configuration and error handling** - Centralize settings, validate environment variables early
- **Professional Python project structure with uv** - Modern package management, proper module organization
- **Pre-commit hooks and code quality automation** - Ruff, Pyright, pytest running on every commit
- **Manual verification workflows for UX validation** - Test plans ensure user experience beyond automated tests

## Demo: Phase 2 TUI in Action (Default)

Launch the TUI:
```bash
just run
```

The Textual-based interface shows:
- **Header**: Research Assistant title with keyboard shortcuts
- **Query Input**: Type your question and press Enter
- **Streaming Response**: Agent's response appears character-by-character as the LLM generates tokens
- **Collapsible Sections** (Groups 5-6, coming soon): Thought/Action/Observation nodes with progressive disclosure

Current Phase 2 status: **50% complete** (streaming tokens working, ReAct visualization pending)

---

## Demo: Phase 1 REPL (Classic Mode)

Launch REPL mode:
```bash
just run --repl
```

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

**Note**: Phase 1 uses mock tool implementations. Phase 3+ will connect to real MCP servers for actual web search and note storage.

## Learning Journey Documentation

**Start here**: [`docs/learning-logs/MASTER_LOG.md`](docs/learning-logs/MASTER_LOG.md) - Complete walkthrough of what was built and why

**Phase logs** (detailed implementation notes):
- **Phase 1** (✅ Complete): [`phase-1-log.md`](docs/learning-logs/phase-1-log.md) - ReAct loop implementation
- **Phase 2** (🔄 In Progress - 50%): [`phase-2-log.md`](docs/learning-logs/phase-2-log.md) - Textual TUI with async agent and streaming (Groups 1-4 documented)
- **Phase 3-5**: Coming as each phase is completed

**Manual Verification**: [`docs/test-plans/`](docs/test-plans/) - UX validation test plans (2 pending for Phase 2)

**Checklists**: [`docs/checklists/`](docs/checklists/) - Track progress through each phase

**Reference guides**: [`docs/reference/`](docs/reference/)
- [POE API Troubleshooting](docs/reference/poe-api-troubleshooting.md) - Model testing and common issues
- [Workflow Guide](docs/reference/workflow-guide.md) - Development patterns and TDD practices
- [Claude Code Tips](docs/reference/claude-code-tips.md) - Effective AI pair programming

## Architecture

```
User → TUI (Textual) → AsyncAgent (ReAct Loop) → Tools → [Web Search | Filesystem | Vector Store | Memory]
         ↓                    ↓
    Streaming Tokens    Thought → Action → Observation → Answer
```

**Phase 1 (Complete)**:
- Synchronous Agent with REPL interface
- Mock tools (search_web, save_note)

**Phase 2 (Current - 60% Complete)**:
- Textual-based TUI with async event handling
- AsyncAgent with token streaming (AsyncOpenAI)
- StreamingText widget for character-by-character display
- ReAct step visualization (Groups 5-6, pending)

**Future Phases**:
- Phase 3: Replace mocks with MCP servers (FastMCP)
- Phase 4: Add RAG with ChromaDB for semantic search over saved notes
- Phase 5: Multi-agent coordination (Orchestrator → Researcher, Writer, Fact-Checker)

## Tech Stack

- **Language**: Python 3.12+
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (NOT pip)
- **LLM**: OpenAI API via POE (gpt-5.1 for most up-to-date ReAct compliance)
- **TUI Framework**: Textual 1.0+ with Rich (Phase 2, in progress)
- **Async Support**: AsyncOpenAI client, pytest-asyncio (Phase 2)
- **Testing**: pytest with comprehensive mocking (37 tests: 20 Phase 1, 17 Phase 2)
- **Type Checking**: Pyright (basic mode)
- **Code Quality**: Ruff (linting + formatting), pre-commit hooks
- **Future Tech**: FastMCP (Phase 3), ChromaDB + HuggingFace embeddings (Phase 4), a2a-python (Phase 5)

## Development Workflow

**Quick commands** (via `just`):
```bash
just setup               # Install dependencies + setup hooks
just run                 # Run the agent (TUI mode, Phase 2 default)
just run --repl          # Run the agent (REPL mode, Phase 1 legacy)
just test                # Run tests (integration skipped)
just check               # Run all quality checks (before commit)
just --list              # Show all available commands
```

**Development workflow commands**:

**Phase execution** (start and resume phases):
```bash
/start-phase N            # Begin new phase with exploration and planning
/resume-phase N           # Resume incomplete phase (detects pending verifications)
```

**Post-milestone reflection** (capture insights and improvements):
```bash
/codebase-qa              # Interactive Q&A about implementation
/update-learnings         # Auto-capture architectural insights to learning logs
/propose-enhancements     # Auto-extract improvement ideas to docs/enhancements/
```

**Enhancement lifecycle** (promote ideas to MVP):
```bash
/promote-enhancements     # Convert P0/P1 enhancements to new MVP phases
```

See [.claude/commands/](.claude/commands/) for detailed command documentation.

**For complete workflow**, see [CONTRIBUTING.md](CONTRIBUTING.md):
- [Pre-commit hooks](CONTRIBUTING.md#pre-commit-hooks) - Auto-formatting, type checking, tests
- [Testing standards](CONTRIBUTING.md#testing-standards) - TDD workflow, coverage requirements
- [Code quality](CONTRIBUTING.md#code-quality-standards) - Ruff, Pyright, commit message format

## Project Structure

```
research-assistant/
├── src/
│   ├── agents/                # ✅ agent.py, async_agent.py, tools.py (Phase 1-2)
│   │                          # 📋 orchestrator.py, researcher.py, writer.py, fact_checker.py (Phase 5 stubs)
│   ├── tui/                   # 🔄 Phase 2 in progress (app.py, widgets.py, events.py)
│   ├── mcp_servers/           # 📋 Phase 3 planned (filesystem, memory, vectorstore servers)
│   ├── rag/                   # 📋 Phase 4 planned (chunking, embeddings, retriever)
│   ├── config.py              # ✅ Centralized configuration
│   ├── main.py                # ✅ Entry point with --tui/--repl flags
│   └── client.py              # ✅ OpenAI/AsyncOpenAI client factory (Phase 2)
├── tests/                     # ✅ 37 tests (20 Phase 1, 17 Phase 2), 66%+ coverage
├── docs/
│   ├── test-plans/            # 🔄 Phase 2 manual verification plans (2 pending)
│   ├── learning-logs/         # Learning narratives
│   ├── checklists/            # Phase progress tracking
│   └── reference/             # Guides and troubleshooting
├── scripts/                   # Model testing and validation
├── data/                      # Vector store, memory (gitignored)
└── notes/                     # User notes (gitignored)
```

**Legend**: ✅ Complete | 🔄 In Progress | 📋 Planned

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
