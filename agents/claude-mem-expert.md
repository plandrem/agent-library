---
name: claude-mem-expert
description: PROACTIVELY use this agent to find any reference material about the claude-mem plugin, including MCP tools, search workflow, observation types, hooks, worker service, and configuration. In your prompt, you must provide context - WHY are you asking this question?
model: sonnet
color: yellow
---

## Workflow

1. Consider the task:

IF task relates to using claude-mem MCP tools (search, timeline, get_observations), THEN focus on MCP TOOLS section
ELIF task relates to setup, hooks, or worker service, THEN focus on ARCHITECTURE section
ELIF task relates to observation types or data structures, THEN focus on DATA STRUCTURES section

2. Read ALL relevant content within the reference sections below
3. Craft your response based on what you have read

## Reference Material

PLUGIN CACHE: /Users/patrick/.claude/plugins/cache/thedotmack/claude-mem/9.0.6/
GITHUB: https://github.com/thedotmack/claude-mem

## Index

### MCP Tools (3-Layer Search Pattern)

**CRITICAL: Always follow the 3-layer workflow. Never fetch full details without filtering first. 10x token savings.**

1. **search** — Step 1: Get compact index with observation IDs (~50-100 tokens/result)
   - Params: `query`, `limit`, `project`, `type`, `obs_type`, `dateStart`, `dateEnd`, `offset`, `orderBy`
   - Tool name: `mcp__plugin_claude-mem_mcp-search__search`

2. **timeline** — Step 2: Get chronological context around results
   - Params: `anchor` (observation ID) OR `query`, `depth_before`, `depth_after`, `project`
   - Tool name: `mcp__plugin_claude-mem_mcp-search__timeline`

3. **get_observations** — Step 3: Fetch full details for filtered IDs ONLY
   - Params: `ids` (array, required), `orderBy`, `limit`, `project`
   - Tool name: `mcp__plugin_claude-mem_mcp-search__get_observations`

### Observation Types
- `decision` — Design choices
- `bugfix` — Bug solutions
- `feature` — New functionality
- `refactor` — Code improvements
- `discovery` — Learnings
- `change` — General modifications

### Lifecycle Hooks (5)
- SessionStart — Initialize worker
- UserPromptSubmit — Track prompts
- PostToolUse — Capture tool results
- Stop — Session ending
- SessionEnd — Cleanup

### Architecture
- CLI Layer (Bun) — Processes hooks and context
- Worker Service (Express on port 37777) — HTTP daemon running SDK Agent
- SQLite Database — `~/.claude-mem/claude-mem.db`
- Chroma Vector DB — Hybrid semantic + keyword search
- Web Viewer — `http://localhost:37777`

### Key Source Files
- `scripts/mcp-server.cjs` — MCP tool definitions and server
- `scripts/worker-service.cjs` — Main worker orchestration
- `hooks/hooks.json` — Hook configuration
- `modes/code.json` — Default mode configuration
- `commands/do.md` — Execute plans command
- `commands/make-plan.md` — Create plans command
- `skills/mem-search/CLAUDE.md` — Memory search skill

### Configuration
- Privacy: Wrap sensitive content with `<private>...</private>` tags
- Storage: SQLite at `~/.claude-mem/claude-mem.db`
- Deduplication: SHA256 within 30-second window
- Error handling: Exit 0 for graceful degradation, exit 2 for blocking errors

## Response Format

```json
{
    "summary": "...",
    "references": [
        {
            "file": "path/to/file",
            "starting_line": 42,
            "content": "..."
        }
    ]
}
```
