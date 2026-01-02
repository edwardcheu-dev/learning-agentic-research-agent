Starting Phase $ARGUMENTS of the Research Assistant project.

## Prerequisites

Read for context:
- **CLAUDE.md** - Project overview, architecture, patterns
- **CONTRIBUTING.md** - Complete development workflow and standards

## Workflow

### 1. EXPLORE

Use subagents to investigate:
- Project context from CLAUDE.md
- Relevant patterns from previous phases
- External documentation or concepts needed for this phase
- Existing code patterns to follow

Report findings before proceeding.

### 2. PLAN

Based on exploration:
- Create detailed implementation plan
- Create/update checklist at `docs/checklists/phase-$ARGUMENTS.md`
- Group related items under logical headings (GROUP 1, GROUP 2, etc.)
- Each item should be small enough for one test + implementation cycle

Wait for approval before proceeding.

**CRITICAL**: After approval, save full implementation plan to:
`docs/implementation_plans/phase-$ARGUMENTS.md`

### 3. IMPLEMENT

For each checklist item, follow TDD cycle from [CONTRIBUTING.md#commit-message-format](../CONTRIBUTING.md#commit-message-format):

1. Write test first, run to confirm failure
2. Commit: `git commit -m "test: [description]"`
3. Write minimal code to pass test
4. Commit: `git commit -m "feat: [description]"`

**After EACH completion**:
- Check off item in `docs/checklists/phase-$ARGUMENTS.md`
- Update TodoWrite tool to reflect progress

**Context Management**:
- Monitor token budget (>50% used? suggest `/clear`)
- Before clearing: commit work and update checklist
- After `/clear`, use: `/resume-phase $ARGUMENTS`

### 4. DOCUMENT

**After Each GROUP**:
1. Append summary to `docs/learning-logs/phase-$ARGUMENTS-log.md`
   - What was built
   - Key decisions
   - Code snippets with explanations
   - Sample output
2. Update checklist to mark GROUP complete
3. Commit both:
   ```bash
   git add docs/checklists/phase-$ARGUMENTS.md docs/learning-logs/phase-$ARGUMENTS-log.md
   git commit -m "docs: update checklist and learning log after GROUP X"
   ```
4. Provide standardized summary (see template below)
5. Ask user if they want to `/clear` before next GROUP

**After FINAL GROUP** (Phase Complete):
1. Complete Phase Summary in `docs/learning-logs/phase-$ARGUMENTS-log.md`
2. Update `MASTER_LOG.md` with phase-specific implementation details
3. Update `CLAUDE.md` Development Patterns ONLY if general, reusable patterns discovered
4. Commit: `git commit -m "docs: complete Phase $ARGUMENTS documentation"`

See [CONTRIBUTING.md#documentation-standards](../CONTRIBUTING.md#documentation-standards) for full requirements.

## Summary Template

After documenting each GROUP:

```
## Summary
[Brief description of what was built in this GROUP]

## How It Connects to the Bigger Picture
- GROUP 1-X: [What's been completed] ✅
- Current GROUP: [What was just finished] ✅
- Next GROUP: [What's coming next]

## Token Usage
Currently at ~[X]k / 200k tokens ([Y]%) - [assessment]

## Documentation Updates
- Phase log updated: ✅
- [If final GROUP] MASTER_LOG.md: [Pending/Completed]
- [If final GROUP] CLAUDE.md: [Updated / No general patterns to add]
```

Ask user if they want to `/clear` before continuing.

## Important

Do not write code until checklist is approved. Start with exploration now.
