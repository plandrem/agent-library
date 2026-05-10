---
description: Execute acceptance criteria from PRD using TDD workflow with subprocess isolation
argument-hint: prd_path git_branch
---

## Variables

PRD_PATH = $1
GIT_BRANCH = $2

## Overview

This command implements acceptance criteria from a PRD v2 document using a multi-agent TDD workflow. Each acceptance criterion is implemented in an isolated subprocess to ensure:
- Fresh agent prompt files are loaded (evolution changes take effect)
- Complete team isolation between acceptance criteria
- Evolution agent can modify agent prompts between criteria

## Architecture

```
/execute_prd (this session)
    │
    ├── [subprocess 1] CRITERION_ORCHESTRATOR for AC1
    │   └── Writes: orchestrator_report + transcript saved
    │
    ├── [subprocess 2] EVOLUTION_AGENT
    │   └── Reads transcript, updates issues.json, evolves agents
    │
    ├── [subprocess 3] CRITERION_ORCHESTRATOR for AC2 (fresh prompts!)
    │   └── ...
    │
    └── ... continues for each AC
```

## Workflow

### Initialize

1. Read PRD_PATH to understand feature requirements
2. Parse PRD to find unchecked acceptance criteria:
   - Look for lines matching `- [ ]` within "Acceptance Criteria" sections
   - Group by Feature Requirement (FR1, FR2, etc.)
3. Create git branch if needed:
   ```bash
   git checkout -b GIT_BRANCH
   ```
4. Ensure directories exist:
   ```bash
   mkdir -p ai_docs/orchestrator_reports
   mkdir -p ai_docs/evolution
   ```
5. Initialize knowledge base if not exists:
   ```bash
   if [ ! -f ai_docs/evolution/issues.json ]; then
     echo '{"issues": [], "last_updated": ""}' > ai_docs/evolution/issues.json
   fi
   ```

### Execute Loop

For each unchecked acceptance criterion:

**Step 1: Invoke Orchestrator (subprocess)**

```bash
RESULT=$(claude --print << EOF
You are the criterion-orchestrator agent.

(Installed as `prd-criterion-orchestrator` — team members are prefixed `prd-*`. See agent file for subagent_type mapping.)

Implement the following acceptance criterion:
CRITERION: {criterion_text}

FR Context:
{full FR description including examples}

PRD Path: ${PRD_PATH}
EOF
)
```

Capture from RESULT:
- `session_id`: For transcript access
- `report_path`: For evolution agent

**Step 2: Invoke Evolution Agent (subprocess)**

```bash
claude --print << EOF
You are the evolution-agent.

Analyze the orchestrator run and evolve agents if patterns detected.

Report: ${REPORT_PATH}
Transcript: ~/.claude/projects/.../subagents/agent-${SESSION_ID}.jsonl
EOF
```

**Step 3: Continue Loop**

- Re-read PRD to check current state
- Find next unchecked criterion
- If more criteria remain, return to Step 1
- If all criteria in current FR are complete, move to next FR
- If all FRs complete, proceed to Completion

### Completion

1. Update "Feature Status" table in PRD's Changes & Learnings section
2. Inform user that all criteria are implemented
3. Push to remote if requested

## PRD Parsing

The PRD v2 format has acceptance criteria as checkboxes:

```markdown
### FR1: Transaction Import

**Acceptance Criteria**:
- [x] `finance import` imports from both SimpleFIN and manual CSV sources
- [ ] `--refresh` forces SimpleFIN cache invalidation
```

Parse logic:
- Find sections starting with `### FR`
- Find "**Acceptance Criteria**:" subsections
- Extract lines matching `- [ ]` (unchecked) or `- [x]` (checked)
- Track which are incomplete

## Why Subprocess Invocation

**Critical**: Agent prompt files are loaded at session start. If the evolution agent modifies `.claude/agents/prd-test-architect.md`, that change is NOT picked up by agents already running in this session.

By invoking each orchestrator as a subprocess:
- New session starts fresh
- All agent files re-read from disk
- Evolution changes take immediate effect

## Communication

Be succinct. Example:
```
Reading PRD... Found FR10 (Audit Logging) with 11 unchecked criteria

=== Criterion 1: "finance audit log lists recent commands" ===
Launching CRITERION_ORCHESTRATOR subprocess...
[subprocess completes]
Report saved: ai_docs/orchestrator_reports/fr10_audit_log_20260119.md

Launching EVOLUTION_AGENT subprocess...
[subprocess completes]
Knowledge base updated

=== Criterion 2: "finance audit show displays command details" ===
...
```

## Rules

1. **Subprocess isolation** - MUST use separate subprocess for each orchestrator
2. **Evolution between criteria** - ALWAYS run evolution agent before next orchestrator
3. **No direct implementation** - All work delegated to orchestrators
4. **Track progress** - Update PRD checkboxes via orchestrator
5. **Capture session IDs** - Needed for evolution agent transcript access

## Error Handling

If a subprocess fails:
1. Capture error output
2. Report to user
3. Ask whether to retry, skip, or abort
4. Do NOT proceed automatically after failure
