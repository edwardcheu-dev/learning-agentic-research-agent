Promote enhancement ideas into a new MVP phase in the project roadmap.

## Purpose

Convert high-priority enhancements (P0/P1) into:
- New phase in CLAUDE.md Implementation Phases
- Implementation plan in `docs/implementation_plans/`
- Checklist in `docs/checklists/`
- Learning log in `docs/learning-logs/`

## Workflow

### 1. SELECT ENHANCEMENTS

Ask user:
- Which enhancements to include (by title or category)
- Phase number (e.g., Phase 5, Phase 6)
- Phase theme/name (e.g., "Production Readiness", "Observability")

### 2. READ ENHANCEMENT PROPOSALS

Load selected enhancements from `docs/enhancements/`:
- Understand problem statements
- Review proposed solutions
- Identify dependencies between enhancements

### 3. GROUP AND PRIORITIZE

Organize enhancements into logical groups:
- **GROUP 1**: Foundation (prerequisite work)
- **GROUP 2**: Core implementation
- **GROUP 3**: Integration and testing
- **GROUP 4**: Documentation and cleanup

Display proposed structure to user for approval.

### 4. CREATE PHASE DOCUMENTATION

After approval, create:

**A. Implementation Plan** (`docs/implementation_plans/phase-N.md`):
```markdown
# Phase N: [Phase Name]

## Overview
[Description of what this phase accomplishes]

## Goals
1. [Primary goal 1]
2. [Primary goal 2]

## Enhancements Addressed
- [Enhancement 1 title] (from docs/enhancements/[category].md)
- [Enhancement 2 title] (from docs/enhancements/[category].md)

## Implementation Groups

### GROUP 1: [Group Name]
- [ ] Task 1
- [ ] Task 2

### GROUP 2: [Group Name]
- [ ] Task 1
- [ ] Task 2

[Continue for all groups]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**B. Checklist** (`docs/checklists/phase-N.md`):
Copy GROUP structure from implementation plan (unchecked items).

**C. Learning Log Stub** (`docs/learning-logs/phase-N-log.md`):
```markdown
# Phase N Learning Log: [Phase Name]

## Session Log

---

(Sessions will be added during implementation)
```

### 5. UPDATE CLAUDE.MD

Add new phase to Implementation Phases section (after existing phases):

```markdown
### Phase N: [Phase Name]

[Brief description of what this phase accomplishes]

**Key enhancements**:
- [Enhancement 1]
- [Enhancement 2]
```

### 6. UPDATE ENHANCEMENT STATUS

Mark promoted enhancements as **[Planned]** in their respective files:
```markdown
### Enhancement Title [P1] [Planned] ← Changed from [Idea]
```

Add reference to new phase:
```markdown
**Status**: Promoted to Phase N - see docs/implementation_plans/phase-N.md
```

### 7. COMMIT ALL CHANGES

```bash
git add docs/implementation_plans/phase-N.md \
        docs/checklists/phase-N.md \
        docs/learning-logs/phase-N-log.md \
        docs/enhancements/*.md \
        CLAUDE.md
git commit -m "docs: create Phase N ([Phase Name]) from enhancement proposals"
```

### 8. CONFIRM

Display summary:
```
✅ Phase N created and enhancements promoted

Phase: Phase N - [Phase Name]
Enhancements: [count] promoted
Files created:
  - docs/implementation_plans/phase-N.md
  - docs/checklists/phase-N.md
  - docs/learning-logs/phase-N-log.md
CLAUDE.md updated: ✅

Next steps:
- Review implementation plan
- Use `/start-phase N` to begin implementation
```

## Important

- Only promote P0/P1 enhancements (high priority)
- Group related enhancements into logical phases
- Update enhancement status to [Planned] with phase reference
- Create all 3 phase files (plan, checklist, log stub)
- Commit all changes together
- Suggest `/start-phase N` to begin implementation
