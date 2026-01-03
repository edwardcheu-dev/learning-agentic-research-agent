# Phase 2: Textual TUI Migration - Learning Log

> **Phase Goal**: Replace REPL with professional Textual-based TUI featuring streaming output, progressive disclosure, and visual hierarchy.

## Overview

This log documents the implementation of Phase 2: migrating from the basic REPL to a full-featured TUI using the Textual framework. This phase is critical for debugging multi-step agent reasoning in later phases (MCP, RAG, A2A).

**Why Phase 2 before MCP/RAG/A2A**: Without real-time visibility into Thought/Action/Observation steps, developing and debugging multi-step workflows becomes significantly harder. The TUI provides essential developer experience improvements that pay dividends in all future phases.

## Key Decisions

### 1. Framework Choice: Textual

**Considered alternatives**:
- **curses**: Low-level, requires significant boilerplate, poor async support
- **Rich**: Great for formatted output, but not a full TUI framework
- **Electron/web-based**: Heavy dependency, requires frontend skills, browser overhead

**Why Textual**:
- Python-native (no JavaScript required)
- Async-first architecture (perfect for streaming)
- Rich widget library (Tree, Collapsible, RichLog)
- CSS-like styling system
- Active development and good documentation
- Used in production tools (e.g., Elia chat client)

### 2. Architecture: Event-Driven

**Decision**: AsyncAgent yields AgentEvent stream instead of returning single string

**Rationale**:
- Decouples agent logic from UI rendering
- Easy to add new event types (e.g., MCP server events, RAG retrieval)
- Testable without running full TUI
- Follows reactive programming patterns in Textual

### 3. Migration Strategy: Preserve REPL

**Decision**: Keep original REPL with `--repl` flag, default to TUI

**Rationale**:
- Safety net during development
- Useful for debugging TUI issues
- Simpler interface for quick testing
- Backwards compatibility for existing workflows

## Implementation Progress

### GROUP 1: Phase Restructuring & Setup ✅

**What We Built**:
Set up the Phase 2 foundation by restructuring project documentation and installing TUI dependencies.

**Completed Tasks**:
- [x] Created comprehensive implementation plan (docs/implementation_plans/phase-2.md)
- [x] Created detailed checklist with 8 GROUPs (docs/checklists/phase-2.md)
- [x] Updated CLAUDE.md - inserted Phase 2 (TUI), pushed MCP→3, RAG→4, A2A→5
- [x] Updated README.md with new 5-phase roadmap
- [x] Created developer-experience.md enhancement category (new DX tracking)
- [x] Created this learning log stub
- [x] Added `textual>=1.0.0` and `rich>=13.0.0` to pyproject.toml dependencies
- [x] Ran `uv sync` - installed textual 7.0.0 + 4 supporting packages

**Key Decisions**:

1. **Phase Insertion vs Renumbering**: Chose to insert Phase 2 and renumber existing phases (2→3, 3→4, 4→5) rather than making TUI Phase 5. Rationale: TUI is essential for debugging multi-step reasoning in MCP/RAG/A2A phases.

2. **Documentation First**: Created full implementation plan with documentation steps and context management workflow before any code. Ensures consistency with Phase 1 patterns and /start-phase workflow.

3. **Enhancement Category**: Created new `developer-experience.md` category alongside existing schema-validation, agent-robustness, and observability categories. Captures DX improvements that don't fit other categories.

**Dependencies Added**:
```toml
"rich>=13.0.0",      # Terminal formatting (Textual dependency)
"textual>=1.0.0",    # TUI framework
```

Installed packages:
- textual==7.0.0 (main TUI framework)
- linkify-it-py==2.0.3 (link detection for rich text)
- mdit-py-plugins==0.5.0 (markdown-it plugins)
- uc-micro-py==1.0.3 (Unicode utilities)

**Commits**:
- `c3baf68`: docs: create Phase 2 implementation plan and setup
- `bfdf9bf`: docs: update phase 2 plan with documentation steps and context management

