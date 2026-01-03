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

For each checklist item, follow TDD cycle from [CONTRIBUTING.md#tdd-workflow-with-helper-commands](../CONTRIBUTING.md#tdd-workflow-with-helper-commands):

1. Write test first, run to confirm failure
2. Commit: `just test-commit "[description]"`
3. Write minimal code to pass test
4. Commit: `just feat-commit "[description]"`

**After EACH completion**:
- Check off item in `docs/checklists/phase-$ARGUMENTS.md`
- Update TodoWrite tool to reflect progress

**Manual Verification (when GROUP requires it)**:
1. Claude creates test plan: `docs/test-plans/phase-$ARGUMENTS-group-X.md`
2. Claude provides verification summary and asks user to test
3. User follows test plan steps manually
4. User reports results (approve/issues found)
5. Claude documents verification in learning log
6. Only after user approval: proceed to next GROUP

**Test Plan Template**:
Test plans include:
- Prerequisites (what must be running, environment setup)
- Step-by-step verification instructions with expected outcomes
- Edge cases to test
- Success criteria checklist
- Failure troubleshooting guide

**Context Management**:
- Monitor token budget (>50% used? suggest `/clear`)
- Before clearing: commit work and update checklist
- After `/clear`, use: `/resume-phase $ARGUMENTS`

### 4. DOCUMENT

**After Each GROUP**:
1. If GROUP requires manual verification:
   - Create test plan document
   - Summarize verification steps for user
   - WAIT for user approval before proceeding
   - Document user approval in learning log
2. Append summary to `docs/learning-logs/phase-$ARGUMENTS-log.md`
   - What was built
   - Key decisions
   - Code snippets with explanations
   - **Manual Verification Results** (if applicable)
   - Sample output
3. Update checklist to mark GROUP complete
4. Update README.md progress tracking:
   - Recalculate phase percentage (completed_groups / total_groups)
   - Update "Completed Groups" section with ✅ for finished GROUP
   - If manual verification: Update "Manual Verifications" with ✅ status
   - Update status badge if phase percentage changed significantly
5. Commit all documentation:
   ```bash
   just docs-commit "update checklist, learning log, and README after GROUP X"
   ```
6. Provide standardized summary (see template below)
7. Ask user if they want to `/clear` before next GROUP

**After FINAL GROUP** (Phase Complete):
1. Complete Phase Summary in `docs/learning-logs/phase-$ARGUMENTS-log.md`
2. Update `MASTER_LOG.md` with phase-specific implementation details
3. Update `CLAUDE.md` Development Patterns ONLY if general, reusable patterns discovered
4. Commit: `just docs-commit "complete Phase $ARGUMENTS documentation"`

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
- README.md updated: ✅
- [If final GROUP] MASTER_LOG.md: [Pending/Completed]
- [If final GROUP] CLAUDE.md: [Updated / No general patterns to add]
```

Ask user if they want to `/clear` before continuing.

## Important

Do not write code until checklist is approved. Start with exploration now.
