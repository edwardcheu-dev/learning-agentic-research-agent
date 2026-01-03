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

### GROUP 3: Async Agent Foundation ✅

**What We Built**:
Created an async version of the Agent class (AsyncAgent) and migrated the TUI to use async/await patterns. This establishes the foundation for streaming LLM tokens in GROUP 4 while maintaining identical behavior to the synchronous agent.

**Completed Tasks**:
- [x] Test: AsyncAgent initializes with same params as Agent (tests/agents/test_async_agent.py)
- [x] Implement: AsyncAgent class with __init__, tools, max_iterations (src/agents/async_agent.py)
- [x] Test: AsyncAgent.run() returns same result as Agent.run() (async test with AsyncMock)
- [x] Implement: async def run(self, query: str) -> str method (converted Agent.run to async)
- [x] Test: TUI app uses AsyncAgent instead of Agent (tests/tui/test_app.py)
- [x] Implement: Updated app.py to use AsyncAgent and async on_input_submitted() (src/tui/app.py)
- [x] Verify: Behavior identical to GROUP 2 but using async/await (manual TUI test passed)

**Key Decisions**:

1. **Code Reuse**: Copied Agent implementation to AsyncAgent instead of inheritance
   - **Rationale**: AsyncAgent.run() is fundamentally different (async/await) from Agent.run()
   - **Trade-off**: Some code duplication vs cleaner separation of sync/async concerns
   - **Benefit**: Easier to add streaming in GROUP 4 without affecting synchronous Agent

2. **Textual Event Handlers Support Async**: on_input_submitted() can be async
   - **Discovery**: Textual natively supports async event handlers
   - **Impact**: No need for run_in_executor() or complex threading
   - **Pattern**: `async def on_input_submitted(self, event: Input.Submitted) -> None`

3. **Mock Strategy**: Use AsyncMock for async functions
   - **Pattern**: `mock_agent.run = AsyncMock(return_value="response")`
   - **Testing**: `await app.on_input_submitted(event)` to wait for async handler
   - **Assertion**: `mock_agent.run.assert_called_once_with("query")`

**Code Highlights**:

```python
# src/agents/async_agent.py - Async ReAct Agent
class AsyncAgent:
    """An async ReAct-style reasoning agent."""

    def __init__(self, client: Any, max_iterations: int) -> None:
        """Initialize the async agent."""
        self.client = client
        self.max_iterations = max_iterations
        self.tools = get_all_tools()

    async def run(self, query: str) -> str:
        """Run the agent on a query using ReAct loop (async version)."""
        # Build system prompt
        system_prompt = self._build_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
        conversation = f"User: {query}\n\n"

        # ReAct loop
        for iteration in range(self.max_iterations):
            # Call LLM (async) - KEY DIFFERENCE from Agent
            response = await self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=DEFAULT_MAX_TOKENS,
            )
            llm_response = response.choices[0].message.content
            conversation += f"{llm_response}\n\n"

            # Parse action and execute tool (synchronous, unchanged)
            action = self._parse_action(llm_response)
            if action is None:
                break
            tool_name, tool_input = action
            tool_result = self._execute_tool(tool_name, tool_input)
            observation = self._format_observation(tool_result)
            conversation += f"{observation}\n\n"

            # Add to conversation for next iteration
            messages.append({"role": "assistant", "content": llm_response})
            messages.append({"role": "user", "content": observation})

        return conversation.strip()
```

```python
# src/tui/app.py - Updated to use AsyncAgent
from src.agents.async_agent import AsyncAgent  # Changed from Agent

class ResearchAssistantApp(App):
    def __init__(self) -> None:
        """Initialize the TUI app with async agent."""
        super().__init__()
        client = create_client()
        self.agent = AsyncAgent(client=client, max_iterations=DEFAULT_MAX_ITERATIONS)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission (async)."""
        query = event.value
        if not query.strip():
            return

        # Clear input and display query
        self.query_one(Input).value = ""
        conversation = self.query_one("#conversation")
        conversation.mount(QueryDisplay(query))

        # Run agent and display response (async) - KEY DIFFERENCE
        response = await self.agent.run(query)
        conversation.mount(ResponseDisplay(response))
```

```python
# tests/agents/test_async_agent.py - Testing Async Agent
@pytest.mark.asyncio
async def test_async_agent_run_returns_conversation():
    """AsyncAgent.run() should return conversation with ReAct steps."""
    mock_client = AsyncMock()  # Use AsyncMock for async client
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        "Thought: I should search\nAction: search_web: python tutorials"
    )
    mock_client.chat.completions.create.return_value = mock_response

    agent = AsyncAgent(client=mock_client, max_iterations=3)
    result = await agent.run("Find me python tutorials")  # await async method

    assert mock_client.chat.completions.create.called
    assert "Observation:" in result
    assert "MOCK SEARCH RESULTS" in result
```