**Challenges**:
None - GROUP 1 was purely documentation and dependency setup.

**Next Steps**:
GROUP 2 will create the basic Textual TUI shell (no streaming yet) with synchronous agent integration.

### GROUP 2: Basic TUI Shell (No Streaming) ✅

**What We Built**:
Created a minimal Textual TUI application that displays agent responses synchronously (no streaming yet). Implemented CLI argument parsing to support both TUI and REPL modes, preserving backward compatibility.

**Completed Tasks**:
- [x] Test: App renders with header, input, conversation area (tests/tui/test_app.py)
- [x] Implement: ResearchAssistantApp class with basic layout (src/tui/app.py)
- [x] Test: QueryDisplay and ResponseDisplay widgets (tests/tui/test_widgets.py)
- [x] Implement: Custom widgets for displaying conversation (src/tui/widgets.py)
- [x] Test: CLI argument parsing with --tui/--repl flags (tests/test_main.py)
- [x] Implement: parse_args(), run_tui(), run_repl() functions (src/main.py)
- [x] Test: Input submission triggers agent.run() (tests/tui/test_app.py)
- [x] Implement: on_input_submitted() event handler (src/tui/app.py)
- [x] Manual verification: Tested live TUI with agent interaction

**Key Decisions**:

1. **Circular Import Resolution**: Created src/client.py to break circular dependency
   - **Problem**: src/tui/app.py needed create_client() from src/main.py, but src/main.py imports ResearchAssistantApp from src/tui/app.py
   - **Solution**: Extracted create_client() to new src/client.py module
   - **Impact**: Clean separation of concerns, easier testing

2. **Testing Strategy**: Direct event invocation instead of pilot simulation
   - **Challenge**: pilot.press("enter") wasn't triggering Input.Submitted events in test mode
   - **Solution**: Create Input.Submitted event manually and call on_input_submitted() directly
   - **Benefit**: More reliable tests, explicit event flow

3. **Widget Inheritance**: Extend textual.widgets.Static for simplicity
   - **Choice**: QueryDisplay and ResponseDisplay inherit from Static widget
   - **Rationale**: Simple text display, leverage Rich markup for styling
   - **Trade-off**: Less customization vs faster implementation

4. **Pytest-Asyncio Configuration**: Added asyncio_mode = "auto" to pyproject.toml
   - **Reason**: Textual tests require async/await support
   - **Setup**: Added pytest-asyncio>=0.25.2 dependency
   - **Benefit**: Clean async test syntax without manual fixtures

**Code Highlights**:

```python
# src/tui/app.py - Minimal Textual App
class ResearchAssistantApp(App):
    """Main TUI application for the research assistant."""

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        client = create_client()
        self.agent = Agent(client=client, max_iterations=DEFAULT_MAX_ITERATIONS)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ScrollableContainer(id="conversation")
        yield Input(placeholder="Type your question...")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission."""
        query = event.value
        if not query.strip():
            return

        # Clear input and display query
        self.query_one(Input).value = ""
        conversation = self.query_one("#conversation")
        conversation.mount(QueryDisplay(query))

        # Run agent and display response
        response = self.agent.run(query)
        conversation.mount(ResponseDisplay(response))
```

```python
# src/tui/widgets.py - Custom Widgets with Rich Markup
class QueryDisplay(Static):
    """Widget to display user queries."""
    def __init__(self, query: str) -> None:
        super().__init__(f"[bold cyan]You:[/bold cyan] {query}")

class ResponseDisplay(Static):
    """Widget to display agent responses."""
    def __init__(self, response: str) -> None:
        super().__init__(f"[bold green]Agent:[/bold green] {response}")
```

