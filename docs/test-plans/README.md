# Manual Verification Test Plans

This directory contains structured test plans for manual verification of features during implementation.

## Purpose

While automated tests verify code correctness, manual verification ensures:
- User experience matches requirements
- Visual/interactive elements work as expected
- Edge cases are covered
- Real-world usage patterns are validated

## Structure

Each test plan follows this template:
- **Prerequisites**: Environment setup, dependencies
- **Verification Steps**: Step-by-step instructions with expected outcomes
- **Edge Cases**: Uncommon scenarios to test
- **Success Criteria**: Checklist of requirements
- **Troubleshooting**: Common issues and solutions

## Workflow

1. Claude completes GROUP implementation
2. Claude creates test plan: `phase-N-group-M.md`
3. User follows test plan manually
4. User reports results (approve/issues)
5. Claude documents verification in learning log
6. On approval: Claude proceeds to next GROUP

## File Naming

Format: `phase-{N}-group-{M}.md`

Examples:
- `phase-2-group-2.md` - Basic TUI Shell verification
- `phase-2-group-4.md` - Streaming LLM Tokens verification
