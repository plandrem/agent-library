---
description: Basic memory — single text file persistence across sessions
---

# Basic Memory

A minimal memory system — one flat text file tracking learnings across sessions. Use when you want lightweight continuity without a full memory framework.

## Included

- `/basic-memory-init` — initialize a new memory file for a project
- `/basic-memory-reflect` — capture session learnings into the memory file

## Usage

- Run `/basic-memory-init` once at the start of a project to set up the memory file.
- Run `/basic-memory-reflect` at the end of meaningful sessions to capture what was learned.
- The memory file is loaded on subsequent sessions so context persists.

For richer memory systems, consider `claude-mem` or `memOS` (see their respective expert agents).
