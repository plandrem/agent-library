---
description: Iterate between executor and reviewer
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - LS
  - Bash
model: sonnet
argument-hint: [prompt]
---

## Goal

Use a pair of subagents to achieve a task with high quality

## Arguments

TASK: $ARGUMENTS

## Workflow

### Step 1. Define Worker Identities

What is the TASK domain? Who would be the ideal expert who could achieve this task with efficiency, quality, and excellence?

### Step 2. Invoke worker agent

Launch a subagent with an identity based on the questions above. Give that agent the TASK and wait for the agent's response

### Step 3. Invoke reviewer agent

Pass the reponse to a separate subagent, ALSO an expert in the same domain, with the additional prompting that the TASK was completed by a prior agent who is overeager and prone to rookie mistakes. The reviewer should be highly skeptical and validate that the TASK was truly completed.

Use this format for the prompt:

```
Identity: ...

Task: {exact TASK from user}
```

### Steps 4-N. Iterate

Have the initial agent address the reviewer feedback, and then prompt the reviewer to review the changes. Iterate until the reviewer is 100% satisfied.

## Examples

### Refactoring a Data Processing Function

**TASK:** Refactor the `process_transactions` function to improve readability and add proper error handling

**Step 1. Define Worker Identities**

Domain: Python backend development, code refactoring
Worker Identity: Staff Python Engineer with 12+ years of experience in backend systems. Has led multiple refactoring initiatives across large codebases. Deep expertise in clean code patterns, SOLID principles, and Python idioms. Known for pragmatic solutions that balance readability with performance.

Reviewer Identity: Principal Python Engineer with 8+ years of experience. Specializes in production incident response and has developed a keen eye for subtle bugs introduced during refactoring. Approaches code review with healthy skepticism, particularly around error handling edge cases and behavioral regressions. Brings a different perspective focused on "what could go wrong."

**Step 2. Invoke Worker Agent**

Prompt to Worker:
```
Identity: You are a Staff Python Engineer with 12+ years of experience leading refactoring initiatives across large codebases. You have deep expertise in clean code patterns, SOLID principles, and Python idioms. 

TASK: Refactor the `process_transactions` function to improve readability and add proper error handling
```

Worker Response:
```
- Extracted validation logic into `validate_transaction()`
- Created `TransactionProcessor` class with single responsibility
- Added try/except blocks around database operations
- Used early returns to reduce nesting
```

**Step 3. Invoke Reviewer Agent**

Prompt to Reviewer:
```
Identity: You are a Principal Python Engineer who specializes in production incident response. You have a keen eye for subtle bugs introduced during refactoring. 

Instructions: A junior engineer has recently completed a task. This individual is highly overeager and prone to rookie mistakes. Review the task with healthy skepticism. Being your response with either "ACCEPTED" or "REJECTED".

TASK: Refactor the `process_transactions` function to improve readability and add proper error handling
```

Reviewer Response:
```
REJECTED

- ISSUE: The new `validate_transaction()` silently returns None on invalid input instead of raising an exception
- ISSUE: Database connection errors are caught but not logged
- ISSUE: Original function handled batch processing; new version processes one at a time
- PASS: Class structure follows SRP correctly
```

**Step 4. Worker Addresses Feedback**

```
Worker fixes:
- Changed `validate_transaction()` to raise `ValidationError`
- Added logging to exception handlers
- Restored batch processing capability with `process_batch()` method
```

**Step 5. Reviewer Re-reviews**

```
ACCEPTED

Reviewer Response:
- PASS: Validation now properly raises exceptions
- PASS: Logging implemented correctly
- PASS: Batch processing restored
```

## Response

```
Summary:
{Summary of work completed}

Feedback Required:
{bulleted list of mistakes made by worker agent}

(# of iterations: N)

```