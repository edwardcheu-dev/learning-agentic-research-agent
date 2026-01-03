# Developer Experience Enhancements

This category tracks improvements to developer workflow, debugging tools, and user interface enhancements that make building and maintaining the Research Assistant easier.

## Textual TUI [P0] [Planned]

**Problem**: Current REPL lacks visibility into agent reasoning, no streaming support, poor debugging experience for multi-step workflows.

The Phase 1 REPL implementation:
- Blocks until full agent response is ready (no progress indication)
- Dumps all Thought/Action/Observation steps as plain text (no visual hierarchy)
- Cannot collapse/expand sections or inspect individual tool calls
- No keyboard shortcuts or interactive navigation
- Difficult to debug multi-iteration ReAct loops

These limitations become critical blockers for Phases 3-5:
- **Phase 3 (MCP)**: Need to visualize MCP server communication and tool execution
- **Phase 4 (RAG)**: Need to display retrieved chunks with relevance scores
- **Phase 5 (A2A)**: Need to show inter-agent message flow

**Proposed Solution**: Replace with Textual-based TUI featuring:
- **Real-time streaming**: LLM tokens appear character-by-character as they're generated
- **Progressive disclosure**: Collapsible Thought/Action/Observation sections
- **Status indicators**: Visual feedback (pending/running/done) for each ReAct step
- **Keyboard shortcuts**: F1 help, F2 logs, Ctrl+L clear, Ctrl+C copy
- **Toggleable debug panel**: RichLog widget for development and troubleshooting

**Architecture**:
```
ResearchAssistantApp (Textual)
├── Header (F1:Help, F2:Logs)
├── ConversationPanel (ScrollableContainer)
│   └── AgentResponseTree (collapsible Thought/Action/Observation nodes)
├── InputArea (TextArea)
└── LogPanel (RichLog, toggleable)

Data Flow:
User Input → AsyncAgent.run_streaming(query)
          → Yields AgentEvent(type, content, metadata)
          → TUI creates/updates widgets
```

**Benefits**:
- **Faster debugging**: See exactly where agent reasoning fails (which iteration, which tool)
- **Better learning experience**: Understand ReAct loop step-by-step with clear visual separation
- **Reduced API costs**: Identify prompt issues by inspecting intermediate steps before full execution
- **Foundation for future phases**: Architecture extends naturally to MCP/RAG/A2A visualization
- **Professional UX**: Demonstrates best practices for TUI design in Python

**Considerations**:
- **Async/await complexity**: Requires converting Agent to async, adds testing complexity
- **Preserve REPL**: Keep `--repl` flag for simplicity and fallback
- **Textual learning curve**: New framework for team, needs documentation and examples
- **POE API streaming**: May not support `stream=True` parameter (fallback: simulated streaming)
- **Testing TUI**: Requires Textual Pilot (async test framework) - different from current unittest patterns

**Implementation Approach**:
- **Phase 2 promotion**: Elevated from enhancement to Phase 2 of MVP roadmap
- **Incremental delivery**: 8 implementation groups from basic shell → full-featured TUI
- **TDD workflow**: Maintain test-first development with Textual Pilot
- **Migration strategy**: Preserve REPL as `--repl` flag, default to TUI

**References**:
- https://textual.textualize.io/ - Official Textual documentation
- https://github.com/darrenburns/elia - Reference TUI implementation (Elia chat client)
- https://textual.textualize.io/guide/reactivity/ - Reactive programming in Textual
- https://textual.textualize.io/widgets/tree/ - Tree widget for hierarchical data
- https://textual.textualize.io/widgets/collapsible/ - Collapsible sections
- https://textual.textualize.io/widgets/rich_log/ - Debug logging widget
- [specs.md](../../specs.md) - Full TUI specification and user experience goals

**Status**: Promoted to Phase 2 of MVP roadmap. See [docs/implementation_plans/phase-2.md](../implementation_plans/phase-2.md) for implementation plan.
