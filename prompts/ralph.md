---
description: Execute PRD using Ralph Wiggum loop with ralph.sh
---

# Ralph - Autonomous PRD Execution Loop

This command launches the `ralph.sh` script to autonomously execute a PRD using the Ralph Wiggum technique. The script wraps `/execute_prd` in a loop, providing fresh context for each Feature Requirement while respecting dependencies, budget limits, and watchdog timeouts.

## Instructions
1. Collect ALL argument values via AskUserQuestion tool
2. Execute the script in the background
3. Wait for further instructions

## Usage Examples

```bash
# Basic usage (serial mode, $100 budget, 30min watchdog)
ai/scripts/ralph.sh --prd <prd_path> --branch <branch_name>

# Parallel mode with custom budget
ai/scripts/ralph.sh --prd specs/prd.md --branch feature-x --mode parallel --budget 50

# Custom watchdog and retry settings
ai/scripts/ralph.sh --prd specs/prd.md --branch feature-x --watchdog 45 --max-retries 5
```

## Arguments

### Required
- `--prd <path>` - Path to PRD file (must contain DEPENDENCY_LAYERS comment block)
- `--branch <name>` - Git branch name for implementation

### Optional
- `--mode <serial|parallel>` - Execution mode (default: serial)
  - **serial**: Processes FRs sequentially with retry support
  - **parallel**: Processes FRs in each layer concurrently (no retries, fails fast)
- `--budget <dollars>` - Additional dollars to spend from current level (default: 100)
  - Budget is RELATIVE to current spend
  - Example: If you've spent $7 and set --budget 10, script stops at $17 total
- `--watchdog <minutes>` - Kill stalled processes after N minutes (default: 30)
- `--max-retries <count>` - Max gatekeeper retries per FR (default: 3, serial mode only)

## PRD Requirements

Your PRD MUST include a DEPENDENCY_LAYERS comment block:

```markdown
<!-- DEPENDENCY_LAYERS
layer1: FR1,FR2,FR7
layer2: FR3,FR4
layer3: FR5,FR8
layer4: FR6a,FR6b,FR6c,FR6d
layer5: FR9,FR10
-->
```

**Rules:**
- FRs in the same layer have no dependencies on each other
- Layer N+1 depends on all FRs in Layer N completing successfully
- Serial mode processes layers sequentially, FRs within a layer sequentially
- Parallel mode processes layers sequentially, FRs within a layer concurrently

## How It Works

### Serial Mode (Recommended)
```
For each layer:
  For each FR in layer:
    retry_count = 0
    while retry_count <= max_retries:
      1. Check budget (stop if exceeded)
      2. Launch: ayo -p "/execute_prd <prd> <branch> <fr>"
         - Orchestrator implements criteria
         - Gatekeeper verifies and updates PRD
         - Evolution learns from failures
      3. Parse result (APPROVED/REJECTED/PARSE_ERROR)
      4. If APPROVED: move to next FR
      5. If REJECTED: retry with fresh context (up to max_retries)
      6. If max_retries exceeded: terminate with error
    end while
  end for
end for
```

### Parallel Mode
```
For each layer:
  Spawn all FRs in layer concurrently
  Wait for all to complete (barrier)
  If any FR fails: terminate immediately
  Move to next layer
```

## Logging & Telemetry

### Real-time Monitoring
```bash
# Tail the main log for real-time progress
tail -f ai_docs/ralph_logs/*/ralph.log

# Output example:
[2026-01-22 14:05:32] START ralph.sh specs/prd.md feature-branch serial 100 30 3
[2026-01-22 14:05:32] Parsed 5 layers, 10 FRs
[2026-01-22 14:05:32] Budget: $0.00 / $100.00
[2026-01-22 14:05:33] === Layer 1 ===
[2026-01-22 14:05:33] [001] FR1 starting...
[2026-01-22 14:12:45] [001] FR1 completed (432s, $2.34, APPROVED)
[2026-01-22 14:12:45] Budget: $2.34 / $100.00
```

### Log Directory Structure
```
ai_docs/ralph_logs/2026-01-22_140532/
├── ralph.log                              # Main log (tail -f this)
├── summary.json                           # Final summary with all metrics
├── iterations/
│   ├── 001_FR1_20260122_140533.log       # Full ayo output
│   ├── 001_FR1_20260122_140533.json      # Iteration telemetry
│   ├── 002_FR2_20260122_141245.log
│   └── 002_FR2_20260122_141245.json
└── errors/
    ├── watchdog_killed_FR3_xxx.log       # Watchdog timeout logs
    └── error_FR4_exit1_xxx.log           # Non-zero exit logs
```

