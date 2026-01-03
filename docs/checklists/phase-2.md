# Phase 2: Textual TUI Migration

## Overview
Replace REPL with professional Textual-based TUI featuring streaming output, progressive disclosure, and visual hierarchy.

## GROUP 1: Phase Restructuring & Setup ✅
- [x] Save implementation plan to docs/implementation_plans/phase-2.md
- [x] Create docs/checklists/phase-2.md checklist
- [x] Update CLAUDE.md with new phase structure (Phase 2 = TUI, push others forward)
- [x] Update README.md with Phase 2 status
- [x] Create docs/enhancements/developer-experience.md enhancement category
- [x] Create docs/learning-logs/phase-2-log.md stub
- [x] Add textual>=1.0.0 and rich>=13.0.0 to pyproject.toml dependencies
- [x] Run `uv sync` to install new dependencies
- [x] Verify dependencies installed successfully

## GROUP 2: Basic TUI Shell (No Streaming)
- [ ] Test: App renders with header, input, conversation area
- [ ] Implement: Create src/tui/app.py with ResearchAssistantApp class
- [ ] Test: QueryDisplay renders user query
- [ ] Implement: Create src/tui/widgets.py with QueryDisplay, ResponseDisplay
- [ ] Test: `--tui` flag launches TUI, `--repl` launches REPL
- [ ] Implement: Modify src/main.py with argparse and run_tui()/run_repl() functions
- [ ] Test: Input submission calls agent.run() and displays result
- [ ] Implement: Add on_input_submitted() handler in app.py
- [ ] Manual verification: Run `uv run python src/main.py --tui` and test query
- [ ] Update learning log with GROUP 2 progress

## GROUP 3: Async Agent Foundation
- [ ] Test: AsyncAgent initializes with same params as Agent
- [ ] Implement: Create src/agents/async_agent.py with AsyncAgent class
- [ ] Test: AsyncAgent.run() returns same result as Agent.run()
- [ ] Implement: Add async def run(self, query: str) -> str method
- [ ] Test: TUI app uses AsyncAgent instead of Agent
- [ ] Implement: Update app.py to use await self.agent.run(query)
- [ ] Verify: Behavior identical to GROUP 2 but using async/await
- [ ] Update learning log with GROUP 3 progress

## GROUP 4: Streaming LLM Tokens
- [ ] Test: AgentEvent has type, content, metadata attributes
- [ ] Implement: Create src/tui/events.py with AgentEvent dataclass
- [ ] Test: run_streaming() yields AgentEvent for each token
- [ ] Implement: Add async def run_streaming() to AsyncAgent with stream=True
- [ ] Test: StreamingText appends tokens incrementally
- [ ] Implement: Add StreamingText widget with append_token() method
- [ ] Test: App processes AgentEvent stream and updates StreamingText
- [ ] Implement: Add event loop in app.py: async for event in agent.run_streaming()
- [ ] Manual verification: Verify text appears character-by-character
- [ ] Update learning log with GROUP 4 progress

## GROUP 5: ReAct Step Visualization
- [ ] Test: ThoughtNode displays content and status indicator
- [ ] Implement: Add ThoughtNode widget with status (pending/running/done)
- [ ] Test: ActionNode shows tool name/input, ObservationNode shows result
- [ ] Implement: Add ActionNode and ObservationNode classes
- [ ] Test: AsyncAgent emits separate events for thought/action/observation
- [ ] Implement: Modify run_streaming() to yield typed events
- [ ] Test: TUI creates appropriate node type for each event
- [ ] Implement: Add event handler to create ThoughtNode/ActionNode/ObservationNode
- [ ] Manual verification: Verify separate sections with status indicators
- [ ] Update learning log with GROUP 5 progress

## GROUP 6: Progressive Disclosure
- [ ] Test: Nodes can be collapsed/expanded
- [ ] Implement: Add Collapsible wrappers to ReAct nodes
- [ ] Test: Click toggles expand/collapse
- [ ] Implement: Add click event handlers to nodes
- [ ] Test: Latest step expanded by default, previous steps collapsed
- [ ] Implement: Add logic to auto-collapse previous nodes
- [ ] Manual verification: Click sections to verify expand/collapse
- [ ] Update learning log with GROUP 6 progress

## GROUP 7: Keyboard Navigation & Polish
- [ ] Test: F1 displays help screen with keybindings
- [ ] Implement: Add action_show_help() method
- [ ] Test: F2 toggles visibility of RichLog widget
- [ ] Implement: Add action_toggle_logs() method and RichLog widget
- [ ] Test: Ctrl+L clears conversation panel
- [ ] Implement: Add action_clear_conversation() method
- [ ] Create: Add CSS styling for status indicators (green/yellow/gray)
- [ ] Manual verification: Test all keyboard shortcuts and visual polish
- [ ] Update learning log with GROUP 7 progress

## GROUP 8: Documentation & Finalization
- [ ] Add docstrings to src/tui/app.py public functions
- [ ] Add docstrings to src/tui/widgets.py public functions
- [ ] Add docstrings to src/tui/events.py
- [ ] Add docstrings to src/agents/async_agent.py public functions
- [ ] Complete docs/learning-logs/phase-2-log.md with full narrative
- [ ] Update CLAUDE.md with Phase 2 patterns (async/await, event-driven, Textual)
- [ ] Update docs/enhancements/developer-experience.md status to [Done]
- [ ] Run linting: `uv run ruff check . && uv run ruff format .`
- [ ] Run tests with coverage: `uv run pytest --cov=src`
- [ ] Run type checking: `uv run pyright`
- [ ] Final coverage verification (target: ≥66%)
- [ ] Final update to learning log with reflection
