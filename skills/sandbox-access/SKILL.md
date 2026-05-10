---
name: sandbox-access
description: Use when encountering "tool blocked by sandbox", "command blocked", "domain blocked", "network access denied", or when needing to enable access to external domains, bash commands, or MCP server tools that are restricted by Apple's Claude Code sandbox.
version: 0.1.0
---

# Sandbox Access Management

## Overview

Apple Claude Code runs in a sandboxed environment that restricts access to certain bash commands, external domains, and tool executions for security. This skill enables access to blocked resources by adding them to the appropriate allowlist files.

When Claude encounters a blocked operation, it will receive an error indicating the resource is restricted. This skill provides the procedures to safely enable access by updating the CSV allowlist files that control sandbox permissions.

## Core Procedures

### Identify the Blocked Resource

When a tool is blocked, examine the error message to determine:
- **Bash command**: Look for command name (e.g., `ssh`, `docker`, `npx`)
- **External domain**: Look for domain/URL (e.g., `github.com`, `api.example.com`)
- **Tool**: Look for the full command string that was blocked

### Enable Bash Command or Tool Access

Add blocked commands/tools to `~/.claude/apple/tool_allowlist.csv`:

1. Read the current allowlist:
   ```
   Read ~/.claude/apple/tool_allowlist.csv
   ```

2. Determine match type:
   - `exact_match`: Use when the exact command string must match (e.g., specific npx commands with full paths)
   - `contains_match`: Use when any command containing this string should be allowed (e.g., `git`, `docker`, `ssh`)

3. Add new entry using Edit tool:
   - Format: `<command>,<match_type>,Added <ISO8601_timestamp> - <optional_comment>`
   - Example: `docker,contains_match,Added 2026-02-15 - Docker commands`
   - Example: `npx -y @user/package,exact_match,Added 2026-02-15T10:30:00.000Z - Specific package`

4. Verify the entry was added correctly by reading the file again

### Enable Domain Access

Add blocked domains to `~/.claude/apple/dangerous_allowed_domains.csv`:

1. Read the current allowlist:
   ```
   Read ~/.claude/apple/dangerous_allowed_domains.csv
   ```

2. Extract the domain from the blocked URL (e.g., `https://api.github.com/repos` → `api.github.com`)

3. Add new entry using Edit tool:
   - Format: `<domain> # Added <ISO8601_timestamp> - <optional_comment>`
   - Example: `api.github.com # Added 2026-02-15T10:30:00.000Z - GitHub API access`
   - Example: `pypi.org # Added 2026-02-15 - Python package repository`

4. Verify the entry was added correctly by reading the file again

### Retry the Blocked Operation

After adding entries to the allowlist:

1. Retry the exact same operation that was previously blocked
2. If still blocked, verify:
   - The entry was added correctly
   - The match type is appropriate (exact vs contains)
   - The domain/command string matches exactly what was in the error

3. If the error persists, check for typos or formatting issues in the CSV file

## Match Type Decision Guide

| Resource Type | Use Case | Match Type |
|---------------|----------|------------|
| Common commands | `git`, `ssh`, `docker`, `npm`, `python` | `contains_match` |
| Specific scripts | `./my-script.sh`, specific npx packages | `exact_match` |
| Commands with variables | `$CLAUDE_PROJECT_DIR/script.py` | `exact_match` |
| Hook scripts | Session start hooks, user prompt hooks | `exact_match` |
| General utilities | `mkdir`, `mv`, `rm`, `chmod`, `echo` | `contains_match` |

## Timestamp Format

Use ISO 8601 format for timestamps:
- Full: `2026-02-15T10:30:00.000Z` (preferred for exact_match entries)
- Date only: `2026-02-15` (acceptable for contains_match entries)

## Common Blocked Resources

**Development Tools:**
- `git`, `npm`, `npx`, `docker`, `uv`, `python`, `node`
- `ssh`, `scp`, `rsync` for remote operations
- `tmux`, `screen` for terminal multiplexing

**Domains:**
- Package registries: `pypi.org`, `npmjs.org`, `registry.npmjs.org`
- Documentation: `docs.python.org`, `nodejs.org`, `github.com`
- APIs: `api.github.com`, `api.anthropic.com`, `api.openai.com`
- CDNs: `cdn.jsdelivr.net`, `unpkg.com`, `raw.githubusercontent.com`

**MCP Servers:**
- Browser tools: `npx -y @agentdeskai/browser-tools-mcp`
- YouTube transcripts: `npx -y @kimtaeyoon83/mcp-server-youtube-transcript`
- Other npx-based MCP servers require exact command strings

## Security Considerations

Only add trusted resources to the allowlist:
- Verify domains belong to legitimate services
- Review command functionality before enabling
- Use `contains_match` sparingly for commands that could be exploited
- Add descriptive comments explaining why access was granted

## Troubleshooting

**Entry not working after adding:**
- Check CSV formatting (no quotes around values, correct comma placement)
- Verify timestamp format is valid
- Ensure no duplicate entries
- Confirm match type is appropriate

**Still blocked after multiple attempts:**
- Try switching from `contains_match` to `exact_match` or vice versa
- Check if there are multiple blockers (both command AND domain)
- Verify the exact string from the error message matches your entry

**File corruption:**
- Both CSV files should end with an empty line
- Each line should follow the exact format specified
- Use Edit tool rather than manual editing to prevent format issues
