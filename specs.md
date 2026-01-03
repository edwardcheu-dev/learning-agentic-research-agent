# TUI Enhancement Specification: Replace REPL with Textual-based Interface

> **Purpose**: This document provides context for Claude Code to understand the objective, current pain points, and implementation plan for upgrading the Research Assistant's user interface from a basic REPL to a professional-grade TUI using Textual.
>
> **Workflow**: After reading this document, use `/propose-enhancements` to add entries to `docs/enhancements/developer-experience.md`, then `/promote-enhancements` to add to the MVP roadmap. Since developer-experience is a new enhancement category, make sure CLAUDE.md, README.md, CONTRIBUTING.md and any other critical docs are also updated accordingly.

## Executive Summary

The current `src/main.py` implements a minimal input/output REPL that lacks visibility into agent reasoning, streaming support, and interactive inspection capabilities. This proposal replaces it with a Textual-based TUI that provides real-time streaming, collapsible reasoning steps, and on-demand detail expansion—critical for developing and debugging agentic systems.

**Priority**: P0 (Critical) - Essential, promote to phase 2 development where debugging multi-step agent reasoning becomes critical. Push existing phase 2 -> 3, phase 3 -> 4 and phase 4 -> 5.

## Current Pain Points

### 1. No Streaming Support

The current implementation blocks until the full response is ready.

Problems:

- User sees nothing until the entire agent loop completes
- Long-running tool calls (web search, RAG retrieval) appear frozen
- No feedback on which step is currently executing

### 2. No Progressive Disclosure
- All Thought/Action/Observation steps dumped as plain text
- Cannot collapse/expand individual reasoning steps
- Tool results (potentially large JSON) clutter the output
- No way to hide verbose details while keeping summary visible

### 3. No Visual Hierarchy
- No distinction between agent thinking, tool calls, and final answers
- No status indicators for in-progress operations
- No structured display for tool results (tables, JSON, lists)

### 4. Poor Development Experience
- Cannot inspect individual tool calls without modifying code
- No persistent log panel for debugging
- No keyboard shortcuts for common operations
- Cannot copy individual sections (just entire output)

### 5. Limited Extensibility
- Adding new display features requires rewriting print statements
- No component architecture for reusable UI elements
- No theming or customization support

## Proposed Solution: Textual TUI
### Why Textual

| Requirement          | Textual Capability                      |
|----------------------|-----------------------------------------|
| Streaming output     | Rich integration, reactive updates      |
| Collapsible sections | Tree, Collapsible widgets               |
| Keyboard navigation  | Built-in binding system                 |
| Async support        | Native asyncio integration              |
| Structured display   | DataTable, Pretty, JSON widgets         |
| Theming              | CSS-like styling system                 |
| Python-native        | Pure Python, no JS/browser overhead     |

## Target User Experience

+-------------------------------------------------------------------+
|  Research Assistant                        [F1:Help] [F2:Logs]    |
+-------------------------------------------------------------------+
|                                                                   |
|  You: Search for Python async patterns                            |
|                                                                   |
|  > Agent Response (streaming...)                                  |
|    +-- [done] Thought (click to expand)                           |
|    |     "I need to search for information about..."              |
|    +-- [running] Action: search_web                               |
|    |     Query: "Python async patterns best practices"            |
|    +-- [pending] Observation                                      |
|    +-- [pending] Answer                                           |
|                                                                   |
|  -----------------------------------------------------------------|
|  Previous: What is RAG?                                           |
|  > Agent Response (collapsed - click to expand)                   |
|                                                                   |
+-------------------------------------------------------------------+
| > Type your question...                              [Ctrl+L]     |
+-------------------------------------------------------------------+

Key Features:

- Streaming tokens: Text appears character-by-character as LLM generates
- Step status indicators: done, running, pending
- Collapsible tree: Expand/collapse any Thought/Action/Observation
- Keyboard shortcuts: F1 help, F2 logs, Ctrl+L clear, Ctrl+C copy
- Log panel (toggleable): Raw debug output, API calls, timing info

## Benefits
### For Development
- Faster debugging: See exactly where agent reasoning fails
- Reduced API costs: Identify prompt issues before full execution
- Better iteration: Modify and test without output archaeology

### For Learning
- Transparency: Understand ReAct loop step-by-step
- Inspection: Examine tool inputs/outputs in detail
- Documentation: Export sessions for learning logs

### For Future Phases
- Phase 2 (MCP): Visualize MCP server communication
- Phase 3 (RAG): Display retrieved chunks with relevance scores
- Phase 4 (A2A): Show inter-agent message flow

## Success Criteria
- Agent reasoning steps display in real-time as they execute
- Each Thought/Action/Observation is collapsible
- Tool results are formatted and expandable
- Final answer streams token-by-token
- Keyboard shortcuts work for common operations
- Log panel toggleable with F2 or Ctrl+L
- All existing agent functionality preserved

## References:

- https://textual.textualize.io/
- https://github.com/darrenburns/elia
- https://textual.textualize.io/guide/reactivity/
- https://textual.textualize.io/widgets/tree/
- https://textual.textualize.io/widgets/collapsible/
- https://textual.textualize.io/widgets/log/
- https://textual.textualize.io/widgets/rich_log/
