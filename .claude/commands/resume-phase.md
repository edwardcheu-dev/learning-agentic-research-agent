Resuming Phase $ARGUMENTS of the Research Assistant project.

## Your Task: Resume Implementation

You are resuming work after a context clear. Jump straight into IMPLEMENT mode - EXPLORE and PLAN are already complete.

### Step 1: Load Context

Read the following files to understand current state:
1. docs/checklists/phase-$ARGUMENTS.md - See progress and find next unchecked item
2. docs/implementation_plans/phase-$ARGUMENTS.md - Reference architecture and GROUP goals
3. Recent commits: Run `git log --oneline -5` to see what was just completed

### Step 2: Display Progress Summary

Present a clear summary in this format:

```
# Phase $ARGUMENTS Progress

## Checklist Overview
[Display each GROUP with completion status using ✅ for complete groups]

## Current Focus
GROUP X: [GROUP name]
- Progress: X/Y items complete
- Next Item: [ ] [Description of next unchecked item]

## Recent Commits
[Show last 5 commits from git log]

## Ready to Continue
I'll now work on: [next unchecked item description]
```

### Step 3: Continue Implementation

Follow the TDD workflow from .claude/commands/start-phase.md:

**IMPLEMENT Cycle:**
1. Write test first, run to confirm failure
2. Commit: `git commit -m "test: [description]"`
3. Write minimal implementation to pass
4. Commit: `git commit -m "feat: [description]"`

**CRITICAL After Each Item:**
- Check off item in docs/checklists/phase-$ARGUMENTS.md
- Update TodoWrite tool to reflect progress

**Context Management:**
- Monitor token budget
- When context gets long (>50%), suggest /clear
- Before clearing, commit work and update checklist

**DOCUMENT After Each GROUP:**
- Append summary to docs/learning-logs/phase-$ARGUMENTS-log.md
- Include: what was built, key decisions, code snippets, sample output
- Commit: `git add docs/... && git commit -m "docs: update checklist and learning log after GROUP X"`
- Provide standardized summary (see start-phase.md line 72-90)
- Ask user if they want to /clear before next GROUP

**DOCUMENT After FINAL GROUP (Phase Complete):**
- Complete Phase Summary in docs/learning-logs/phase-$ARGUMENTS-log.md
- Update MASTER_LOG.md with phase-specific implementation details and patterns
- Update CLAUDE.md Development Patterns ONLY if general, reusable patterns were discovered
- See start-phase.md line 58-69 for documentation guidelines

### Step 4: Validation

Before starting:
- If all items are checked, inform user that phase is complete
- If checklist file doesn't exist, suggest running /start-phase instead
- If implementation plan doesn't exist, warn user and ask how to proceed

### Reference

For complete workflow details, see .claude/commands/start-phase.md sections 3 and 4 (IMPLEMENT and DOCUMENT).

Begin by loading context and displaying the progress summary now.
