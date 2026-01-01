Starting Phase $ARGUMENTS of the Research Assistant project.

Follow this workflow:

1. EXPLORE (use subagents liberally here):
   - Use a subagent to read CLAUDE.md and summarize the project context
   - Use a subagent to read and summarize relevant files for this phase
   - Use a subagent to check if there are patterns from previous phases to follow
   - Use a subagent to investigate any external docs or concepts needed
   - Report findings to me before proceeding

2. PLAN:
   - Based on exploration, create a detailed checklist at docs/checklists/phase-$ARGUMENTS.md
   - Each checklist item should be small enough for one test + implementation cycle
   - Group related items under logical headings
   - Wait for my approval before proceeding

3. IMPLEMENT (for each checklist item):
   - Write the test first, run it to confirm it fails
   - Commit with: git commit -m "test: [description]"
   - Write minimal code to pass the test
   - Commit with: git commit -m "feat: [description]"
   - Check off the item in the checklist
   - Use /clear if context is getting long

4. DOCUMENT (after completing a logical group of items):
   - Append a summary to docs/learning-logs/phase-$ARGUMENTS-log.md
   - Include: what was built, key decisions, code snippets with explanations, sample output
   - Commit with: git commit -m "docs: update phase $ARGUMENTS learning log"
   - Summarize what was implemented and how it connects to the bigger picture
   - Recommend any updates to CLAUDE.md based on patterns established

Do not write any code until the checklist is approved. Start with exploration now.