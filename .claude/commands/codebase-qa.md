Interactive Q&A session about the Research Assistant codebase.

## Purpose

Ask questions about:
- How specific features work
- Why certain design decisions were made
- Where to find implementations
- Understanding ReAct loop, MCP servers, RAG, or A2A patterns

## Prerequisites

Read for comprehensive context:
- **CLAUDE.md** - Project overview and patterns
- **MASTER_LOG.md** - Pedagogical walkthrough of all phases
- **docs/learning-logs/phase-N-log.md** - Detailed session logs for specific phases

## Workflow

### 1. CLARIFY THE QUESTION

Ask user to specify:
- What aspect they want to understand (architecture, implementation, design decision)
- Which phase or component (Phase 1 agent, Phase 2 MCP, Phase 3 RAG, Phase 4 A2A)
- Depth of answer needed (high-level overview vs detailed code walkthrough)

### 2. GATHER CONTEXT

Use Explore agents to:
- Find relevant code files
- Read implementation details
- Check learning logs for design rationale
- Review related test files for examples

**Do NOT modify any files** - this is read-only exploration.

### 3. ANSWER THE QUESTION

Provide answer with:
- **Concept Explanation**: High-level description
- **Code References**: File paths and line numbers (e.g., `src/agents/agent.py:112-163`)
- **Why It Works**: Design rationale from learning logs
- **Example**: Concrete code snippet or interaction flow
- **Related Concepts**: Links to related documentation or patterns

### 4. FOLLOW-UP

Ask if the user wants to:
- Dive deeper into specific aspects
- See related code or patterns
- Understand related design decisions
- Capture this understanding in documentation (suggest `/update-learnings`)

## Example Questions

- "How does the ReAct loop orchestrate single actions per iteration?"
- "Why do we use factory functions for tools?"
- "Where is the action parser implemented and how does it work?"
- "What's the difference between messages and conversation in the agent?"

## Important

- Always provide file paths and line numbers for code references
- Explain WHY decisions were made, not just WHAT the code does
- Use learning logs to provide historical context
- Suggest `/update-learnings` if answer reveals insights worth documenting
- Suggest `/propose-enhancements` if answer reveals opportunities worth enhancing