### Summary JSON
```json
{
  "run_id": "2026-01-22_140532",
  "prd_path": "specs/prd.md",
  "git_branch": "feature-branch",
  "mode": "serial",
  "started_at": "2026-01-22T14:05:32Z",
  "ended_at": "2026-01-22T18:45:00Z",
  "total_duration_seconds": 16768,
  "total_iterations": 15,
  "total_retries": 8,
  "budget_limit": 100,
  "budget_start": 7.00,
  "budget_end": 94.23,
  "total_spent": 87.23,
  "termination_reason": "complete",
  "criteria_summary": {
    "total": 47,
    "approved": 42,
    "failed": 5
  },
  "watchdog_kills": 2,
  "parse_errors": 1
}
```

## Termination Reasons

- `complete` - All FRs processed successfully
- `budget_exceeded` - Budget limit reached mid-execution
- `max_retries_exceeded` - FR failed after max retries
- `interrupted` - User pressed Ctrl+C
- `no_criteria` - PRD has no unchecked criteria

## Error Handling

### Watchdog Timeout
If a process stalls (no progress for N minutes):
1. Process killed with SIGKILL (exit code 137)
2. Log copied to `errors/watchdog_killed_*`
3. Fresh retry launched (serial mode) or script terminates (parallel mode)

### Parse Errors
If `/execute_prd` doesn't output the expected result block:
1. Logged as PARSE_ERROR
2. Counted against max_retries
3. Fresh retry launched with clean context

### Budget Exhaustion
When budget limit reached:
1. Current iteration completes
2. Partial progress saved to summary.json
3. Script exits with termination_reason: "budget_exceeded"

### Graceful Shutdown
Press Ctrl+C to interrupt:
1. Current iteration completes
2. Partial summary.json saved
3. Log shows "Interrupted, saving state"

## Examples

### Example 1: Basic Serial Execution
```bash
ai/scripts/ralph.sh --prd specs/finance-prd.md --branch feature/finance-v2
```

**Use case:** Default settings, process all FRs sequentially with retries

### Example 2: Parallel with Low Budget
```bash
ai/scripts/ralph.sh \
  --prd specs/prd.md \
  --branch feature/parallel-test \
  --mode parallel \
  --budget 20
```

**Use case:** Fast execution for independent FRs, limited budget

### Example 3: Aggressive Retries
```bash
ai/scripts/ralph.sh \
  --prd specs/prd.md \
  --branch feature/complex \
  --max-retries 10 \
  --watchdog 60 \
  --budget 200
```

**Use case:** Complex FRs that may need many retries, long timeout, high budget

### Example 4: Testing with $1 Budget
```bash
ai/scripts/ralph.sh \
  --prd specs/test-prd.md \
  --branch test/budget-check \
  --budget 1
```

**Use case:** Test budget enforcement without spending much

## Integration with /execute_prd

Ralph.sh invokes `/execute_prd` with three arguments:

```bash
ayo -p "/execute_prd <prd_path> <branch> <fr_id>"
```

**execute_prd responsibilities:**
1. Filter criteria to only those from the specified FR
2. Run criterion-orchestrator → gatekeeper → evolution for each criterion
3. Output structured result block:
```
=== EXECUTE_PRD RESULT ===
FEATURE: FR1
CRITERIA_TOTAL: 5
CRITERIA_APPROVED: 5
CRITERIA_REJECTED: 0
GATEKEEPER_RESULT: APPROVED
ERRORS: none
```

Ralph.sh parses this block to determine retry/continue logic.

## Troubleshooting

### "Missing DEPENDENCY_LAYERS in PRD"
**Problem:** PRD doesn't have the required comment block
**Solution:** Add DEPENDENCY_LAYERS comment to your PRD (see PRD Requirements above)

### "Budget limit reached"
**Problem:** Script stopped before completing all FRs
**Solution:** Check summary.json for progress, increase --budget, or continue from checkpoint

### "Script exits immediately with max_retries_exceeded"
**Problem:** First FR failed all retries
**Solution:** Check errors/ logs, fix the issue, re-run with higher --max-retries

### Watchdog keeps killing processes
**Problem:** FRs are legitimately taking >30 minutes
**Solution:** Increase --watchdog timeout (e.g., --watchdog 60)

### "bc command not found" or "jq command not found"
**Problem:** Missing dependencies
**Solution:** Install bc and jq:
```bash
# macOS
brew install bc jq

# Ubuntu/Debian
sudo apt-get install bc jq
```

## Dependencies

- **bash** - Shell (macOS/Linux compatible)
- **bc** - Arbitrary precision calculator (for budget math)
- **jq** - JSON processor (for reading Claude stats)
- **timeout** - Process timeout utility (GNU coreutils)
- **ayo** - Claude CLI wrapper (aliased to `claude` or `apple-claude-code`)

