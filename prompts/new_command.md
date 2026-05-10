---
description: add a new custom slash command
argument-hint: [name] [scope] [description]
---

Create a new, custom slash command using a specified format

## Arguments
NAME: $1
SCOPE: $2
DESCRIPTION: $ARGUMENTS
CACHE_LOCATION: ai_docs/slash_commands.xml

## Workflow
### **1. Refresh Documentation**

Check the date modified metadata for CACHE_LOCATION:

IF the file does not exist OR the file was not updated today,
THEN 
    1. Use the claude code docs agent to fetch the latest documentation on custom slash commands from Anthropic
    2. Create/Update the file at CACHE_LOCATION (include a "refresh date" field to be updated even if the other contents are the same, to indicate a fetch was performed)

### **2. Read Documentation**
READ CACHE_LOCATION

### **4. Create Command File**
IF scope == 'user', THEN command should be placed in ~/.claude/commands/{NAME}.md
ELIF scope == 'project', THEN command should be placed in project_root/.claude/commands/{NAME}.md

## Output Format
Use this structure EXACTLY:

```markdown
---
description: {command intent, <= 10 words}
argument-hint: [arg1] [arg2] ...
---
## Workflow
### **1. Refresh Documentation**

Check the date modified metadata for CACHE_LOCATION:

IF the file does not exist OR the file was not updated today,
THEN 
    1. Use the claude code docs agent to fetch the latest documentation on custom slash commands from Anthropic
    2. Create/Update the file at CACHE_LOCATION (include a "refresh date" field to be updated even if the other contents are the same, to indicate a fetch was performed)

### **2. Read Documentation**
READ CACHE_LOCATION

### **4. Create Command File**
IF scope == 'user', THEN command should be placed in ~/.claude/commands/{NAME}.md
ELIF scope == 'project', THEN command should be placed in project_root/.claude/commands/{NAME}.md

## Output Format
Use this structure EXACTLY:


```

## Response to User