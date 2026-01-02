Starting Phase $ARGUMENTS of the Research Assistant project.

Follow this workflow:

1. EXPLORE (use subagents liberally here):
   - Use a subagent to read CLAUDE.md and summarize the project context
   - Use a subagent to read and summarize relevant files for this phase
   - Use a subagent to check if there are patterns from previous phases to follow
   - Use a subagent to investigate any external docs or concepts needed
   - Report findings to me before proceeding

2. PLAN:
   - Based on exploration, create a detailed implementation plan
   - Create or update the checklist at docs/checklists/phase-$ARGUMENTS.md
   - Each checklist item should be small enough for one test + implementation cycle
   - Group related items under logical headings (GROUP 1, GROUP 2, etc.)
   - Wait for my approval before proceeding

   CRITICAL: After plan approval, SAVE the full implementation plan to:
   docs/implementation_plans/phase-$ARGUMENTS.md

   This ensures the plan is preserved for reference during implementation.

3. IMPLEMENT (for each checklist item):

   TDD Cycle:
   - Write the test first, run it to confirm it fails
   - Commit with: git commit -m "test: [description]"
   - Write minimal code to pass the test
   - Commit with: git commit -m "feat: [description]"

   CRITICAL: After EACH completion:
   - Check off the item in docs/checklists/phase-$ARGUMENTS.md
   - Update the todo list with TodoWrite tool to reflect progress

   Context Management:
   - Monitor context length - when it gets long (>50% budget), suggest /clear
   - Before clearing, commit any pending work and update the checklist
   - AFTER /clear, use the resume-phase command to quickly restore context:

     "/resume-phase $ARGUMENTS"

   - This command will load progress, display the next item, and jump into IMPLEMENT mode
   - See docs/reference/sample-prompts.md "When Context Gets Long" section

4. DOCUMENT (after completing a logical group of items):

   CRITICAL: Documentation is REQUIRED after each GROUP, not just at the end.

   After Each GROUP:
   - Append a summary to docs/learning-logs/phase-$ARGUMENTS-log.md
   - Include: what was built, key decisions, code snippets with explanations, sample output
   - Update docs/checklists/phase-$ARGUMENTS.md to mark GROUP as complete
   - Commit all documentation together:
     git add docs/checklists/phase-$ARGUMENTS.md docs/learning-logs/phase-$ARGUMENTS-log.md
     git commit -m "docs: update checklist and learning log after GROUP X"

   After FINAL GROUP (Phase Complete):
   - Complete the Phase Summary section in docs/learning-logs/phase-$ARGUMENTS-log.md
   - Update MASTER_LOG.md with Phase $ARGUMENTS section (implementation details, architecture, patterns)
   - Update CLAUDE.md Development Patterns ONLY if you discovered GENERAL, REUSABLE patterns
   - Commit: git commit -m "docs: complete Phase $ARGUMENTS documentation"

   Documentation Guidelines:
   - phase-$ARGUMENTS-log.md: Detailed session-by-session implementation log
   - MASTER_LOG.md: High-level tutorial explaining how the system works (phase-specific patterns and architecture)
   - CLAUDE.md Development Patterns: ONLY general patterns that apply across ALL phases
     * What goes in CLAUDE.md: Testing strategies, error handling conventions, code organization
     * What does NOT go in CLAUDE.md: ReAct loops, RAG pipelines, MCP servers (those go in MASTER_LOG.md)

   After documenting:
   - Provide a standardized summary in the following format:

     ## Summary
     [Brief description of what was built in this GROUP]

     ## How It Connects to the Bigger Picture
     - GROUP 1-X: [What's been completed] ✅
     - Current GROUP: [What was just finished] ✅
     - Next GROUP: [What's coming next]

     ## Token Usage
     Currently at ~[X]k / 200k tokens ([Y]%) - [assessment of remaining capacity]

     ## Documentation Updates
     - Phase log updated: ✅
     - [If final GROUP] MASTER_LOG.md: [Pending/Completed]
     - [If final GROUP] CLAUDE.md: [Updated with general patterns / No general patterns to add]

   - ASK USER if they want to /clear before continuing to next GROUP

Do not write any code until the checklist is approved. Start with exploration now.
