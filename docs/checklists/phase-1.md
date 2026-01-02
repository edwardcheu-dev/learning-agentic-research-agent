# Phase 1: Basic Agentic Loop

## Overview
Build a single agent with ReAct-style reasoning loop (Think → Act → Observe → Repeat).

## GROUP 1: Setup ✅
- [x] Verify pytest runs successfully with no tests
- [x] Create tests/agents/test_tools.py with placeholder test

## GROUP 2: Tool System ✅
- [x] Test: Tool has name, description, function attributes
- [x] Implement: Basic Tool dataclass
- [x] Test: search_web tool returns mock search results
- [x] Implement: search_web placeholder tool
- [x] Test: save_note tool returns confirmation message
- [x] Implement: save_note placeholder tool
- [x] Test: get_all_tools returns complete tool list
- [x] Implement: get_all_tools function

## GROUP 3: Agent Core Structure ✅
- [x] Test: Agent initializes with client, max_iterations, tools list
- [x] Implement: Agent.__init__ with attributes
- [x] Test: Agent builds system prompt with ReAct instructions and tool descriptions
- [x] Implement: _build_system_prompt() method

## GROUP 4: ReAct Loop Components ✅
- [x] Test: Parse action from LLM response (extracts tool_name and input)
- [x] Test: Parser returns None if no Action found
- [x] Implement: _parse_action() method
- [x] Test: Execute tool by name
- [x] Test: Handle unknown tool errors
- [x] Implement: _execute_tool() method
- [x] Test: Format observation with label
- [x] Implement: _format_observation() method

## GROUP 5: Main Run Loop ✅
- [x] Test: Agent runs single iteration with mocked LLM response
- [x] Implement: run() method with loop logic
- [x] Test: Agent respects max_iterations limit
- [x] Verify/Refactor: Ensure loop respects limit (implementation already correct)
- [x] Test: Agent stops when final answer provided
- [x] Verify: Current implementation handles Answer detection (implementation already correct)

## GROUP 6: Integration
- [ ] Test: End-to-end workflow with mocked responses (Thought→Action→Observation→Answer)
- [ ] Implement: src/main.py with interactive REPL
- [ ] Manual verification: Run agent interactively in terminal

## GROUP 7: Documentation
- [ ] Add docstrings to all public functions
- [ ] Complete docs/learning-logs/phase-1-log.md
- [ ] Update CLAUDE.md with Phase 1 patterns
- [ ] Update MASTER_LOG.md with Phase 1 summary
- [ ] Run linting: `uv run ruff check . && uv run ruff format .`
- [ ] Final coverage: `uv run pytest --cov=src`
