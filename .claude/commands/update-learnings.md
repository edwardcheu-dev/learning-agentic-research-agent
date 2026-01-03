Automatically capture architectural insights from the recent codebase-qa conversation.

## Purpose

**This command is part of the post-milestone workflow** and should be run AFTER `/codebase-qa`.

Update learning documentation based on the Q&A discussion when:
- Important architectural insights were discovered (e.g., "how ReAct loop actually works")
- Design decisions were explained with rationale
- Patterns worth documenting were identified
- Gaps in existing documentation were revealed

**NO user input required** - Claude analyzes conversation history automatically.

## Workflow

### 1. ANALYZE CONVERSATION HISTORY

Review recent messages from the codebase-qa session to identify:
- Key architectural insights explained
- "Aha moments" where user gained understanding
- Design rationale that should be documented
- Code patterns that need explanation
- Concepts that bridge implementation and theory

Automatically determine target location:
- **MASTER_LOG.md**: For general architectural insights (pedagogical)
- **phase-N-log.md**: For implementation-specific details (narrative)
- **Both**: If insight is both conceptual and implementation-specific

### 2. READ EXISTING DOCUMENTATION

Load current documentation to understand:
- Structure and organization
- Where new content should fit
- What's already documented (avoid duplication)

For MASTER_LOG.md:
- Check "Key Concepts" section for conceptual additions
- Check "Code Walkthrough" for implementation examples

For phase-N-log.md:
- Find appropriate session or create new "Post-Implementation Insights" section
- Maintain session-based narrative structure

### 3. DRAFT CONTENT

Create content with:
- **Clear heading**: Subsection title that describes the insight
- **Context**: Why this matters / what problem it addresses
- **Explanation**: Detailed walkthrough with examples
- **Code references**: File paths and line numbers
- **Implications**: How this affects understanding or future work

### 4. UPDATE DOCUMENTATION

Add content to appropriate location:
- **MASTER_LOG.md**: Under relevant section (usually "Key Concepts" or new subsection)
- **phase-N-log.md**: As new session entry or post-implementation section

### 5. COMMIT CHANGES

```bash
git add docs/learning-logs/*.md
git commit -m "docs: capture insights from codebase-qa discussion"
```

### 6. CONFIRM

Display summary:
```
✅ Insights captured from codebase-qa conversation

Documentation updated:
- MASTER_LOG.md: [New section added or "No additions needed"]
- phase-N-log.md: [New section added or "No additions needed"]

Insights documented:
1. [Brief description of insight 1]
2. [Brief description of insight 2]

Changes committed: [commit hash]

Next steps:
- Review additions in learning logs
- Run `/propose-enhancements` to extract improvement ideas
```

## Content Guidelines

**For MASTER_LOG.md**:
- Focus on "why" and "how it works"
- Use pedagogical tone (teaching others)
- Include diagrams or examples
- Reference code with file:line notation

**For phase-N-log.md**:
- Maintain chronological narrative
- Include decision rationale
- Document trade-offs and alternatives considered
- Capture lessons learned

## Important

- **Run this AFTER `/codebase-qa`** - needs conversation history to analyze
- Always read existing docs before adding content to avoid duplication
- Maintain consistent structure and formatting
- Include concrete examples with code references from the Q&A
- Automatically commit changes with descriptive message
- If nothing significant to document, inform user (no changes made)
