Automatically propose enhancements based on the recent codebase-qa conversation.

## Purpose

**This command is part of the post-milestone workflow** and should be run AFTER `/codebase-qa`.

Extract improvement ideas from the Q&A discussion for:
- **Schema & Validation**: Pydantic, Instructor, structured outputs
- **Agent Robustness**: Prompt engineering, DSPy, error recovery
- **Observability**: MLflow tracing, logging, monitoring

**NO user input required** - Claude analyzes conversation history automatically.

## Workflow

### 1. ANALYZE CONVERSATION HISTORY

Review recent messages from the codebase-qa session to identify:
- Limitations mentioned (e.g., "string parsing is brittle")
- Improvement opportunities (e.g., "could use Pydantic for validation")
- Known gaps (e.g., "no observability into LLM calls")
- Trade-offs discussed (e.g., "simple now, but won't scale")
- Tools/libraries mentioned (e.g., "Instructor for structured outputs")

### 2. READ EXISTING ENHANCEMENTS

Check `docs/enhancements/[category].md` to:
- Avoid duplicates
- Ensure consistent formatting
- Understand related enhancements

### 3. AUTO-GENERATE ENHANCEMENTS

For each improvement identified from the conversation:
- Categorize (schema, robustness, observability)
- Assign priority based on discussion:
  - P0: If described as "critical" or "blocker"
  - P1: If described as "important" or "should have"
  - P2: If described as "nice-to-have" or "future"
- Extract problem statement from discussion
- Extract proposed solution (if mentioned)
- Note benefits and considerations from conversation

### 4. ADD ENHANCEMENTS

Append to the appropriate category file using this format:

```markdown
### [Enhancement Title] [Priority] [Idea]

**Problem**: [Description of limitation or opportunity]

**Proposed Solution**: [High-level approach]

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Considerations**:
- [Trade-off 1]
- [Risk or dependency]

**References**:
- [Link to docs, papers, or examples]
```

Status starts as **[Idea]** - user can update to Planned/In Progress/Done later.

### 5. COMMIT CHANGES

```bash
git add docs/enhancements/*.md
git commit -m "docs: add enhancement proposals from codebase-qa discussion"
```

### 6. CONFIRM

Display summary:
```
✅ Enhancements extracted from codebase-qa conversation

Added [N] enhancement(s):

1. [Category]: [Enhancement Title] [Priority]
2. [Category]: [Enhancement Title] [Priority]
...

Files updated:
- docs/enhancements/schema-validation.md
- docs/enhancements/agent-robustness.md
- docs/enhancements/observability.md

Changes committed: [commit hash]

Next steps:
- Review proposals in docs/enhancements/
- Update priority/status if needed
- Use `/promote-enhancements` to convert to MVP phase when ready
```

## Enhancement Entry Template

```markdown
### Enhancement Title [P1] [Idea]

**Problem**: Describe the limitation or opportunity

**Proposed Solution**: Brief description of approach

**Benefits**: Why this matters

**Considerations**: Trade-offs, risks, dependencies

**References**: Links to docs, papers, libraries
```

## Important

- **Run this AFTER `/codebase-qa`** - needs conversation history to analyze
- Automatically assign priority based on discussion urgency/importance
- Status always starts as [Idea]
- Check for duplicates before adding
- Automatically commit changes after adding enhancements
- If no enhancements identified from conversation, inform user (no changes made)
