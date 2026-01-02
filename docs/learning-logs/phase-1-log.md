# Phase 1 Learning Log: Basic Agentic Loop

## Session Log

---

### Session 1: 2026-01-02 - GROUP 1 & GROUP 2

#### What We Built

**GROUP 1: Testing Infrastructure**
- Verified pytest test discovery works correctly
- Created `tests/agents/test_tools.py` with baseline placeholder test

**GROUP 2: Tool System**
- Implemented `Tool` dataclass with name, description, and function attributes
- Created two placeholder tools:
  - `search_web`: Returns mock search results
  - `save_note`: Returns mock save confirmation
- Implemented `get_all_tools()` helper to aggregate available tools

#### Key Decisions

1. **Tool Interface**: Used a simple dataclass with function callback rather than a complex class hierarchy
   - **Rationale**: Keeps Phase 1 focused on the agentic loop, not tool architecture
   - **Trade-off**: Will need refactoring in Phase 2 for MCP integration

2. **Placeholder Returns**: Tools return formatted strings with "MOCK" prefixes
   - **Rationale**: Makes it obvious during testing that we're using placeholders
   - **Example**: `"MOCK SEARCH RESULTS for 'python':\n1. Example result..."`

3. **Max Iterations = 3**: Conservative limit chosen by user
   - **Rationale**: Prevents API cost runaway during development
   - **Impact**: Agent must be efficient in its reasoning

#### Code Highlights

**Tool Dataclass (src/agents/tools.py:7-13)**
```python
@dataclass
class Tool:
    """Represents a tool the agent can use."""
    name: str
    description: str
    function: Callable[[str], str]
```

**Search Web Placeholder (src/agents/tools.py:16-22)**
```python
def _search_web_impl(query: str) -> str:
    """Placeholder implementation of web search."""
    return (
        f"MOCK SEARCH RESULTS for '{query}':\n"
        f"1. Example result about {query}\n"
        f"2. Another result for {query}"
    )
```

**Save Note Placeholder (src/agents/tools.py:34-38)**
```python
def _save_note_impl(content: str) -> str:
    """Placeholder implementation of save note."""
    lines = content.split("\n", 1)
    title = lines[0].replace("title:", "").strip() if lines else "untitled"
    return f"MOCK SAVE: Note '{title}' saved successfully"
```

#### Testing Pattern

Following strict TDD workflow:
1. Write test first (test: commit)
2. Run test to confirm failure
3. Write minimal implementation (feat: commit)
4. Run test to confirm pass
5. Repeat

**Example Test (tests/agents/test_tools.py:21-29)**
```python
def test_search_web_tool_returns_mock_results():
    """search_web tool returns placeholder search results."""
    tool = get_search_web_tool()
    result = tool.function("python tutorials")

    assert "MOCK SEARCH RESULTS" in result
    assert "python tutorials" in result
    assert tool.name == "search_web"
    assert "search" in tool.description.lower()
```

#### Lessons Learned

1. **Mocking Strategy**: Using simple string returns makes testing deterministic without requiring complex mocking frameworks

2. **Commit Granularity**: Atomic commits (test → implementation) create clear history and make debugging easier

3. **Line Length**: Had to refactor long f-strings to satisfy ruff's 88-character limit:
   ```python
   # Before (112 chars - too long)
   return f"MOCK SEARCH RESULTS for '{query}':\n1. Example result about {query}\n2. Another result for {query}"

   # After (split across lines)
   return (
       f"MOCK SEARCH RESULTS for '{query}':\n"
       f"1. Example result about {query}\n"
       f"2. Another result for {query}"
   )
   ```

4. **Import Organization**: Used absolute imports (`from src.agents.tools import Tool`) to ensure tests can find modules

#### Git History

```
fb2309b test: verify pytest test discovery works
8150b14 test: tool must have name, description, and function
4fcf429 feat: implement basic Tool class structure
3438f4f test: search_web tool returns mock search results
8c5f265 feat: implement placeholder search_web tool
9d9165a test: save_note tool returns confirmation message
b283ac8 feat: implement placeholder save_note tool
29a96af test: get_all_tools returns complete tool list
51cc09f feat: implement get_all_tools function
```

Each commit follows the prefix convention:
- `test:` - Adding/updating tests before implementation
- `feat:` - New feature implementation that makes tests pass

