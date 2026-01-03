# Agent Robustness Enhancements

Improvements related to prompt engineering, agent reliability, and error recovery.

## Current State (Phase 1)

- Fixed system prompt with ReAct format
- No few-shot examples
- Max 3 iterations (conservative limit)
- Unknown tool errors raise ValueError (no recovery)
- No prompt optimization or testing

## Enhancements

### Add Few-Shot Examples to System Prompt [P1] [Idea]

**Problem**: LLM may not immediately understand ReAct format without examples

**Proposed Solution**:
- Add 1-2 example interactions to system prompt
- Show complete Thought → Action → Observation → Answer cycles
- Demonstrate edge cases (multi-step reasoning, tool selection)

**Benefits**:
- Faster convergence to correct format
- Fewer malformed responses
- Better tool selection (LLM sees examples of when to use which tool)

**Considerations**:
- Increases prompt tokens (cost per call)
- Need to choose representative examples
- Examples may bias agent toward specific patterns

**References**:
- ReAct paper: https://arxiv.org/abs/2210.03629 (Section 3.2 on prompting)

---

### Implement Automatic Prompt Optimization with DSPy [P2] [Idea]

**Problem**: Current prompt is hand-crafted - no systematic testing or optimization

**Proposed Solution**:
- Use [DSPy](https://github.com/stanfordnlp/dspy) to optimize prompts
- Define success metrics (correct tool selection, format adherence, answer quality)
- Generate training examples from manual tests
- Automatically find better prompt templates

**Benefits**:
- Data-driven prompt improvement
- Systematic testing against regression
- Discover better phrasings than manual iteration
- Adaptable to new models or tools

**Considerations**:
- Requires labeled training data
- May overfit to specific examples
- Adds complexity to prompt management
- Learning curve for DSPy

**References**:
- [DSPy documentation](https://dspy-docs.vercel.app/)
- [DSPy paper](https://arxiv.org/abs/2310.03714)

---

### Graceful Error Recovery [P1] [Idea]

**Problem**: Unknown tool errors crash the agent - no opportunity for self-correction

**Proposed Solution**:
- Catch `ValueError` from `_execute_tool()`
- Feed error message back to LLM as observation
- Allow agent to try different tool or ask for clarification

**Benefits**:
- More resilient to typos or hallucinated tool names
- LLM can learn from errors (sees "Unknown tool: search_weg")
- Better user experience (doesn't crash on errors)

**Considerations**:
- May waste iterations on unrecoverable errors
- Need max retry limit to prevent loops
- Error messages must be informative to LLM

**Example**:
```python
try:
    tool_result = self._execute_tool(tool_name, tool_input)
except ValueError as e:
    tool_result = f"ERROR: {str(e)}. Please try a different tool."
```

---

### Add to Enhancement List

(Template for new ideas)