```python
# src/main.py - CLI Argument Parsing
def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Research Assistant - Multi-agent AI system"
    )
    parser.add_argument("--tui", action="store_const", const="tui", dest="mode",
                        help="Launch the Textual TUI interface (default)")
    parser.add_argument("--repl", action="store_const", const="repl", dest="mode",
                        help="Launch the classic REPL interface")
    parser.set_defaults(mode="tui")
    return parser.parse_args(args)

def main() -> None:
    """Main entry point - parse arguments and launch appropriate interface."""
    args = parse_args()
    if args.mode == "repl":
        run_repl()
    else:
        run_tui()
```

**Challenges Encountered**:

1. **Circular Import Between main.py and app.py**
   - **Symptom**: `ImportError: cannot import name 'ResearchAssistantApp' from partially initialized module`
   - **Root Cause**: main.py → tui.app → main.create_client() → main.py
   - **Solution**: Extracted create_client() to new client.py module
   - **Learning**: Keep module dependencies acyclic; extract shared utilities early

2. **Mock Patching Location**
   - **Issue**: `@patch("src.client.create_client")` didn't work, mocks weren't applied
   - **Fix**: Changed to `@patch("src.tui.app.create_client")` (where it's imported)
   - **Learning**: Patch where functions are used, not where they're defined

3. **Textual Event Simulation in Tests**
   - **Issue**: `await pilot.press("enter")` didn't trigger on_input_submitted()
   - **Fix**: Created Input.Submitted event manually: `event = Input.Submitted(input_widget, value="query")`
   - **Learning**: Direct event invocation more reliable for unit tests; pilot better for integration tests

**Testing Insights**:

1. **Test Structure**: Mirrored src/ structure in tests/ (tests/tui/ for src/tui/)
2. **Mock Strategy**: Patched create_client() and Agent class to avoid API calls
3. **Coverage**: All 8 checklist items have corresponding tests (5 test files created)
4. **Test Count**: Added 7 new tests across test_app.py, test_widgets.py, test_main.py
5. **Assertion Style**: Verified both behavior (mock calls) and state (widget presence)

**Commits**:
- `82719b4`: test: add test for basic TUI app layout
- `f4a8b6a`: feat: create basic TUI app with header, input, and conversation area
- `50c0a6f`: test: add tests for QueryDisplay and ResponseDisplay widgets
- `eee33cb`: feat: create QueryDisplay and ResponseDisplay widgets
- `a464d19`: test: add tests for CLI argument parsing and mode selection
- `50b146a`: feat: add CLI argument parsing with --tui and --repl modes
- `12ec6dd`: test: add test for input submission and agent interaction
- `eb0d4bd`: feat: implement input submission handler with agent integration

**Next Steps**:
GROUP 3 will create AsyncAgent foundation (async/await without streaming yet) to prepare for GROUP 4's token streaming.

### GROUP 3: Async Agent Foundation

(To be filled in during implementation)

### GROUP 4: Streaming LLM Tokens

(To be filled in during implementation)

### GROUP 5: ReAct Step Visualization

(To be filled in during implementation)

### GROUP 6: Progressive Disclosure

(To be filled in during implementation)

### GROUP 7: Keyboard Navigation & Polish

(To be filled in during implementation)

### GROUP 8: Documentation & Finalization

(To be filled in during implementation)

## Code Highlights

(To be filled in with key code snippets as implementation progresses)

## Challenges Encountered

(To be filled in with obstacles and how they were overcome)

## Testing Insights

(To be filled in with testing patterns and discoveries)

## What's Next

After Phase 2 completion:
- **Phase 3 (MCP Integration)**: Connect TUI to real MCP servers for filesystem, memory, vector store
- **Phase 4 (RAG System)**: Display retrieved chunks with relevance scores in TUI
- **Phase 5 (A2A Multi-Agent)**: Visualize inter-agent message flow in TUI

## References

- [Implementation Plan](../implementation_plans/phase-2.md)
- [Checklist](../checklists/phase-2.md)
- [Textual Documentation](https://textual.textualize.io/)
- [Elia Reference Implementation](https://github.com/darrenburns/elia)
- [TUI Specification](../../specs.md)
