# Schema & Validation Enhancements

Improvements related to structured outputs, type safety, and schema validation.

## Current State (Phase 1)

- Action parsing uses string splitting (`split(":", 1)`)
- Returns `tuple[str, str] | None` without validation
- Assumes LLM follows format (relies on prompt conditioning)
- No runtime validation of tool inputs or outputs

## Enhancements

### Use Pydantic Models for Action Parsing [P1] [Idea]

**Problem**: String parsing is brittle - doesn't validate structure or handle malformed responses gracefully

**Proposed Solution**:
- Define Pydantic models for Thought, Action, Observation, Answer
- Parse LLM responses into structured objects
- Validate tool names against registry
- Type-check tool inputs before execution

**Benefits**:
- Runtime validation catches format violations early
- Type safety prevents bugs
- Better error messages for debugging
- Easier to extend with new action types

**Considerations**:
- Adds dependency complexity
- May need fallback for malformed responses
- Performance overhead (minimal for Phase 1 scale)

**References**:
- [Pydantic documentation](https://docs.pydantic.dev/)
- Example: `src/config.py` already uses Pydantic for cache validation

---

### Use Instructor for Structured Outputs [P1] [Idea]

**Problem**: Current implementation relies on prompt engineering for format adherence - no guarantee LLM follows schema

**Proposed Solution**:
- Use [Instructor](https://github.com/jxnl/instructor) library
- Define response schemas with Pydantic
- Automatically retry on validation failures
- Leverage OpenAI function calling for guaranteed structure

**Benefits**:
- Near-perfect format adherence (function calling mode)
- Automatic retries with validation errors
- Simpler prompts (less format instructions needed)
- Better handling of edge cases

**Considerations**:
- Requires OpenAI models with function calling (already using gpt-4.1-mini)
- May increase API costs (retries)
- Need to handle API rate limits

**References**:
- [Instructor library](https://github.com/jxnl/instructor)
- [OpenAI function calling docs](https://platform.openai.com/docs/guides/function-calling)

---

### Add to Enhancement List

(Template for new ideas - delete this section when adding real enhancements)
