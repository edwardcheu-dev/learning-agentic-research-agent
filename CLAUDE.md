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
- LLM: OpenAI API via openai SDK (gpt-5-mini recommended)
- MCP Framework: FastMCP
- A2A Framework: a2a-python
- Vector Store: ChromaDB
- Embeddings: HuggingFace SentenceTransformers

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
│   └── reference/
│       ├── claude-code-tips.md
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

## Code Style

Use ruff for linting and formatting. Run before committing:
    uv run ruff check .
    uv run ruff format .

## Testing

This project follows TDD. Write tests before implementation.
    uv run pytest
    uv run pytest --cov=src

Test files mirror source structure in tests/ directory.

Patterns established during development will be documented here.

## Important Notes

- Use uv for ALL package management, never pip
- Use uv run to execute Python scripts
- MCP servers run as separate processes
- Vector store persists to data/chroma/
- All notes are markdown files in notes/
- Use POE Python OpenAI for client creation:

```python
import os
import openai

client = openai.OpenAI(
    api_key=os.getenv("POE_API_KEY"),
    base_url="https://api.poe.com/v1",
)

chat = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{
        "role": "user",
        "content": "Your prompt here"
    }]
)

print(chat.choices[0].message.content)