Phase 1: Basic Agentic Loop - Implementation Plan

Overview

Build a single ReAct-style agent (Think → Act → Observe → Repeat) with placeholder tools to
establish the foundation for the research assistant system.

User Preferences:
- Tools: Placeholder implementations only (mock data)
- Output: Visible reasoning (show Thought/Action/Observation)
- Safety: Max 3 iterations to prevent runaway costs

Architecture

Agent
├── OpenAI Client (POE API, gpt-5-mini)
├── Tools (placeholder search_web, save_note)
└── ReAct Loop
    ├── Think: LLM generates reasoning
    ├── Act: Parse and execute tool
    ├── Observe: Format tool output
    └── Repeat: Loop until done or max iterations

Critical Files

- src/agents/tools.py - Tool class and placeholder implementations
- src/agents/agent.py - Agent class with ReAct loop
- tests/agents/test_tools.py - Tool tests
- tests/agents/test_agent.py - Agent tests
- tests/agents/test_integration.py - End-to-end tests
- src/main.py - Interactive entry point

Implementation Groups (TDD Workflow)

GROUP 1: Project Setup

Goal: Verify testing infrastructure works

1. Run uv run pytest to verify no tests found (baseline)
2. Create tests/agents/test_tools.py with placeholder test
3. Commit: test: verify pytest test discovery works

GROUP 2: Tool System

Goal: Create Tool class and placeholder implementations

Test-Implement Pairs:

1. Tool class structure
- Test: Tool has name, description, function attributes
- Implement: Basic Tool dataclass
- Commits: test: then feat: implement basic Tool class structure
2. search_web placeholder
- Test: Returns mock search results containing query
- Implement: Function returning "MOCK SEARCH RESULTS for '{query}'"
- Commits: test: then feat: implement placeholder search_web tool
3. save_note placeholder
- Test: Returns confirmation message
- Implement: Function returning "MOCK SAVE: Note '{title}' saved"
- Commits: test: then feat: implement placeholder save_note tool
4. get_all_tools helper
- Test: Returns list with both tools
- Implement: Function returning [search_web, save_note]
- Commits: test: then feat: implement get_all_tools function

Documentation: Update learning log after GROUP 2

GROUP 3: Agent Core Structure

Goal: Initialize Agent with client and tools

Test-Implement Pairs:

1. Agent initialization
- Test: Agent initializes with client, max_iterations, tools list
- Implement: Agent.init with attributes
- Commits: test: then feat: implement Agent class initialization
2. System prompt builder
- Test: Prompt contains ReAct instructions and tool descriptions
- Implement: _build_system_prompt() method
- Commits: test: then feat: implement ReAct system prompt builder

GROUP 4: ReAct Loop Components

Goal: Implement parsing and tool execution

Test-Implement Pairs:

1. Action parser
- Test: Extracts tool_name and input from "Action: tool: input" format
- Test: Returns (None, None) if no Action found
- Implement: _parse_action() method
- Commits: test: then feat: implement action parser
2. Tool executor
- Test: Calls correct tool by name
- Test: Returns error for unknown tool
- Implement: _execute_tool() method
- Commits: test: then feat: implement tool executor
3. Observation formatter
- Test: Formats as "Observation: {output}"
- Implement: _format_observation() method
- Commits: test: then feat: implement observation formatter

Documentation: Update learning log after GROUP 4

GROUP 5: Main Run Loop

Goal: Integrate components into working ReAct loop

Test-Implement Pairs:

1. Basic run method
- Test: Executes single iteration with mocked LLM response
- Implement: run() method with loop logic
- Commits: test: then feat: implement basic ReAct run loop
2. Max iterations enforcement
- Test: Stops after max_iterations even if not done
- Verify/Refactor: Ensure loop respects limit
- Commits: test: then refactor: ensure max iterations enforced
3. Final answer detection
- Test: Stops when LLM provides Answer instead of Action
- Verify: Current implementation handles this
- Commit: test: agent stops when final answer provided

Documentation: Update learning log after GROUP 5

GROUP 6: Integration

Goal: End-to-end testing and manual verification

Test-Implement Pairs:

1. End-to-end test
- Create: tests/agents/test_integration.py
- Test: Complete flow with mocked responses (Thought→Action→Observation→Answer)
- Commit: test: end-to-end agent workflow with mocked responses
2. Interactive main
- Implement: src/main.py with REPL loop
- Commit: feat: add interactive main entry point
3. Manual verification
- Run: uv run python src/main.py
- Test queries: "Search for Python", "Save a note"
- Document: Output in learning log (no commit)

Documentation: Update learning log after GROUP 6

GROUP 7: Documentation & Cleanup

Goal: Document patterns and finalize Phase 1

1. Add docstrings to all public functions
2. Complete docs/learning-logs/phase-1-log.md with:
- What we built (ReAct agent with placeholders)
- Key decisions (max_iterations=3, visible output)
- Code highlights (system prompt, action parsing)
- Sample output (complete interaction)
3. Update CLAUDE.md with Phase 1 patterns:
- ReAct prompt format
- Tool interface structure
- Testing patterns for LLM code
4. Update MASTER_LOG.md with Phase 1 summary
5. Run linting: uv run ruff check . && uv run ruff format .
6. Final coverage: uv run pytest --cov=src (expect >70%)

Commits:
- docs: add comprehensive docstrings
- docs: complete phase 1 learning log
- docs: add Phase 1 patterns to CLAUDE.md
- docs: add Phase 1 to MASTER_LOG
- chore: format code with ruff

Key Technical Decisions

1. Placeholder Tools: Mock implementations return static data. Real integration comes in Phase 2
(MCP servers).
2. Visible Reasoning: Output accumulates all Thought/Action/Observation text for transparency and
learning.
3. Max 3 Iterations: Conservative limit prevents API cost runaway during development.
4. Action Parsing: Simple string matching for "Action: tool_name: input" format. Reliable when LLM
follows prompt.
5. Conversation History: Managed within run() method as messages list. Each call is independent.
6. Testing Strategy: Mock OpenAI client responses for deterministic tests. Use side_effect for
multi-turn flows.

System Prompt Format

You are a helpful research assistant using the ReAct framework.

For each request:

Thought: [reasoning about what to do]
Action: [tool_name: input]
Observation: [tool output will be provided]

Continue until you can answer:

Answer: [final response]

Available tools:
- search_web: Search the web for information
- save_note: Save a note with title and content

Expected Output Example

Thought: I need to search for information about Python.
Action: search_web: Python programming language

Observation: MOCK SEARCH RESULTS for 'Python programming language':
1. Example result about Python programming language
2. Another result for Python programming language

Thought: I have the information I need.
Answer: Python is a popular programming language known for simplicity and versatility.

Workflow Tips

- Use /clear after each GROUP to reset context
- Run tests after every change: uv run pytest
- Commit atomically: One test, one implementation
- Document as you go: Update learning log after major groups
- Manual test in GROUP 6 to see ReAct loop in action

Success Criteria

✅ All tests pass (uv run pytest)
✅ Agent runs interactively via src/main.py
✅ Output shows visible Thought/Action/Observation
✅ Agent respects max 3 iterations
✅ Placeholder tools return mock data
✅ Code coverage >70%
✅ Learning logs document journey
