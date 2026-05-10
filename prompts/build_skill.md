---
description: Create new Claude Code skills
argument-hint: [description]
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
model: sonnet
---

# Build Skill

Create a new Claude Code skill at user or project scope.

## Arguments
DESCRIPTION: $ARGUMENTS

## Key Concepts

**Skills vs Commands:**
- Commands (.claude/commands/): User-invoked via /name, single markdown file
- Skills (.claude/skills/): Model-invoked when Claude determines relevance, directory with SKILL.md + resources

**Skills Directory Structure:**
```
skill-name/
├── SKILL.md                    (required, 1,500-2,000 words)
├── references/                 (optional, detailed docs)
│   └── detailed-guide.md
├── examples/                   (optional, working code)
│   └── example.sh
└── scripts/                    (optional, utilities)
    └── validate.sh
```

**SKILL.md Format:**
```yaml
---
name: skill-name  # Must match the skill directory name (kebab-case)
description: This skill should be used when... {provide 1-2 sentences of relevant context here}. Key trigger phrases include "trigger phrase 1", "trigger phrase 2".
---
```

**Writing Style:**
- Imperative/infinitive form (verb-first)
- NOT second person ("You should...")
- Strong trigger phrases in description

## Workflow

### 1. Gather Details
Use AskUserQuestion to ask:
- Skill name (kebab-case, e.g., "code-review")
- Scope: user (~/.claude/skills/) or project (./.claude/skills/)

### 2. Research Existing Patterns
Search for similar skills in:
- ~/.claude/skills/
- ~/.claude/plugins/marketplaces/*/plugins/*/skills/
- Current project .claude/skills/

Reference: ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/skill-development/SKILL.md

### 3. Design the Skill
Create skill spec with:
- Strong trigger description with specific phrases
- Progressive disclosure plan (what goes in SKILL.md vs references/)
- List of bundled resources needed

### 4. Create Skill Directory
IF SCOPE == "user":
  Create: ~/.claude/skills/NAME/
ELIF SCOPE == "project":
  Create: ./.claude/skills/NAME/

### 5. Write SKILL.md
```markdown
---
name: {skill-directory-name}  # Must match the directory name (kebab-case)
description: This skill should be used when the user asks to "{trigger 1}", "{trigger 2}", "{trigger 3}".
version: 0.1.0
---

# {Title}

## Overview
{What this skill accomplishes - 1-2 paragraphs}

## Core Procedures

### {Procedure 1}
{Step-by-step instructions in imperative form}

### {Procedure 2}
{More procedures as needed}

## Quick Reference
{Tables, checklists, common patterns}

## Bundled Resources
- `references/` - {description of detailed docs}
- `examples/` - {description of example files}
- `scripts/` - {description of utilities}
```

### 6. Add Bundled Resources (if needed)
Create subdirectories and files:
- references/*.md for detailed documentation
- examples/* for working code samples
- scripts/* for validation/utility scripts

### 7. Verify Creation
- Read SKILL.md to confirm structure
- List directory contents
- Report full path to user

## Response
"Skill created."