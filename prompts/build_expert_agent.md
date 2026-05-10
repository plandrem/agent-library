---
name: build_expert_agent
description: Create expert agent with auto-generated index
argument-hint: [resource-path-or-url]
disable-model-invocation: false
---

# Build Expert Agent

Create a new expert agent that indexes documentation and source code for fast future queries.

## Arguments

- `$ARGUMENTS` (resource-path-or-url): Path to local directory or URL to documentation/repository

## Workflow

### 1. Ask User for Configuration

Use AskUserQuestion to gather:

1. **Agent name** (header: "Agent name", question: "What should the agent be named? Use lowercase with hyphens (e.g., 'mem0-expert').")
   - Option 1: Auto-generate from resource name (Recommended)
   - Option 2: Custom name (I'll specify)

2. **Color** (header: "Color", question: "What color should represent this agent in the UI?")
   - Option 1: blue - For general purpose or data-related agents
   - Option 2: green - For API/service-related agents
   - Option 3: purple - For database or storage agents
   - Option 4: yellow - For framework or tool agents
   - Option 5: red - For security or critical system agents

3. **Scope** (header: "Scope", question: "Where should this agent be available?")
   - Option 1: User (~/.claude/agents/) - Available across all projects (Recommended)
   - Option 2: Project (.claude/agents/) - Only this project

### 2. Fetch Documentation (if URL)

IF resource is a URL:
- Use `/find` to fetch documentation focusing on:
  - Quickstart guides and setup instructions
  - API reference and how-to guides
  - Architecture and implementation details
- Save to `docs/$1/` directory
- Clone any associated GitHub repositories

ELIF resource is a local path:
- Verify path exists
- Use this as the documentation/codebase location

### 3. Determine Agent Name

IF user selected "Auto-generate from resource name":
- Extract name from resource path/URL (e.g., "mem0" from "https://github.com/mem0ai/mem0")
- Append "-expert" suffix
- Convert to lowercase with hyphens

ELSE:
- Use custom name provided by user

### 4. Create Agent File

Create agent at appropriate location based on scope:
- User scope: `~/.claude/agents/[agent-name].md`
- Project scope: `.claude/agents/[agent-name].md`

Use this structure:

```markdown
---
name: $1
description: PROACTIVELY use this agent to find any reference material about [TOPIC], including examples and where to look in source code. In your prompt, you must provide context - WHY are you asking this question?
model: sonnet
color: $2
---

## Workflow

1. Consider the task:

IF task category relates to system design, architecture, or API usage, THEN focus on DOCUMENTATION

ELIF task category relates to internal behavior or implementation details, THEN focus on CODEBASE

2. Read ALL relevant content within DOCUMENTATION/CODEBASE
3. Craft your response based on what you have read

## Reference Material

DOCUMENTATION: [path to research summary or docs]
CODEBASE: [path to cloned repo or source code]

Key areas to explore:
- [List 5-7 key topics specific to this domain]

## Index

[Will be generated in next step]

## Response Format

\`\`\`json
{
    'summary': ..., // a succinct paragraph addressing the query
    'references': [
        {
            'file': path/to/file.md,
            'starting_line': 42,
            'content': ... // the specific statements that satisfy the query
        },
        ...
    ]
}
\`\`\`
```

### 5. Generate Index

Launch a haiku agent to explore the documentation and generate a comprehensive index:

```
Use a haiku agent to:

1. Read the research summary at [path]
2. Explore the codebase structure at [path]
3. Identify key files, modules, and topics
4. Generate a hierarchical index with:
   - File paths and brief descriptions
   - Line number ranges for code sections
   - Topic organization
   - API endpoints, configuration options, etc.

Update the agent file at ~/.claude/agents/$1.md by inserting the index into the "## Index" section (between "## Reference Material" and "## Response Format").

The index should be in markdown format with nested lists, making it easy to quickly locate relevant content for future queries.
```

### 6. Confirm Creation

Report to user:
- Agent created at: `~/.claude/agents/$1.md`
- Documentation location: [path]
- Codebase location: [path if applicable]
- Index generated: Yes/No
- Agent can be invoked by other agents using the Task tool

## Example Usage

```
/build_expert_agent https://github.com/mem0ai/mem0
```

This will:
1. Ask for agent name, color, and scope
2. Fetch mem0.ai documentation and clone the repo
3. Create agent file (e.g., `~/.claude/agents/mem0-expert.md`)
4. Generate a comprehensive index using haiku
5. Make the agent available for queries about the domain

```
/build_expert_agent ~/projects/my-framework/docs
```

For local documentation, provide the path and configure interactively.
