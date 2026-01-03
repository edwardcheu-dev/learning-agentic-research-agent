# Phase 2, GROUP 4: Streaming LLM Tokens - Manual Verification

**Feature**: Character-by-character streaming of LLM responses in TUI

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

### Step 1: Launch TUI and Verify Streaming

**Command**:
```bash
uv run python src/main.py --tui
```

**Action**:
1. Type in input field: "Explain photosynthesis in 3 sentences"
2. Press Enter to submit
3. **Watch closely** for token-by-token streaming

**Expected Outcome**:
- Tokens appear incrementally (character-by-character or word-by-word)
- NOT all at once after waiting
- Smooth, continuous appearance of text

**Visual Check**:
- [ ] First token appears within 1-2 seconds
- [ ] Subsequent tokens stream continuously
- [ ] Text builds up smoothly without sudden jumps
- [ ] No full response appearing all at once

**If Failed**:
- Check if run_streaming() is being used instead of run()
- Verify OpenAI client has stream=True parameter
- Check for network issues delaying all tokens

---

### Step 2: Measure First Token Latency

**Action**:
1. Note the time when you press Enter
2. Submit query: "What is 2 + 2?"
3. Note when first character appears

**Expected Outcome**:
- First token appears in <2 seconds
- Much faster than full response completion time

**Time Check**:
- [ ] First token: ___ seconds (should be <2s)
- [ ] Full response: ___ seconds (may be 3-10s)
- [ ] Latency is acceptable for good UX

**If Failed**:
- Check network latency
- Verify POE API is responding quickly
- Consider if streaming is actually working

---

### Step 3: Test Multiple Queries for Consistency

**Action**:
1. Submit query: "List 5 colors"
2. Verify streaming works
3. Submit query: "Count from 1 to 10"
4. Verify streaming works again

**Expected Outcome**:
- Both queries stream tokens incrementally
- Consistent behavior across queries
- No regression to non-streaming

**Visual Check**:
- [ ] First query streams correctly
- [ ] Second query streams correctly
- [ ] Behavior is consistent
- [ ] No sudden changes in streaming behavior

**If Failed**:
- Check if streaming state is maintained across queries
- Look for any state reset issues

---

### Step 4: Verify No Visual Glitches

**Action**:
1. Submit a longer query: "Write a 5-line poem about programming"
2. Watch for visual artifacts during streaming

**Expected Outcome**:
- Text appears cleanly without corruption
- No flickering or jumping
- No duplicate characters
- Proper line wrapping

**Visual Check**:
- [ ] No flickering during streaming
- [ ] No duplicate or missing characters
- [ ] Text wraps properly at terminal width
- [ ] Formatting is preserved

**If Failed**:
- Check StreamingText widget update() implementation
- Verify Textual rendering is working correctly
- Look for race conditions in async code

---

## Edge Cases

### Edge Case 1: Very Long Response

**Action**: Submit query: "Explain the history of computers in detail"

**Expected**:
- Streaming continues smoothly even for long responses
- Terminal scrolls automatically
- No memory issues or slowdowns

**Actual**: _____

---

### Edge Case 2: Network Latency Simulation

**Action**:
1. Submit query during poor network conditions (if possible)
2. Observe streaming behavior

**Expected**:
- Tokens may arrive in bursts but still stream
- No complete freeze or timeout
- Graceful handling of delays

**Actual**: _____

---

### Edge Case 3: API Error During Streaming

**Action**:
1. Submit a complex query
2. If API returns an error mid-stream, observe behavior

**Expected**:
- Error message appears clearly
- App doesn't crash
- User can still submit new queries

**Actual**: _____

---

## Success Criteria

**Functional Requirements**:
- [ ] Tokens appear incrementally, not all at once
- [ ] First token appears quickly (<2 seconds)
- [ ] Streaming works consistently across multiple queries
- [ ] Long responses stream smoothly

**Visual Requirements**:
- [ ] No flickering or visual glitches
- [ ] No duplicate or corrupted text
- [ ] Proper line wrapping and formatting
- [ ] Smooth, continuous text appearance

**Performance**:
- [ ] First token latency <2 seconds
- [ ] Streaming feels responsive and smooth
- [ ] No lag or freezing during streaming
- [ ] UI remains responsive

---

## Troubleshooting

**Issue**: Tokens appear all at once, not streaming

**Solution**:
1. Verify `stream=True` in client.chat.completions.create()
2. Check if run_streaming() is being called instead of run()
3. Verify AsyncOpenAI client is used, not synchronous OpenAI

---

**Issue**: Slow first token (>3 seconds)

**Solution**:
1. Check network connectivity
2. Verify POE API is responsive
3. Consider switching models if needed

---

**Issue**: Flickering or visual glitches

**Solution**:
1. Check StreamingText widget implementation
2. Verify update() is called correctly
3. Ensure no conflicting Textual updates

---

## Verification Checklist

Complete this checklist and report results:

- [ ] All verification steps passed
- [ ] All edge cases tested
- [ ] Success criteria met
- [ ] Streaming works as expected
- [ ] No visual glitches
- [ ] No unresolved issues

**Approval**: YES / NO / ISSUES FOUND

**Notes**: _____
