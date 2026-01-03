Resuming Phase $ARGUMENTS of the Research Assistant project.

## Your Task: Resume Implementation

Jump straight into IMPLEMENT mode - EXPLORE and PLAN are complete.

## Step 1: Load Context

Read these files to understand current state:
1. `docs/checklists/phase-$ARGUMENTS.md` - Check implementation AND verification status
2. `docs/implementation_plans/phase-$ARGUMENTS.md` - Reference architecture and goals
3. Run `git log --oneline -5` - See what was just completed

### Verification Detection

For each GROUP in checklist:
1. Check if all implementation items are [x] checked
2. Look for "Manual Verification" section
3. Check verification status:
   - `⏸️ PENDING USER VERIFICATION` → Pause here, ask user to verify
   - `✅ VERIFIED` → Continue to next GROUP
   - `⚠️ ISSUES FOUND` → Check if issues are resolved
4. If "User has verified and approved" is [ ] unchecked → Needs verification
5. If test plan exists but verification section missing → Needs verification

**Priority Order**:
1. First, complete any pending manual verifications
2. Then, resume implementation of next GROUP

## Step 2: Display Progress Summary

```
# Phase $ARGUMENTS Progress

## Checklist Overview
[Display each GROUP with completion status AND verification status]
Example:
- GROUP 1: Phase Restructuring & Setup ✅
- GROUP 2: Basic TUI Shell ✅ ⚠️ Needs Verification
- GROUP 3: Async Agent Foundation ✅ (No verification required)
- GROUP 4: Streaming LLM Tokens ✅ ⚠️ Needs Verification
- GROUP 5: ReAct Step Visualization (Not started)

## ⚠️ Manual Verification Status

**Pending Verifications**:
[List all GROUPs with PENDING status]

Example:
1. GROUP 2: Basic TUI Shell
   - Test Plan: `docs/test-plans/phase-2-group-2.md`
   - Status: ⏸️ PENDING USER VERIFICATION
   - Action: User needs to verify

2. GROUP 4: Streaming LLM Tokens
   - Test Plan: `docs/test-plans/phase-2-group-4.md`
   - Status: ⏸️ PENDING USER VERIFICATION
   - Action: User needs to verify (after GROUP 2)

## Current Focus

**If manual verification pending**:
Next Action: Verify GROUP X
- Test Plan: `docs/test-plans/phase-$ARGUMENTS-group-X.md`
- Please follow the test plan and report results

**If no verification pending**:
GROUP X: [GROUP name]
- Progress: X/Y items complete
- Next Item: [ ] [Description of next unchecked item]

## Recent Commits
[Show last 5 commits from git log]

## Ready to Continue

**If verification pending**:
Please verify GROUP X using the test plan above. Report:
- APPROVED: All checks passed
- ISSUES: [describe what failed]

**If no verification pending**:
I'll now work on: [next unchecked item description]
```

## Step 3: Continue Implementation

**PRIORITY: Manual Verification First**

If Step 2 identified pending verifications:
1. DO NOT proceed with new implementation
2. Provide test plan summary for first pending GROUP
3. Ask user to verify and report results
4. Wait for user response
5. Update checklist based on results:
   - If APPROVED: Mark `✅ VERIFIED`, proceed to next verification or implementation
   - If ISSUES: Mark `⚠️ ISSUES FOUND`, investigate and fix issues
6. Only after all verifications complete: resume implementation

**If No Pending Verifications**:

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
- Update `README.md` with phase progress (percentage, completed groups, verification status)
- Commit: `just docs-commit "update checklist, learning log, and README after GROUP X"`
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
