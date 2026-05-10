---
description: create a new custom agent
argument-hint: [description]
---

Create a new custom agent definition file through guided, interactive brainstorming

## Arguments
DESCRIPTION: $ARGUMENTS
CACHE_LOCATION: ai_docs/agents.xml

## Workflow

### **1. Refresh Documentation**

Check the date modified metadata for CACHE_LOCATION:

IF the file does not exist OR the file was not updated today,
THEN
    1. Use the claude code docs agent to fetch the latest documentation on custom agents from Anthropic
    2. Create/Update the file at CACHE_LOCATION (include a "refresh date" field to be updated even if the other contents are the same, to indicate a fetch was performed)

### **2. Read Documentation**
READ CACHE_LOCATION

### **3. Read Template**
READ ~/.claude/templates/new_agent.md as the template for agent file structure

### **4. Interactive Brainstorming**

Guide the user through agent design ONE QUESTION AT A TIME using AskUserQuestion. Do not bundle questions — ask each separately and wait for the answer before proceeding.

**Round 1 — Scope**
Ask: "Where should this agent live?"
Options:
- "User (~/.claude/agents/)" — available in all projects
- "Project (.claude/agents/)" — scoped to current project

**Round 2 — Purpose Refinement**
Based on DESCRIPTION, propose 2-3 interpretations of what the agent should do. Lead with your recommended interpretation and explain why. Ask which one the user wants. Use multiple choice.

**Round 3 — Workflow Design**
Propose 2-3 workflow structures for the agent (e.g. conditional branching like memos_expert, sequential steps, iterative loop). Lead with your recommendation. Ask which the user prefers. Use multiple choice.

**Round 4 — Reference Material**
Ask: "What reference material should this agent consult?"
Options should be contextual — propose likely paths based on the project structure and agent purpose. Include an open-ended option.

**Round 5 — Response Format**
Ask: "How should the agent format its responses?"
Options:
- "JSON (structured, like memos_expert)" — summary + references
- "Markdown (prose)" — natural language with headers
- "Code" — output code blocks
Tailor options to the agent's purpose.

**Round 6 — Model**
Ask: "Which model should power this agent?"
Options:
- "haiku (Recommended)" — fast, cheap, good for lookup/retrieval tasks
- "sonnet" — balanced, good for reasoning and synthesis
- "opus" — most capable, for complex analysis or generation

**Round 7 — Name & Color**
Propose a kebab-case name derived from the finalized purpose. Ask the user to confirm or suggest an alternative.
Ask: "Pick a color for the agent status indicator."
Options: yellow, blue, green, red, cyan, magenta

### **5. Create Agent File**

Using all answers from step 4, populate the template from step 3 and write the file:

IF scope == 'user', THEN place in ~/.claude/agents/{NAME}.md
ELIF scope == 'project', THEN place in project_root/.claude/agents/{NAME}.md

## Response to User
Confirm the agent was created and where it was placed.
