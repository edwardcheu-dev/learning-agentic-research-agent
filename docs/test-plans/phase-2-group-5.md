# Phase 2, GROUP 5: ReAct Step Visualization - Manual Verification

**Feature**: Separate visual sections for Thought, Action, and Observation steps with status indicators

**Implementation Date**: 2026-01-06
**Test Plan Version**: 1.0

---

## Prerequisites

**Environment Setup**:
1. Ensure dependencies installed: `uv sync`
2. Verify POE_API_KEY is set: `echo $POE_API_KEY`
3. No other instances of the app running
4. Completion of GROUP 4 (streaming tokens) verified

**Expected Environment**:
- Python 3.12+
- Terminal with color support and Unicode symbols (○ ● ✓)
- Working directory: `/Users/edwardcheu/AE/hands-on/research-assistant/`

---

## Verification Steps

### Step 1: Launch TUI and Submit Query

**Command**:
```bash
uv run python src/main.py
```

**Action**:
1. Wait for TUI to launch
2. Type query: "Search for Python tutorials"
3. Press Enter to submit

**Expected Outcome**:
- TUI launches successfully
- Query appears in conversation area
- Streaming tokens appear character-by-character
- After streaming completes, separate nodes appear for:
  - **ThoughtNode**: Agent's reasoning (e.g., "I should search for information")
  - **ActionNode**: Tool execution (e.g., "search_web(Python tutorials)")
  - **ObservationNode**: Tool result (e.g., "Observation: MOCK SEARCH RESULTS...")

**Visual Check**:
- [ ] ThoughtNode appears with "Thought:" label
- [ ] ActionNode appears with "Action:" label
- [ ] ObservationNode appears with "Observation:" label
- [ ] Each node is visually distinct from streaming text
- [ ] Nodes appear in order: Thought → Action → Observation

**If Failed**:
- Check if AsyncAgent.run_streaming() emits typed events
- Verify app.py event handler creates nodes
- Check terminal output for errors

---

### Step 2: Verify Status Indicators

**Focus**: Check that each node displays a status symbol

**Expected Status Symbols**:
- ○ (hollow circle) = pending
- ● (filled circle) = running
- ✓ (checkmark) = done

**Visual Check**:
- [ ] ThoughtNode shows a status symbol (should be ✓ done)
- [ ] ActionNode shows a status symbol (should be ✓ done)
- [ ] ObservationNode shows a status symbol (should be ✓ done)
- [ ] Symbols are visible and correctly rendered

**Note**: GROUP 5 shows all nodes as "done" status. Real-time status updates (pending→running→done) will be enhanced in GROUP 6.

**If Failed**:
- Check terminal supports Unicode symbols
- Verify STATUS_SYMBOLS dict in widgets.py
- Try different terminal emulator

---

### Step 3: Verify Status Colors

**Focus**: Check that status indicators have appropriate colors

**Expected Colors**:
- dim (gray) = pending
- yellow = running
- green = done

**Visual Check**:
- [ ] ThoughtNode status symbol is green (done)
- [ ] ActionNode status symbol is green (done)
- [ ] ObservationNode status symbol is green (done)
- [ ] Colors are visible and distinguishable

**If Failed**:
- Check terminal supports ANSI colors
- Verify STATUS_COLORS dict in widgets.py
- Test in different terminal with better color support

---

### Step 4: Verify Node Content

**Focus**: Check that each node displays the correct content

**Expected Content**:

**ThoughtNode**:
- Should display agent's reasoning text
- Example: "I should search for information"
- Should NOT include "Thought:" prefix (label is separate)

**ActionNode**:
- Should display tool name and input
- Format: `tool_name(input)`
- Example: "search_web(Python tutorials)"

**ObservationNode**:
- Should display full observation text
- Example: "Observation: MOCK SEARCH RESULTS for 'Python tutorials'"

**Visual Check**:
- [ ] ThoughtNode content is readable and complete
- [ ] ActionNode shows tool name and input correctly
- [ ] ObservationNode shows full result text
- [ ] No text truncation or formatting issues

**If Failed**:
- Check _parse_thought() extracts content correctly
- Verify metadata contains tool_name and tool_input
- Check observation formatting

---

### Step 5: Multiple ReAct Iterations

**Action**:
1. Submit complex query that triggers multiple tool calls
2. Example: "Find Python tutorials and save them to notes"

**Expected Outcome**:
- Multiple sets of Thought/Action/Observation nodes appear
- Each iteration is clearly separated
- Nodes appear in chronological order

**Visual Check**:
- [ ] First iteration: Thought → Action → Observation
- [ ] Second iteration: Thought → Action → Observation
- [ ] Clear visual separation between iterations
- [ ] All nodes display correctly

**If Failed**:
- Check iteration metadata in events
- Verify multiple events are yielded correctly
- Check conversation area scrolling

---

### Step 6: Streaming Text vs Nodes

