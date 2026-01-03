Resuming Phase $ARGUMENTS of the Research Assistant project.

## Your Task: Resume Implementation

Jump straight into IMPLEMENT mode - EXPLORE and PLAN are complete.

## Step 1: Load Context

Read these files to understand current state:
1. `docs/checklists/phase-$ARGUMENTS.md` - Find next unchecked item
2. `docs/implementation_plans/phase-$ARGUMENTS.md` - Reference architecture and goals
3. Run `git log --oneline -5` - See what was just completed

## Step 2: Display Progress Summary

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

## Step 3: Continue Implementation

Follow TDD workflow from [CONTRIBUTING.md#tdd-workflow-with-helper-commands](../CONTRIBUTING.md#tdd-workflow-with-helper-commands):

1. Write test first, run to confirm failure
2. Commit: `just test-commit "[description]"`
3. Write minimal implementation to pass
4. Commit: `just feat-commit "[description]"`

**CRITICAL After Each Item**:
- Check off item in `docs/checklists/phase-$ARGUMENTS.md`
- Update TodoWrite tool to reflect progress

**Context Management**:
- Monitor token budget
- When context gets long (>50%), suggest `/clear`
- Before clearing, commit work and update checklist

**DOCUMENT After Each GROUP**:
- Append summary to `docs/learning-logs/phase-$ARGUMENTS-log.md`
- Include: what was built, key decisions, code snippets, sample output
- Commit: `just docs-commit "update checklist and learning log after GROUP X"`
- Provide standardized summary (see [start-phase.md](start-phase.md))
- Ask user if they want to `/clear` before next GROUP

**DOCUMENT After FINAL GROUP** (Phase Complete):
- Complete Phase Summary in `docs/learning-logs/phase-$ARGUMENTS-log.md`
- Update `MASTER_LOG.md` with phase-specific implementation details
- Update `CLAUDE.md` Development Patterns ONLY if general, reusable patterns discovered

See [CONTRIBUTING.md#documentation-standards](../CONTRIBUTING.md#documentation-standards) for full details.

## Step 4: Validation

Before starting:
- If all items checked → inform user phase is complete
- If checklist doesn't exist → suggest running `/start-phase` instead
- If implementation plan missing → warn user and ask how to proceed

Begin by loading context and displaying the progress summary now.
