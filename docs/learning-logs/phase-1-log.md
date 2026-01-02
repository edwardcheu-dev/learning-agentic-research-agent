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

## Phase Summary

(Written at the end of Phase 1 - high-level summary for MASTER_LOG.md)