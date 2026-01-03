# Phase 2: Textual TUI Migration - Implementation Plan

## Overview

Replace the current REPL with a professional Textual-based TUI featuring streaming output, progressive disclosure, and visual hierarchy. This becomes the new **Phase 2**, pushing existing phases forward (MCP→3, RAG→4, A2A→5).

**Why P0 Priority**: Essential for debugging multi-step agent reasoning in later phases. Without real-time visibility into Thought/Action/Observation steps, developing MCP/RAG/A2A features will be significantly harder.

**User Experience Goals**:
- Streaming tokens appear character-by-character as LLM generates
- Thought/Action/Observation sections are collapsible/expandable
- Status indicators (pending/running/done) for each ReAct step
- Keyboard shortcuts: F1 help, F2 logs, Ctrl+L clear, Ctrl+C copy
- Toggleable debug log panel for development

**Migration Strategy**: Preserve REPL as `--repl` fallback, implement TUI incrementally, maintain all existing agent functionality.

## Architecture

```
ResearchAssistantApp (Textual)
├── Header (Static)
│   └── [F1:Help] [F2:Logs]
├── ConversationPanel (ScrollableContainer)
│   ├── QueryDisplay
│   ├── AgentResponseTree
│   │   ├── ThoughtNode (Collapsible, status indicator)
│   │   ├── ActionNode (Collapsible, status indicator)
│   │   ├── ObservationNode (Collapsible, status indicator)
│   │   └── AnswerNode (StreamingText)
│   └── ...previous conversations
├── InputArea (TextArea)
└── LogPanel (RichLog, toggleable)

Data Flow:
User Input → AsyncAgent.run_streaming(query)
          → Yields AgentEvent(type, content, metadata)
          → TUI creates/updates widgets
          → Visual feedback in real-time
```

## Critical Files

**New Files**:
- `src/tui/__init__.py` - TUI package
- `src/tui/app.py` - Main ResearchAssistantApp class
- `src/tui/widgets.py` - Custom widgets (ThoughtNode, ActionNode, etc.)
- `src/tui/events.py` - AgentEvent dataclass
- `src/agents/async_agent.py` - Async streaming version of Agent
- `tests/tui/test_widgets.py` - Widget tests
- `tests/tui/test_app.py` - App integration tests
- `tests/agents/test_async_agent.py` - Async agent tests

**Files to Modify**:
- `src/main.py` - Add `--tui`/`--repl` flags, route to appropriate UI
- `pyproject.toml` - Add textual and rich dependencies

**Documentation Files**:
- `docs/implementation_plans/phase-2.md` - This plan
- `docs/checklists/phase-2.md` - Task checklist
- `docs/learning-logs/phase-2-log.md` - Implementation narrative
- `docs/enhancements/developer-experience.md` - New enhancement category
- `CLAUDE.md` - Update phase structure
- `README.md` - Update roadmap

## Implementation Groups (TDD Workflow)

### GROUP 1: Phase Restructuring & Setup

**Goal**: Update documentation to reflect new phase structure, add dependencies

**Tasks**:
1. Save implementation plan to docs/implementation_plans/phase-2.md
2. Create docs/checklists/phase-2.md checklist
3. Update CLAUDE.md with new phase structure
4. Update README.md with Phase 2 status
5. Create docs/enhancements/developer-experience.md
6. Create docs/learning-logs/phase-2-log.md
7. Add textual and rich dependencies to pyproject.toml
8. Run uv sync to install dependencies

**Commits**:
- `docs: create phase 2 implementation plan and checklist`
- `docs: update CLAUDE.md with new phase structure`
- `docs: update README.md roadmap with Phase 2 TUI`
- `docs: add developer-experience enhancement category`
- `docs: create phase 2 learning log`
- `chore: add textual and rich dependencies`

### GROUP 2: Basic TUI Shell (No Streaming)

**Goal**: Create minimal Textual app that displays agent responses (synchronous)

**Test-Implement Pairs**:
1. Minimal app structure - App renders with header, input, conversation area
2. Static widgets - QueryDisplay and ResponseDisplay widgets
3. Main entry point routing - `--tui` and `--repl` flags
4. Wire up synchronous agent - Input submission calls agent.run()

**Manual Verification**: `uv run python src/main.py --tui`