```python
# tests/tui/test_app.py - Testing Async TUI
@patch("src.tui.app.create_client")
@patch("src.tui.app.AsyncAgent")  # Changed from Agent
async def test_input_submission_calls_agent_and_displays_result(
    self, mock_agent_class, mock_create_client
):
    """Test that submitting input calls agent.run() and displays the result."""
    mock_client = Mock()
    mock_create_client.return_value = mock_client
    mock_agent = AsyncMock()  # Use AsyncMock for async agent
    mock_agent.run = AsyncMock(return_value="This is the agent's answer.")
    mock_agent_class.return_value = mock_agent

    app = ResearchAssistantApp()
    async with app.run_test():
        input_widget = app.query_one("Input")
        event = Input.Submitted(input_widget, value="What is machine learning?")
        await app.on_input_submitted(event)  # await async handler

        mock_agent.run.assert_called_once_with("What is machine learning?")
        # Verify displays were added
        assert len(app.query("#conversation QueryDisplay")) == 1
        assert len(app.query("#conversation ResponseDisplay")) == 1
```

**Challenges Encountered**:

1. **Pre-commit Hook Blocking Failing Tests**
   - **Issue**: Test for AsyncAgent.run() failed because method didn't exist yet
   - **Fix**: Committed test and implementation together in single commit
   - **Learning**: TDD with pre-commit hooks requires committing pairs (test + impl) together

2. **Updating Existing Tests**
   - **Issue**: Old test patched `src.tui.app.Agent` which no longer exists
   - **Fix**: Updated all tests to patch `src.tui.app.AsyncAgent` and use AsyncMock
   - **Learning**: Migration requires updating all related tests, not just new ones

3. **AsyncOpenAI vs OpenAI Client** ⚠️ **Critical Fix**
   - **Issue**: `TypeError: object ChatCompletion can't be used in 'await' expression`
   - **Root Cause**: `openai.OpenAI` client is synchronous, can't be awaited
   - **Fix**: Created `create_async_client()` using `openai.AsyncOpenAI`
   - **Code Change**: Updated `src/tui/app.py` to use `create_async_client()`
   - **Learning**: OpenAI SDK provides separate async client for async/await support
   - **Impact**: TUI now correctly uses async client, making agent.run() awaitable

**Testing Insights**:

1. **Async Test Patterns**:
   - Use `@pytest.mark.asyncio` decorator for async tests
   - Use `AsyncMock()` for mocking async functions/methods
   - Use `await` when calling async methods in tests
   - Assert on AsyncMock the same way as regular Mock

2. **Test Coverage**: Added 3 new tests
   - test_async_agent_initialization
   - test_async_agent_run_returns_conversation
   - test_app_uses_async_agent

3. **Full Test Suite**: All 37 tests passing (0 failures, 4 deselected integration tests)

**Commits**:
- `d111baf`: test: add test for AsyncAgent initialization
- `8d70951`: feat: create AsyncAgent class with initialization
- `002cec4`: test: add test for AsyncAgent.run() method
- `3c102ce`: test: add test for TUI app using AsyncAgent
- `7cd23d9`: fix: use AsyncOpenAI client for async agent support (CRITICAL FIX)

**Next Steps**:
GROUP 4 will implement streaming LLM tokens by modifying AsyncAgent.run() to yield AgentEvent objects incrementally, and creating a StreamingText widget to display tokens as they arrive.

**Verification**:
Manually ran `uv run python src/main.py --tui` to verify:
- TUI renders correctly with header, input, conversation area, footer
- App initializes with AsyncAgent
- No runtime errors or async/await issues
- Behavior identical to GROUP 2 (synchronous version)

### GROUP 4: Streaming LLM Tokens ✅

**What We Built**:
Implemented character-by-character streaming of LLM responses in the TUI. Created an event-driven architecture where AsyncAgent yields AgentEvent objects for each token, and the TUI displays them incrementally using a StreamingText widget.

**Completed Tasks**:
- [x] Test: AgentEvent has type, content, metadata attributes (tests/tui/test_events.py)
- [x] Implement: AgentEvent dataclass with type/content/metadata (src/tui/events.py)
- [x] Test: run_streaming() yields AgentEvent for each token (tests/agents/test_async_agent.py)
- [x] Implement: AsyncAgent.run_streaming() with stream=True (src/agents/async_agent.py)
- [x] Test: StreamingText appends tokens incrementally (tests/tui/test_widgets.py)
- [x] Implement: StreamingText widget with append_token() method (src/tui/widgets.py)
- [x] Test: App processes AgentEvent stream and updates StreamingText (tests/tui/test_app.py)
- [x] Implement: Streaming event loop in app.py (async for event in agent.run_streaming())
- [x] Manual verification: Verified token-by-token display in TUI

**Key Decisions**:

