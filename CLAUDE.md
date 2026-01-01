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
- Embeddings: HuggingFace SentenceTranformers

## Project Structure

research-assistant/
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
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
├── notes/                  # Knowledge base (markdown files)
├── data/
│   ├── chroma/            # Vector store persistence
│   └── memory.db          # SQLite conversation memory
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

## Implementation Phases

### Phase 1: Basic Agentic Loop

Build a single agent with ReAct-style reasoning loop (Think → Act → Observe → Repeat). Implement basic tools: search_web, save_note.

### Phase 2: MCP Integration

Create MCP servers for filesystem, SQLite memory, and web search. Connect agents to tools via MCP protocol.

### Phase 3: RAG System

Implement document chunking, embedding generation, vector storage with ChromaDB, and semantic retrieval.

### Phase 4: A2A Multi-Agent

Split into specialized agents communicating via A2A protocol. Orchestrator coordinates Researcher, Writer, and Fact-Checker.

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
    api_key = os.getenv("POE_API_KEY")
    base_url = "https://api.poe.com/v1",
)

chat = client.chat.completions.create(
    model = "gpt-5-mini",
    messages = [{
      "role": "user",
      "content": "Analyze the root causes and subsequent impacts of the Industrial Revolution in Europe"
    }]
)

print(chat.choices[0].message.content)
```