# Sample Prompts for Each Phase

## Mode Switching

Before diving into prompts, understand when to switch modes:

| Workflow Stage              | Mode              | How to Activate   |
|-----------------------------|-------------------|-------------------|
| Exploring / Investigating   | Plan Mode         | Shift+Tab twice   |
| Implementing checklist items| Auto-Accept Edits | Shift+Tab once    |
| Sensitive or unfamiliar code| Normal Mode       | Default           |

Tip: After Plan Mode presents a plan, selecting "Yes, and auto-accept edits"
switches to Auto-Accept mode and begins execution immediately.

## Starting a Phase

Switch to Plan Mode first (Shift+Tab twice), then use the custom command:

    /project:start-phase 1

This lets Claude research and create the checklist without making changes until
you approve.

## After Checklist Approval

Once you approve the checklist, switch to Auto-Accept (Shift+Tab once), then:

    The checklist looks good. Before implementing, use a subagent to verify our
    project structure matches what we planned in CLAUDE.md. Then start with the
    first checklist item.

## Between Logical Groups

Prompt:

    /clear

    Continue with the next group in the Phase 1 checklist. Read the checklist
    file to see where we left off.

## Keeping TDD Strict

Write test first:

    Write only the test for [specific item]. Run it to confirm it fails, then
    commit with message "test: [description]". Do not write implementation yet.

Then implement:

    Now write the minimal implementation to make the test pass. Run the test to
    confirm it passes, then commit with message "feat: [description]".

## After a Group of Commits

Prompt:

    We just finished implementing [X]. Append a summary to
    docs/learning-logs/phase-1-log.md including:
    - What was built
    - Key decisions made
    - Relevant code snippets with explanations
    - Sample output if applicable

    Then commit with message "docs: update phase 1 learning log".

## Updating Documentation

Prompt:

    Review what we built in Phase 1. Summarize the key patterns we established
    and update CLAUDE.md with any code style or testing patterns we should
    follow going forward. Then commit the changes.

## End of Phase

Prompt:

    Phase 1 is complete. Update docs/learning-logs/MASTER_LOG.md with a
    pedagogical summary of Phase 1, aggregating from the phase-1-log.md.
    Write it so someone new can understand how the agentic loop works by
    reading this section.

## Investigating Before Coding

Switch to Plan Mode (Shift+Tab twice) for investigation prompts:

General investigation:

    Use a subagent to investigate how [concept/library] works. Report back
    with a summary before we start implementing.

Pattern discovery:

    Use a subagent to read all files in src/mcp_servers/ and summarize the
    patterns they follow. Then use those patterns for our implementation.

After receiving the investigation results, switch to Auto-Accept (Shift+Tab
once) to begin implementation.

## When Context Gets Long

Prompt:

    /clear

    We're working on Phase 1. Current progress is tracked in
    docs/checklists/phase-1.md. Continue with the next unchecked item.

## Debugging

Prompt:

    The test is failing with [error]. Think hard about what might be wrong,
    then fix it.

## Asking for Recommendations

Stay in Plan Mode for recommendations:

    Before we implement this, what patterns would you recommend? Consider
    our existing code style and the project goals in CLAUDE.md.

## Mode-Specific Prompt Patterns

### Plan Mode Prompts (Research and Analysis)

These prompts work best in Plan Mode where Claude focuses on understanding:

    Analyze the current codebase structure and identify how [feature] should
    integrate with existing patterns.

    Review the test coverage in [directory] and recommend what additional
    tests we need.

    Compare our current implementation approach against the patterns in
    CLAUDE.md. Are we following our own guidelines?

    What are the potential risks or edge cases for implementing [feature]?

### Auto-Accept Prompts (Execution)

These prompts work best in Auto-Accept Mode for efficient execution:

    Implement all items in group 2 of the Phase 1 checklist. Follow TDD for
    each item.

    Refactor [file] to match the patterns we use in [other file]. Run tests
    after each change.

    Fix all linting errors in src/ and commit with message "chore: fix linting".

### Normal Mode Prompts (Careful Changes)

Use Normal Mode when you want to review each change:

    Make the changes we discussed, but pause after each file so I can review.

    Update the configuration files. I want to approve each change individually.