1. **Event-Driven Architecture**: AgentEvent dataclass for decoupling
   - **Pattern**: AsyncAgent yields `AgentEvent(type, content, metadata)` instead of strings
   - **Benefit**: Easy to add new event types (thought, action, observation) in GROUP 5
   - **Type Safety**: Literal type for event types prevents typos

2. **OpenAI Streaming API**: Use `stream=True` parameter
   - **API Call**: `await client.chat.completions.create(..., stream=True)`
   - **Response**: Returns async iterator of chunks with delta.content
   - **Token Extraction**: `if hasattr(delta, "content") and delta.content:`

3. **Widget Update Pattern**: Call update() after appending tokens
   - **Method**: `self.update(self._content)` triggers Textual re-render
   - **State**: Maintain `_content` string internally, update widget on each token
   - **Reactivity**: Textual automatically re-renders when update() is called

**Code Highlights**:

```python
# src/tui/events.py - Event Dataclass
from dataclasses import dataclass, field
from typing import Any, Literal

@dataclass
class AgentEvent:
    """Event emitted by AsyncAgent during streaming execution."""
    type: Literal["thought", "action", "observation", "answer", "token"]
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
```

```python
# src/agents/async_agent.py - Streaming Method
async def run_streaming(self, query: str) -> AsyncGenerator[AgentEvent, None]:
    """Run the agent on a query with streaming token events."""
    # ... build system prompt and messages ...

    for iteration in range(self.max_iterations):
        # Call LLM with streaming enabled
        stream = await self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=DEFAULT_MAX_TOKENS,
            stream=True,  # Enable streaming
        )

        # Collect full response while yielding tokens
        llm_response = ""
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                token = delta.content
                llm_response += token

                # Yield token event
                yield AgentEvent(
                    type="token",
                    content=token,
                    metadata={"iteration": iteration},
                )

        # Parse action, execute tool, etc...
```

```python
# src/tui/widgets.py - StreamingText Widget
class StreamingText(Static):
    """Widget that displays text incrementally as tokens arrive."""

    def __init__(self) -> None:
        """Initialize StreamingText with empty content."""
        super().__init__("")
        self._content = ""

    def append_token(self, token: str) -> None:
        """Append a token to the streaming text."""
        self._content += token
        self.update(self._content)  # Trigger Textual re-render
```

```python
# src/tui/app.py - Streaming Event Loop
async def on_input_submitted(self, event: Input.Submitted) -> None:
    """Handle user input submission with streaming."""
    query = event.value
    if not query.strip():
        return

    # Clear input and display query
    self.query_one(Input).value = ""
    conversation = self.query_one("#conversation")
    conversation.mount(QueryDisplay(query))

    # Create streaming text widget
    streaming_widget = StreamingText()
    conversation.mount(streaming_widget)

    # Stream agent response token by token
    async for agent_event in self.agent.run_streaming(query):
        if agent_event.type == "token":
            streaming_widget.append_token(agent_event.content)
```

**Challenges Encountered**:

1. **Mock Strategy for Async Generators**
   - **Issue**: AsyncMock wraps async generator in coroutine, can't use `async for`
   - **Fix**: Mock run_streaming as plain async generator function, not AsyncMock
   - **Pattern**: `mock_agent.run_streaming = async_generator_func` (not `AsyncMock(return_value=...)`)

2. **Old Tests Breaking After Streaming Migration**
   - **Issue**: Previous tests expected agent.run(), now app uses agent.run_streaming()
   - **Fix**: Updated all TUI tests to mock run_streaming() with token events
   - **Learning**: API changes require updating all dependent tests

3. **Line Length Violation in Docstring**
   - **Issue**: Ruff enforced 88-character line limit in docstrings
   - **Fix**: Shortened docstring from 93 to 62 characters
   - **Tool**: Ruff auto-fix didn't handle docstrings, required manual edit

**Testing Insights**:

1. **Async Generator Mocking Pattern**:
   ```python
   async def mock_streaming_events(query):
       yield AgentEvent(type="token", content="Hello")
       yield AgentEvent(type="token", content=" world")

   mock_agent.run_streaming = mock_streaming_events  # Direct assignment
   ```

2. **Test Coverage**: Added 4 new tests
   - test_agent_event_has_required_attributes
   - test_async_agent_run_streaming_yields_agent_events
   - test_streaming_text_appends_tokens_incrementally
   - test_app_processes_streaming_events

3. **Full Test Suite**: All 47 tests passing (0 failures, 4 deselected integration tests)

**Commits**:
- `faee30f`: test: add tests for AgentEvent dataclass
- `b24c1dd`: feat: implement AsyncAgent.run_streaming() with token-by-token events
- `0b5d7ee`: test: add test for StreamingText widget
- `86f0aa6`: test: add test for app processing streaming events / feat: implement streaming event loop in TUI app

**Next Steps**:
GROUP 5 will implement ReAct step visualization by emitting separate event types (thought, action, observation) and creating specialized widgets (ThoughtNode, ActionNode, ObservationNode) with status indicators.

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