### GROUP 3: Async Agent Foundation

**Goal**: Convert Agent to async (no streaming yet)

**Test-Implement Pairs**:
1. AsyncAgent class initialization
2. Async run method (non-streaming)
3. Update TUI to use async agent

### GROUP 4: Streaming LLM Tokens

**Goal**: Stream LLM response tokens character-by-character

**Test-Implement Pairs**:
1. AgentEvent dataclass
2. Streaming agent method with `stream=True`
3. StreamingText widget
4. Wire streaming to TUI

### GROUP 5: ReAct Step Visualization

**Goal**: Display Thought/Action/Observation as separate sections

**Test-Implement Pairs**:
1. ThoughtNode widget with status indicators
2. ActionNode and ObservationNode widgets
3. Update AsyncAgent to emit structured events
4. Event processing in TUI

### GROUP 6: Progressive Disclosure

**Goal**: Make sections collapsible

**Test-Implement Pairs**:
1. Collapsible wrapper
2. Click handlers
3. Default expanded state

### GROUP 7: Keyboard Navigation & Polish

**Goal**: Add keyboard shortcuts and styling

**Test-Implement Pairs**:
1. F1 help modal
2. F2 log panel toggle
3. Ctrl+L clear conversation
4. CSS styling

### GROUP 8: Documentation & Finalization

**Goal**: Document implementation, finalize Phase 2

**Tasks**:
1. Add docstrings to all public functions
2. Complete learning log
3. Update CLAUDE.md with Phase 2 patterns
4. Update developer-experience.md status to [Done]
5. Run quality checks (ruff, pytest, pyright)
6. Verify 66%+ coverage

## Key Technical Decisions

1. **Async/Await**: Required for non-blocking streaming and Textual's reactive model
2. **Event-Driven Architecture**: AsyncAgent yields AgentEvent for decoupling
3. **Textual Framework**: Python-native, async-first, rich widget library
4. **Preserve REPL**: Keep `--repl` flag for fallback and debugging
5. **OpenAI Streaming**: Use `stream=True` parameter (or simulate if unsupported)
6. **Widget Granularity**: Separate widgets for each ReAct step
7. **Testing Strategy**: Textual Pilot for app tests, mock async iterators

## POE API Streaming Compatibility

**Risk**: POE API may not support `stream=True`

**Mitigation**:
- Test streaming early in GROUP 4
- Fall back to simulated streaming if needed
- Document in troubleshooting guide

## Testing Strategy

**Unit Tests**: Widget rendering, event creation, async agent logic
**Integration Tests**: TUI app layout (Textual Pilot), event processing
**Mock Patterns**: Async iterators for streaming responses
**Coverage Target**: ≥66% (matching Phase 1)

## Success Criteria

**Functional**:
- ✅ TUI launches with default command
- ✅ Streaming tokens appear incrementally
- ✅ ReAct steps clearly separated
- ✅ Status indicators accurate
- ✅ Sections collapsible/expandable
- ✅ Keyboard shortcuts work
- ✅ REPL fallback works

**Quality**:
- ✅ Test coverage ≥66%
- ✅ All pre-commit hooks pass
- ✅ No API cost increase
- ✅ Documentation complete
- ✅ Zero breaking changes

## Code Examples

### Minimal Textual App
```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.containers import ScrollableContainer

class ResearchAssistantApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Static("Conversation area"))
        yield Input(placeholder="Type your question...")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value
        # Call agent and display result
```

### Mock Async Iterator
```python
async def async_iter(items):
    for item in items:
        yield item

@pytest.fixture
def mock_stream():
    return async_iter([
        Mock(choices=[Mock(delta=Mock(content="Hello"))]),
        Mock(choices=[Mock(delta=Mock(content=" world"))]),
    ])
```

### AgentEvent Dataclass
```python
from dataclasses import dataclass, field
from typing import Literal, Any

@dataclass
class AgentEvent:
    type: Literal["thought", "action", "observation", "answer", "token"]
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
```

## Workflow Tips

- Run tests after every change: `uv run pytest`
- Commit atomically: One test, one implementation
- Document as you go: Update learning log after major groups
- Manual test each GROUP to verify TUI behavior
- Test both `--tui` and `--repl` flags regularly