---

### Session 2: 2026-01-02 - GROUP 3

#### What We Built

**GROUP 3: Agent Core Structure**
- Created the `Agent` class in `src/agents/agent.py`
- Implemented `__init__` with client, max_iterations, and tools initialization
- Implemented `_build_system_prompt()` to generate ReAct-style system prompts

#### Key Decisions

1. **Agent Initialization**: Agent automatically loads all available tools via `get_all_tools()`
   - **Rationale**: Simplifies initialization and ensures all tools are available
   - **Trade-off**: Can't selectively enable/disable tools (not needed in Phase 1)

2. **System Prompt Format**: Used clear, explicit ReAct format with labeled sections
   - **Rationale**: Makes it easier for LLM to follow the pattern
   - **Structure**: Thought → Action → Observation → Answer
   - **Tool Listing**: Dynamically includes tool names and descriptions

3. **Private Method Naming**: Used `_build_system_prompt()` with underscore prefix
   - **Rationale**: Internal helper method, not part of public API
   - **Pattern**: Will continue for other internal methods like `_parse_action()`, `_execute_tool()`

#### Code Highlights

**Agent Initialization (src/agents/agent.py:9-18)**
```python
def __init__(self, client, max_iterations: int):
    """Initialize the agent.

    Args:
        client: OpenAI client for LLM calls
        max_iterations: Maximum number of reasoning iterations
    """
    self.client = client
    self.max_iterations = max_iterations
    self.tools = get_all_tools()
```

**System Prompt Builder (src/agents/agent.py:20-44)**
```python
def _build_system_prompt(self) -> str:
    """Build the system prompt with ReAct instructions and tool descriptions."""
    tool_descriptions = "\n".join(
        f"- {tool.name}: {tool.description}" for tool in self.tools
    )

    return f"""You are a ReAct (Reasoning and Acting) agent.

Answer the user's question by following this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name: input]
Observation: [Result from the tool]
... (repeat Thought/Action/Observation as needed)
Answer: [Final answer to the user's question]

Available tools:
{tool_descriptions}

Always start with a Thought, then take an Action, wait for the Observation, and repeat until you can provide a final Answer.
"""
```

**Sample System Prompt Output**:
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

Always start with a Thought, then take an Action, wait for the Observation, and repeat until you can provide a final Answer.
```

#### Testing Pattern

**Test for Initialization (tests/agents/test_agent.py:8-15)**
```python
def test_agent_initializes_with_client():
    """Agent should initialize with OpenAI client and tools."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    assert agent.client == mock_client
    assert agent.max_iterations == 3
    assert len(agent.tools) == 2  # search_web and save_note
```

**Test for System Prompt (tests/agents/test_agent.py:18-36)**
```python
def test_agent_builds_system_prompt_with_react_instructions():
    """Agent should build system prompt with ReAct format and tool descriptions."""
    mock_client = Mock()
    agent = Agent(client=mock_client, max_iterations=3)

    prompt = agent._build_system_prompt()

    assert isinstance(prompt, str)
    # Check for ReAct-style keywords
    assert "Thought:" in prompt
    assert "Action:" in prompt
    assert "Observation:" in prompt
    assert "Answer:" in prompt
    # Check for tool descriptions
    assert "search_web" in prompt
    assert "save_note" in prompt
```

#### Lessons Learned

1. **TDD Workflow Enforcement**: The user caught me implementing before committing the test - following strict TDD discipline is crucial for maintaining project standards

2. **Dynamic Tool Listing**: Using a loop to build tool descriptions ensures the prompt automatically updates when new tools are added

3. **Mock Usage**: Using `unittest.mock.Mock()` for the OpenAI client makes tests fast and deterministic without requiring API keys

4. **Format String Clarity**: Multi-line f-strings with triple quotes make prompt templates more readable

#### Git History

```
d75f3f1 test: Agent initializes with client, max_iterations, and tools list
b895715 feat: implement Agent.__init__ with client, max_iterations, and tools
d38bd0d test: Agent builds system prompt with ReAct instructions and tool descriptions
dcb3302 feat: implement _build_system_prompt() with ReAct format
```

---

## Phase Summary

(Written at the end of Phase 1 - high-level summary for MASTER_LOG.md)