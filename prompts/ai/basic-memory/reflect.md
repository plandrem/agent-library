---
description: Capture learnings from current session into basic memory
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - LS
  - Bash
model: opus
disable-model-invocation: false
---

## Goal

Update the memory file with relevant experiences to improve reliability and performance in future work

## Workflow

### Step 1. Locate memory files

Read `$CLAUDE_PROJECT_DIR/.memories.md` and `~/.claude/.memories.md`. If either does not exist, run /ai:basic-memory:init to set up.

### Step 2. Enumerate Learnings

Thoroughly explore the session transcript up to this point. Identify all of the following:
- Feedback from the user
- Failed tool calls
- New resources discovered
- Gotchas
- Work that had to be redone
- Anything else matching a section header from the memories file

### Step 3. Prompt the User

FOR EACH potential learning: AskUserQuestion with "Capture memory? global/project/skip"

- **global**: Write to `~/.claude/.memories.md` (applies across all projects)
- **project**: Write to `$CLAUDE_PROJECT_DIR/.memories.md` (applies to current project only)
- **skip**: Do not capture this learning

### Step 4. Commit to memory

Based on user selection:
- **global**: Append to `~/.claude/.memories.md`
- **project**: Append to `$CLAUDE_PROJECT_DIR/.memories.md`
- **skip**: Do not write

## Examples

### Trigger Phrases

Look for the following in user messages as possible opportunities to learn:
- "should have"
- "you didn't"
- "Always"
- "Don't"
- "I want"
- "Why did you"

etc.

### Example 1: User Feedback on Code Style
**Session event:** User says "Please use f-strings instead of .format()"
**Learning type:** User Preferences
**Memory entry:** "Prefer f-strings over .format() for string interpolation"

### Example 2: Failed Tool Call - File Not Found
**Session event:** Read tool fails with "File not found: /src/utils.py"
**Learning type:** Failed tool call
**Memory entry:** "Project uses /lib/ directory instead of /src/ for utility modules"

### Example 3: Discovered Resource
**Session event:** Found comprehensive API docs at docs/api-reference.md
**Learning type:** New resource discovered
**Memory entry:** "API documentation located at docs/api-reference.md - check before implementing endpoints"

### Example 4: Gotcha - Environment Variable
**Session event:** Tests failed because DATABASE_URL wasn't set
**Learning type:** Gotcha
**Memory entry:** "Tests require DATABASE_URL environment variable; run `source .env.test` before pytest"

### Example 5: Rework from Previous Session
**Session event:** User says "this project should have used CSVs instead of sqlite"
**Learning type:** Work that had to be redone
**Memory entry:** "Incorrectly used sqlite instead of CSVs. Adhere to plan document and check with user before any departures."

### Example 6: Failed Tool Call - Permission Denied
**Session event:** Bash command failed writing to /etc/hosts
**Learning type:** Failed tool call
**Memory entry:** "System files require sudo; prefer project-local configuration when possible"

### Example 7: User Preference
**Session event:** User: "I prefer explicit type annotations even for obvious types"
**Learning type:** User feedback
**Memory entry:** "Add type annotations to all variables, not just function signatures"

### Example 8: Discovered Pattern
**Session event:** Found that all services follow a factory pattern in services/
**Learning type:** Best Practices
**Memory entry:** "Services use factory pattern: create_*_service() functions in services/__init__.py"

### Example 9: Gotcha - Test Database
**Session event:** Integration tests modified production data
**Learning type:** Gotcha
**Memory entry:** "Integration tests must use TEST_MODE=1 flag to target test database"

### Example 10: Rework - Wrong Test Strategy
**Session event:** Wrote unit tests, then discovered project uses integration tests only
**Learning type:** Work that had to be redone
**Memory entry:** "Check tests/ directory structure first; project prefers integration over unit tests"

## Response

"Created N new memories."
