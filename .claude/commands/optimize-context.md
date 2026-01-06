---
description: Check context usage and suggest optimizations for token efficiency
---

# Optimize Context

Check current context usage and suggest optimizations.

## Workflow

### 1. CHECK USAGE

Run `/cost` to see token consumption.

### 2. RECOMMEND ACTION

| Usage | Recommendation |
|-------|----------------|
| <30% | No action needed - context is healthy |
| 30-50% | Consider `/compact` to summarize conversation |
| 50-70% | Commit work, update checklist, use `/compact` |
| >70% | Commit, update docs, `/clear`, resume with `/resume-phase` |

### 3. PRE-CLEAR CHECKLIST

Before using `/clear`, ensure:

- [ ] All code changes committed
- [ ] Checklist updated with current progress
- [ ] Learning log updated with session insights
- [ ] TodoWrite reflects current state
- [ ] Note current GROUP for resume

### 4. RECOVERY PLAN

After `/clear`:

1. Confirm checklist is up to date
2. Confirm learning log is current
3. Resume work: `/resume-phase $N`

## Context Efficiency Tips

**Always Loaded** (minimize these):
- CLAUDE.md (~2k tokens target)
- `.claude/rules/*.md` (path-filtered)

**On-Demand** (use subagents):
- Debugging: Use `debugger` subagent
- Code review: Use `code-reviewer` subagent
- Phase research: Use `phase-explorer` subagent

**Best Practices**:
- Subagents run in isolated context (preserves main conversation)
- Skills load only when triggered (not always)
- Use @imports instead of duplicating content
