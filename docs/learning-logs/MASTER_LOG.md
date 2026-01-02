# Research Assistant: Learning Journey

This document provides a pedagogical walkthrough of how this multi-agent AI system was built. Read this to understand how the entire repository works, from first principles to the complete implementation.

## Table of Contents

1. [Introduction](#introduction)
2. [Phase 1: Basic Agentic Loop](#phase-1-basic-agentic-loop)
3. [Phase 2: MCP Integration](#phase-2-mcp-integration)
4. [Phase 3: RAG System](#phase-3-rag-system)
5. [Phase 4: A2A Multi-Agent](#phase-4-a2a-multi-agent)
6. [Key Takeaways](#key-takeaways)

---

## Introduction

This project demonstrates four core concepts in modern AI agent development:

1. **Agentic Loops**: How agents think, act, and observe in cycles
2. **RAG (Retrieval-Augmented Generation)**: How to ground LLM responses in your own data
3. **MCP (Model Context Protocol)**: How to give agents access to tools
4. **A2A (Agent-to-Agent)**: How multiple agents coordinate to solve complex tasks

Each phase builds on the previous one. By the end, you'll have a working multi-agent system that can research topics, save notes, and answer questions from your personal knowledge base.

---

## Phase 1: Basic Agentic Loop

**Goal**: Build a single ReAct (Reasoning and Acting) agent that can think, use tools, and provide answers in a loop.

### What We Built

Phase 1 implemented a complete agentic loop using the ReAct framework:

1. **Tool System** (`src/agents/tools.py`):
   - Simple `Tool` dataclass with name, description, and function callback
   - Placeholder tools: `search_web` and `save_note` returning mock data
   - Factory functions for tool instantiation

2. **ReAct Agent** (`src/agents/agent.py`):
   - System prompt builder with dynamic tool descriptions
   - Action parser to extract tool calls from LLM responses
   - Tool executor with error handling
   - Main run loop: Thought → Action → Observation → Answer

3. **Interactive REPL** (`src/main.py`):
   - Command-line interface for manual testing
   - Transparent output showing all reasoning steps

4. **Configuration** (`src/config.py`):
   - Centralized settings for model, API, and defaults

### Key Concepts

**The ReAct Pattern**:

ReAct (Reasoning and Acting) is a prompting pattern that makes LLM reasoning explicit:

1. **Thought**: LLM explains its reasoning ("I need to search for X")
2. **Action**: LLM calls a tool ("search_web: Python programming")
3. **Observation**: Tool returns result (mock search results)
4. **Repeat**: Loop continues until LLM provides final Answer

This pattern makes the agent's decision-making transparent and debuggable.

**System Prompt Structure**:

```
You are a ReAct (Reasoning and Acting) agent.

Answer the user's question by following this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name: input]
Observation: [Result from the tool]
... (repeat Thought/Action/Observation as needed)
Answer: [Final answer to the user's question]

Available tools:
- search_web: Search the web for information
- save_note: Save a note to the knowledge base

Always start with a Thought, then take an Action, wait for the Observation,
and repeat until you can provide a final Answer.
```

The prompt is built dynamically to include all available tools.

**Action Parsing**:

The agent parses LLM responses to extract tool calls:

```
Input: "Thought: I need to search\nAction: search_web: Python tutorials"
Output: ("search_web", "Python tutorials")
```

Key implementation detail: Use `split(":", 1)` to split only on the FIRST colon, allowing colons in tool inputs.

**Loop Termination**:

Two ways to exit the ReAct loop:
1. **Max iterations reached**: Safety limit prevents infinite loops (default: 3)
2. **Final answer provided**: When `_parse_action()` returns `None` (no "Action:" found in response)

### Code Walkthrough

**Agent Initialization**:

```python
class Agent:
    def __init__(self, client: Any, max_iterations: int) -> None:
        self.client = client  # OpenAI client
        self.max_iterations = max_iterations
        self.tools = get_all_tools()  # Load all available tools
```

**Action Parser Implementation**:

```python
def _parse_action(self, response: str) -> tuple[str, str] | None:
    """Parse action from LLM response.

    Returns (tool_name, tool_input) or None if no action found.
    """
    if "Action:" not in response:
        return None

    for line in response.split("\n"):
        if line.strip().startswith("Action:"):
            action_text = line.strip()[7:].strip()  # Remove "Action: "

            if ":" in action_text:
                # Split on FIRST colon only (allows colons in input)
                tool_name, tool_input = action_text.split(":", 1)
                return (tool_name.strip(), tool_input.strip())

    return None
```

Why this works:
- Returns `None` when no "Action:" found → signals final answer
- Splits on first `:` only → allows tool inputs like "title: My Note"
- Handles multi-line responses by checking each line

**Main Run Loop**:

```python
def run(self, query: str) -> str:
    """Run the agent on a query using ReAct loop."""
    system_prompt = self._build_system_prompt()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    conversation = f"User: {query}\n\n"

    # ReAct loop
    for iteration in range(self.max_iterations):
        # Call LLM
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=DEFAULT_MAX_TOKENS  # CRITICAL for POE API
        )

        llm_response = response.choices[0].message.content
        conversation += f"{llm_response}\n\n"

        # Parse action
        action = self._parse_action(llm_response)

        # If no action, agent has provided final answer
        if action is None:
            break

        # Execute tool
        tool_name, tool_input = action
        tool_result = self._execute_tool(tool_name, tool_input)

        # Format observation
        observation = self._format_observation(tool_result)
        conversation += f"{observation}\n\n"

        # Add to conversation for next iteration
        messages.append({"role": "assistant", "content": llm_response})
        messages.append({"role": "user", "content": observation})

    return conversation.strip()
```

Flow:
1. Build system prompt with ReAct instructions
2. Initialize message history (system + user query)
3. Loop up to `max_iterations`:
   - Call LLM with current messages
   - Parse response for action
   - If no action → break (final answer provided)
   - Execute tool and format observation
   - Append assistant response and observation to messages
4. Return full conversation history

**Conversation Management**:

The agent maintains two representations:
- **messages**: List of OpenAI-style messages for LLM context
- **conversation**: Accumulated string for output to user

Pattern:
```
messages = [
    {"role": "system", "content": "You are a ReAct agent..."},
    {"role": "user", "content": "Search for Python"},
    {"role": "assistant", "content": "Thought: ...\nAction: search_web: Python"},
    {"role": "user", "content": "Observation: MOCK SEARCH RESULTS..."},
    {"role": "assistant", "content": "Answer: Python is..."}
]
```

Each turn adds TWO messages: assistant response + user observation.

### Example Interaction

```
User: Search for Python programming

Thought: I need to search for information about Python programming.
Action: search_web: Python programming

Observation: MOCK SEARCH RESULTS for 'Python programming':
1. Example result about Python programming
2. Another result for Python programming

Thought: I have the search results. I can now provide an answer.
Answer: Python is a popular high-level programming language known for
its readability and versatility.
```

### Patterns Established

**Tool Interface**:
- Tools are dataclasses with `name`, `description`, and `function`
- Tools are stateless: take string input, return string output
- Factory functions (`get_search_web_tool()`) for instantiation

**Testing Strategy**:
- Mock OpenAI client using `unittest.mock.MagicMock`
- Use `side_effect` for multi-turn conversations
- Verify behavior with count assertions, not exact strings
- Test both success and error paths

**Configuration**:
- ALL settings in `src/config.py`
- Never hardcode model names or API URLs
- Validate environment variables early with helpful error messages

### What's Next

Phase 2 will replace placeholder tools with real MCP servers:
- Filesystem server for reading/writing markdown notes
- Web search server using Brave Search API
- SQLite server for conversation memory

The ReAct loop stays the same, but tools will perform real actions instead of returning mock data.

---

## Phase 2: MCP Integration

*Summary will be aggregated from docs/learning-logs/phase-2-log.md*

(To be filled after Phase 2 completion)

---

## Phase 3: RAG System

*Summary will be aggregated from docs/learning-logs/phase-3-log.md*

(To be filled after Phase 3 completion)

---

## Phase 4: A2A Multi-Agent

*Summary will be aggregated from docs/learning-logs/phase-4-log.md*

(To be filled after Phase 4 completion)

---

## Key Takeaways

(To be filled after all phases complete)
