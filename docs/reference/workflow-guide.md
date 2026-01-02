# Development Workflow Guide

## Overview

This project uses a structured workflow combining:

1. Exploration - Understand before coding
2. Planning - Checklist-driven development
3. TDD - Tests before implementation
4. Atomic Commits - Small, focused changes
5. Learning Logs - Document as you build

## Claude Code Modes

Press Shift+Tab to cycle through modes. The cycle order is:

    Normal Mode → Auto-Accept Edits → Plan Mode → Normal Mode...

### Normal Mode (Default)

Claude asks for confirmation before making file changes.

Use when:

- Learning Claude Code for the first time
- Working on critical or sensitive code
- You want to review each change before it happens
- Making changes you're unsure about

### Auto-Accept Edits Mode (1x Shift+Tab)

Claude writes files without asking permission. Still prompts for bash commands.

Use when:

- Implementing well-defined checklist items
- Doing routine refactoring
- You trust the current task is well-scoped
- Running through TDD cycles (test → implement → commit)
- Large refactoring or repetitive tasks

Avoid when:

- Working on unfamiliar code
- Making architectural decisions
- You haven't clearly defined the task

This is the recommended mode for most development work once you're comfortable.

### Plan Mode (2x Shift+Tab)

Claude can only read, search, and research. Cannot edit files or run commands.

Use when:

- Starting a new phase
- Complex feature planning
- Understanding unfamiliar code before modifying
- You want a plan presented before any execution
- Early stages of a project

After reviewing a plan, Claude will offer options to execute. Selecting "Yes, and
auto-accept edits" will switch to Auto-Accept mode and execute the plan.

### Quick Reference

| Mode              | Shift+Tab | File Edits       | Bash Commands    |
|-------------------|-----------|------------------|------------------|
| Normal            | 0x        | Asks permission  | Asks permission  |
| Auto-Accept Edits | 1x        | Auto-approved    | Asks permission  |
| Plan Mode         | 2x        | Disabled         | Disabled         |

Note: On Windows, you may need to use Alt+M instead of Shift+Tab.

## The Flow

    START PHASE
         │
         ▼
    ┌─────────────────────────────────────────────────────────┐
    │  1. EXPLORE (use Plan Mode - Shift+Tab twice)           │
    │     - Use subagents to investigate                      │
    │     - Read relevant files, docs, patterns               │
    │     - Report findings before proceeding                 │
    └─────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────────────┐
    │  2. PLAN                                                │
    │     - Create checklist in docs/checklists/phase-N.md    │
    │     - Break into small, testable items                  │
    │     - Wait for approval                                 │
    └─────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────────────┐
    │  3. IMPLEMENT (switch to Auto-Accept - Shift+Tab once)  │
    │                                                         │
    │     a. Write test                                       │
    │     b. Run test (confirm fail)                          │
    │     c. Commit: "test: description"                      │
    │     d. Write implementation                             │
    │     e. Run test (confirm pass)                          │
    │     f. Commit: "feat: description"                      │
    │     g. Check off item in checklist                      │
    │     h. /clear if context is long                        │
    │                                                         │
    │     After logical group complete:                       │
    │     - Update learning log                               │
    │     - Commit: "docs: update phase N log"                │
    └─────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────────────┐
    │  4. COMPLETE PHASE                                      │
    │     - Update MASTER_LOG.md with phase summary           │
    │     - Update CLAUDE.md with patterns learned            │
    │     - Final phase commit                                │
    └─────────────────────────────────────────────────────────┘
         │
         ▼
    NEXT PHASE

## Commit Prefixes

| Prefix      | Use For                              | Example                                         |
|-------------|--------------------------------------|-------------------------------------------------|
| test:       | Adding tests before implementation   | test: agent returns response for simple query   |
| feat:       | Implementation that passes tests     | feat: implement basic agent response loop       |
| refactor:   | Improving code without behavior change | refactor: extract tool selection logic        |
| docs:       | Documentation updates                | docs: update phase 1 learning log               |
| chore:      | Build, config, tooling               | chore: add pytest-cov to dev dependencies       |

## When to Use Subagents

Good uses:

- Investigating unfamiliar code before modifying
- Researching how a library works
- Checking patterns across multiple files
- Verifying implementation details

Avoid for:

- Simple, focused tasks
- When you already know what to do
- Trivial file reads

## When to /clear

Clear when:

- Switching between checklist groups
- Context feels cluttered
- Starting a new logical unit of work
- After completing documentation updates

Do not clear when:

- In the middle of implementing a feature
- When you need previous context for current task

## Learning Log Guidelines

Each log entry should include:

1. What We Built - Concrete deliverables
2. Key Decisions - Why we chose certain approaches
3. Code Highlights - Important snippets with explanations
4. Sample Output - Show it working
5. Lessons Learned - Insights for future reference

The MASTER_LOG.md aggregates these into a tutorial-style document.
