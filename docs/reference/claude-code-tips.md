# Claude Code Tips and Reference

## Keyboard Shortcuts

| Shortcut          | Action                                      |
|-------------------|---------------------------------------------|
| Shift+Tab         | Cycle modes: Normal → Auto-Accept → Plan    |
| Ctrl+C            | Cancel current operation                    |
| Ctrl+L            | Clear terminal (keeps context)              |
| Escape            | Interrupt current generation                |
| Up Arrow          | Previous prompt (in input)                  |

Note: On Windows, use Alt+M instead of Shift+Tab for mode switching.

## Modes

Claude Code has three modes. Press Shift+Tab to cycle through them.

### Normal Mode (Default)

    Status bar: (none or "Normal")

Behavior:

- Claude asks permission before editing files
- Claude asks permission before running bash commands
- You approve or reject each action

Best for:

- New Claude Code users learning the tool
- Working on critical or sensitive code
- Unfamiliar codebases
- When you want maximum control

### Auto-Accept Edits Mode

    Status bar: "Auto-accept edits on"

Behavior:

- Claude edits files without asking
- Claude still asks permission for bash commands
- Faster iteration on well-defined tasks

Best for:

- TDD cycles (test → implement → commit)
- Implementing approved checklist items
- Routine refactoring
- Bulk file operations
- Most everyday development work

Activate: Press Shift+Tab once from Normal Mode.

### Plan Mode

    Status bar: "Plan mode"

Behavior:

- Claude cannot edit files
- Claude cannot run commands
- Claude can only read, search, and research
- Presents a plan for your approval

Best for:

- Starting new phases or features
- Investigating unfamiliar code
- Complex architectural decisions
- When you want analysis before action

Activate: Press Shift+Tab twice from Normal Mode.

After Claude presents a plan, you will see options:

- "Yes" - Execute in Normal Mode
- "Yes, and auto-accept edits" - Execute in Auto-Accept Mode
- "No" - Refine the plan

### Mode Quick Reference

    ┌─────────────────────────────────────────────────────────────┐
    │                      MODE CYCLE                             │
    │                                                             │
    │    ┌──────────┐   Shift+Tab   ┌─────────────┐   Shift+Tab   │
    │    │  Normal  │ ───────────▶  │ Auto-Accept │ ───────────▶  │
    │    └──────────┘               └─────────────┘               │
    │          ▲                                                  │
    │          │                         ┌───────────┐            │
    │          └──────── Shift+Tab ───── │ Plan Mode │            │
    │                                    └───────────┘            │
    └─────────────────────────────────────────────────────────────┘

## Slash Commands

| Command      | Description                                     |
|--------------|-------------------------------------------------|
| /clear       | Clear conversation context (start fresh)        |
| /compact     | Condense conversation to save context space     |
| /config      | Open or modify configuration                    |
| /cost        | Show token usage and cost for session           |
| /doctor      | Troubleshoot Claude Code installation           |
| /help        | Show available commands                         |
| /init        | Initialize CLAUDE.md in current project         |
| /login       | Switch accounts or re-authenticate              |
| /logout      | Sign out of current session                     |
| /memory      | Edit CLAUDE.md memory file                      |
| /model       | Switch Claude model                             |
| /project     | Run custom project commands from .claude/       |
| /review      | Request code review of recent changes           |
| /terminal    | Run terminal commands directly                  |
| /vim         | Toggle vim keybindings for input                |

## Subagents (Task Tool)

Subagents are independent Claude instances for parallel or isolated work.

Spawn with natural language:

    Use a subagent to investigate how the authentication module works.

Good uses:

- Researching libraries or patterns
- Reading multiple files to find patterns
- Verifying implementation details
- Parallel investigation tasks

Subagents cannot:

- Edit files
- Run bash commands
- Access previous conversation context

## Context Management

### When to /clear

Clear context when:

- Switching between logical groups of work
- Context feels cluttered or confused
- Starting a new phase or feature
- After completing documentation updates

Do not clear when:

- In the middle of implementing a feature
- You need prior context for current task
- Debugging requires seeing previous attempts

### When to /compact

Use /compact when:

- Context is getting long but you need continuity
- You want to preserve key decisions but reduce noise
- Mid-phase but switching focus slightly

## Project Commands

Custom commands live in .claude/commands/ as markdown files.

Example structure:

    .claude/
    └── commands/
        ├── start-phase.md
        ├── update-docs.md
        └── run-tests.md

Run with:

    /project:start-phase 1

Arguments are passed as $ARGUMENTS in the command template.

## Tips for Effective Use

### Be Specific

Instead of:

    Fix the bug

Try:

    The test in tests/test_agent.py::test_response_format is failing with
    "KeyError: 'content'". Fix the bug in src/agent.py.

### Use Think Prompts for Complex Problems

    Think hard about why the agent loop might be hanging when no tools are
    available.

    Think step by step about how to refactor this module to support streaming.

### Provide Context in Prompts

    Looking at src/tools/base.py, add a new validation method that follows
    the same pattern as the existing validate_input method.

### Chain Commands Explicitly

    Run the tests. If they pass, commit with message "feat: add retry logic".
    If they fail, fix the issues and try again.

## Configuration

Settings live in:

- Project: .claude/settings.json
- Global: ~/.claude/settings.json

Common settings:

    {
      "permissions": {
        "allow": ["bash:git *", "bash:uv *", "bash:pytest *"],
        "deny": ["bash:rm -rf *"]
      },
      "env": {
        "CLAUDE_CODE_EDITOR": "vim"
      }
    }

## Troubleshooting

### Claude Not Seeing Recent Changes

    /clear

Then re-state what you need.

### Claude Making Wrong Assumptions

    Stop. Read the file src/agent.py first, then continue with the
    implementation.

### Context Too Long

    /compact

Or for a fresh start:

    /clear

    Continue Phase 1 from the checklist. Read docs/checklists/phase-1.md
    to see current progress.

### Mode Not Switching (Windows)

Try Alt+M instead of Shift+Tab.