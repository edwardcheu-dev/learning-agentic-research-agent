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
   - AFTER /clear, follow this prompt pattern:

     "/clear

     We're working on Phase $ARGUMENTS. Current progress is tracked in
     docs/checklists/phase-$ARGUMENTS.md. Continue with the next unchecked item."

   - See docs/reference/sample-prompts.md "When Context Gets Long" section

4. DOCUMENT (after completing a logical group of items):

   CRITICAL: Documentation is REQUIRED after each GROUP, not just at the end.

   - Append a summary to docs/learning-logs/phase-$ARGUMENTS-log.md
   - Include: what was built, key decisions, code snippets with explanations, sample output
   - Update docs/checklists/phase-$ARGUMENTS.md to mark GROUP as complete
   - Commit all documentation together:
     git add docs/checklists/phase-$ARGUMENTS.md docs/learning-logs/phase-$ARGUMENTS-log.md docs/implementation_plans/phase-$ARGUMENTS.md
     git commit -m "docs: update implementation plan, checklist, and learning log after GROUP X"

   After documenting:
   - Summarize what was implemented and how it connects to the bigger picture
   - Recommend any updates to CLAUDE.md based on patterns established
   - ASK USER if they want to /clear before continuing to next GROUP

Do not write any code until the checklist is approved. Start with exploration now.