**Focus**: Verify that streaming text and ReAct nodes coexist properly

**Action**:
Submit query: "What is machine learning?"

**Expected Behavior**:
1. StreamingText widget displays tokens as they arrive
2. After streaming completes, typed nodes appear
3. StreamingText remains visible (shows final answer)
4. Nodes appear below/alongside streaming text

**Visual Check**:
- [ ] Streaming text displays during LLM generation
- [ ] Nodes appear after streaming completes
- [ ] Both streaming text and nodes are visible
- [ ] Layout is clean (no overlap or collision)

**If Failed**:
- Check if both widgets are mounted to conversation
- Verify event processing order
- Check CSS/layout configuration

---

## Edge Cases

### Edge Case 1: Query with No Action

**Action**: Submit query: "Hello, how are you?"

**Expected**:
- StreamingText displays answer
- ThoughtNode may appear (if LLM outputs "Thought:")
- No ActionNode or ObservationNode (no tool call)
- Application doesn't crash

**Actual**: _____

---

### Edge Case 2: Very Long Node Content

**Action**: Submit query that generates long thought/action/observation

**Expected**:
- Long content wraps correctly in conversation area
- No truncation
- Scrollbar appears if needed
- Text remains readable

**Actual**: _____

---

### Edge Case 3: Unicode Symbol Fallback

**Action**: Test in terminal without Unicode support

**Expected**:
- Status symbols may appear as characters or boxes
- Application doesn't crash
- Content is still readable
- Functionality works despite display issues

**Actual**: _____

**Note**: If symbols don't render, consider ASCII fallback in future enhancement.

---

### Edge Case 4: Rapid Consecutive Queries

**Action**: Submit 3 queries quickly in succession

**Expected**:
- All queries process correctly
- Nodes appear for each query
- No race conditions or missing nodes
- Conversation area scrolls appropriately

**Actual**: _____

---

## Success Criteria

**Functional Requirements**:
- [ ] ThoughtNode displays with status indicator
- [ ] ActionNode displays with tool name and input
- [ ] ObservationNode displays with result text
- [ ] Status symbols are visible (○ ● ✓)
- [ ] Status colors work (dim/yellow/green)
- [ ] Nodes appear in correct order (Thought → Action → Observation)
- [ ] Multiple iterations display correctly

**Quality Requirements**:
- [ ] Visual separation between streaming text and nodes
- [ ] All text is readable and properly formatted
- [ ] No overlap or layout issues
- [ ] Conversation area scrolls smoothly
- [ ] No crashes or errors

**Visual Design**:
- [ ] Status indicators are intuitive
- [ ] Colors enhance readability
- [ ] Node labels are clear (Thought:/Action:/Observation:)
- [ ] Layout is clean and professional

---

## Troubleshooting

**Issue**: Status symbols don't render (show as boxes or ?)

**Solution**:
1. Check terminal supports Unicode: `echo "○ ● ✓"`
2. Try different terminal emulator (iTerm2, Terminal.app, etc.)
3. Verify font supports Unicode symbols
4. For now, symbols should still display (even if ugly)

---

**Issue**: Status colors don't appear

**Solution**:
1. Check terminal supports ANSI colors
2. Verify TERM environment variable: `echo $TERM`
3. Test colors: `tput setaf 2; echo "green"; tput sgr0`
4. Try enabling color in terminal preferences

---

**Issue**: Nodes don't appear, only streaming text

**Solution**:
1. Check AsyncAgent emits typed events: Add debug print in run_streaming()
2. Verify app.py event handler has elif branches for thought/action/observation
3. Check event.type values are correct
4. Run tests: `uv run pytest tests/agents/test_async_agent.py::test_async_agent_emits_thought_event -v`

---

**Issue**: Nodes appear in wrong order

**Solution**:
1. Verify event emission order in AsyncAgent.run_streaming()
2. Check metadata["iteration"] values
3. Verify conversation.mount() is called in order
4. Check ScrollableContainer scroll behavior

---

## Verification Checklist

Complete this checklist and report results:

- [ ] All verification steps passed
- [ ] All edge cases tested
- [ ] Success criteria met
- [ ] No unresolved issues

**Approval**: YES / NO / ISSUES FOUND

**Notes**: _____

---

## Example Expected Output

When you submit "Search for Python tutorials", you should see something like:

```
You: Search for Python tutorials

[Streaming text appears character-by-character...]
Thought: I should search...
Action: search_web: Python tutorials

✓ Thought: I should search for information about Python tutorials
✓ Action: search_web(Python tutorials)
✓ Observation: Observation: MOCK SEARCH RESULTS for 'Python tutorials'

[Final answer continues streaming...]
Answer: Based on the search results...
```

**Key Visual Elements**:
- ✓ symbols should be green
- "Thought:", "Action:", "Observation:" labels in bold
- Clear separation between each node
- Streaming text flows naturally
