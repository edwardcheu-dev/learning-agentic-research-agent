# Phase 2, GROUP 2: Basic TUI Shell - Manual Verification

**Feature**: Minimal Textual app with header, input, conversation area, synchronous agent integration

**Implementation Date**: 2026-01-03
**Test Plan Version**: 1.0

---

## Prerequisites

**Environment Setup**:
1. Ensure dependencies installed: `uv sync`
2. Verify POE_API_KEY is set: `echo $POE_API_KEY`
3. No other instances of the app running

**Expected Environment**:
- Python 3.12+
- Terminal with color support
- Working directory: `/Users/edwardcheu/AE/hands-on/research-assistant/`

---

## Verification Steps

### Step 1: Launch TUI

**Command**:
```bash
uv run python src/main.py --tui
```

**Expected Outcome**:
- Application launches without errors
- TUI interface appears with:
  - Header at top
  - Conversation area (scrollable, initially empty)
  - Input field at bottom with placeholder text
  - Footer with keyboard shortcuts

**Visual Check**:
- [ ] Header displays "Research Assistant" or similar title
- [ ] Conversation area is visible and empty
- [ ] Input field shows placeholder: "Type your question..."
- [ ] Footer shows: F1:Help, F2:Logs, q:Quit (or similar)

**If Failed**:
- Check error message
- Verify textual dependency installed: `uv pip list | grep textual`
- Check logs: Look for import errors

---

### Step 2: Submit Query (Synchronous Agent)

**Action**:
1. Type in input field: "What is the capital of France?"
2. Press Enter to submit

**Expected Outcome**:
- Query appears in conversation area
- Agent response appears below query
- Response should mention "Paris"
- Input field clears after submission

**Visual Check**:
- [ ] Query text displays in conversation area
- [ ] Agent response appears (may take 2-5 seconds)
- [ ] Response is readable and formatted
- [ ] Input field is cleared and ready for next query

**If Failed**:
- Check if POE_API_KEY is valid
- Look for network errors in terminal
- Verify agent.run() is called (check logs if F2 works)

---

### Step 3: Multiple Queries

**Action**:
1. Submit query: "What is 2 + 2?"
2. Submit query: "What color is the sky?"

**Expected Outcome**:
- Both queries and responses appear in conversation area
- Conversation area scrolls to show latest response
- Previous queries/responses remain visible above

**Visual Check**:
- [ ] Both Q&A pairs visible
- [ ] Conversation area scrolls automatically
- [ ] All text is readable (no truncation)

**If Failed**:
- Check if ScrollableContainer is configured correctly
- Verify conversation history is maintained

---

### Step 4: Keyboard Shortcuts

**Action**:
1. Press F1 (Help)
2. Press F2 (Logs) - if implemented
3. Press Ctrl+C or 'q' to quit

**Expected Outcome**:
- F1: Help modal or message appears
- F2: Log panel toggles (if implemented in this GROUP)
- Ctrl+C or 'q': Application exits cleanly

**Visual Check**:
- [ ] F1 shows help information
- [ ] F2 toggles logs (or shows "not implemented" message)
- [ ] 'q' exits without errors

**If Failed**:
- Check bindings in ResearchAssistantApp class
- Look for key handler errors in logs

---

### Step 5: Fallback REPL Mode

**Command**:
```bash
uv run python src/main.py --repl
```

**Expected Outcome**:
- Application launches in REPL mode (not TUI)
- Command-line prompt appears
- Can submit queries and get responses

**Visual Check**:
- [ ] REPL prompt displays
- [ ] Can submit query and get response
- [ ] No TUI interface appears

**If Failed**:
- Check main.py flag routing logic
- Verify --repl flag is recognized

---

## Edge Cases

### Edge Case 1: Empty Input Submission

**Action**: Press Enter with empty input field

**Expected**:
- No query submitted
- No error message
- Input field remains focused

**Actual**: _____

---

### Edge Case 2: Very Long Query

**Action**: Submit query with 500+ characters

**Expected**:
- Query wraps in conversation area
- Agent processes normally
- No truncation or errors

**Actual**: _____

---

### Edge Case 3: API Error Handling

**Action**:
1. Temporarily unset POE_API_KEY: `unset POE_API_KEY`
2. Launch TUI
3. Submit query

**Expected**:
- Error message appears in conversation area
- Application doesn't crash
- User can still quit cleanly

**Actual**: _____

**Restore**: `export POE_API_KEY=your_key` after testing

---

## Success Criteria

**Functional Requirements**:
- [ ] TUI launches with --tui flag
- [ ] REPL launches with --repl flag
- [ ] User can submit queries via input field
- [ ] Agent responses appear in conversation area
- [ ] Conversation history is maintained
- [ ] Keyboard shortcuts work (F1, q)

**Quality Requirements**:
- [ ] No crashes during normal usage
- [ ] Visual layout is clean and readable
- [ ] Error messages are user-friendly
- [ ] Application exits cleanly

**Performance**:
- [ ] TUI launches in <2 seconds
- [ ] Agent responds in <10 seconds (network dependent)
- [ ] UI remains responsive during agent processing

---

## Troubleshooting

**Issue**: TUI doesn't launch, ImportError for textual

**Solution**: Run `uv sync` to install dependencies

---

**Issue**: Agent doesn't respond, hangs indefinitely

**Solution**:
1. Check POE_API_KEY is set
2. Test API manually: `uv run python -c "import os; print(os.getenv('POE_API_KEY'))"`
3. Check network connectivity

---

**Issue**: TUI layout looks broken

**Solution**:
1. Verify terminal supports ANSI colors
2. Resize terminal window
3. Try different terminal emulator

---

## Verification Checklist

Complete this checklist and report results:

- [ ] All verification steps passed
- [ ] All edge cases tested
- [ ] Success criteria met
- [ ] No unresolved issues

**Approval**: YES / NO / ISSUES FOUND

**Notes**: _____
