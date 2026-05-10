---
description: Initialize a basic, single text file memory system
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - LS
  - Bash
model: haiku
---

## Goal

Create a basic, single file memory system

## Workflow

### Step 1a. Create Project Memory File

If `$CLAUDE_PROJECT_DIR/.memories.md` does not exist, create it:
```
# Memories

This file contains a record of important learning, feedback and experiences from work that you have done in the past.
```

Include subheadings for
- User Preferences
- Best Practices
- Workflows
- Gotchas
- Resource Locations

If the file already exists, do not modify it.

### Step 1b. Create Global Memory File

If `~/.claude/.memories.md` does not exist, create it with the same structure as above.

If the file already exists, do not modify it.

### Step 2. Update System Context

Ensure `$CLAUDE_PROJECT_DIR/CLAUDE.md` exists. If it does not exist, create it.

Add both imports at the top of the file if not already present:
```
@import ~/.claude/.memories.md
@import .memories.md
```

Do not duplicate imports if they already exist.

### Step 3. Install Proactive Reflect Skill

If `$CLAUDE_PROJECT_DIR/.claude/skills/ai-basic-memory-proactive-reflect/SKILL.md` already exists, skip this step.

Create `SKILL.md`:
```markdown
---
name: Proactive Memory Reflection
description: This skill should be used proactively to update the agent's memory file. Trigger for any failed tool calls, when user says "should have", "you didn't", "Always", "Don't", "I want", "Why did you", or when completing tasks, receiving feedback, discovering gotchas, or finding new resources.
---

# Proactive Memory Reflection

## Overview

Invoke `/ai:basic-memory:reflect` at natural checkpoints during work to capture learnings, preferences, and patterns worth remembering.

## When to Reflect

Trigger reflection after:
- Completing a significant task or milestone
- Receiving explicit user feedback or corrections
- Discovering a gotcha or unexpected behavior
- Learning a new workflow or pattern
- Encountering a resource location worth remembering

## Procedure

1. Recognize a reflection trigger has occurred
2. Invoke `/ai:basic-memory:reflect`
3. Continue with the current task

## Quick Reference

| Trigger | Example |
|---------|---------|
| Task completion | "Finished implementing auth" |
| User feedback | "Actually, always use X instead of Y" |
| Gotcha discovered | "This API silently fails on Z" |
| Pattern learned | "This codebase uses convention A" |
```

## Validation

- [] Project memory file exists at `$CLAUDE_PROJECT_DIR/.memories.md`
- [] Global memory file exists at `~/.claude/.memories.md`
- [] CLAUDE.md exists
- [] Both import statements are present
- [] Skill installed at project level

## Response

"Memory initialized."
