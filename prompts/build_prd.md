---
description: Create a prd file based on a plan
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Glob
  - Grep
  - LS
  - Bash
model: opus
argument-hint: [plan]
disable-model-invocation: false
---

## Goal

Create a detailed, actionable Product Requirements Document (PRD) with user stories and acceptance critera to organize the execution of a project

## Arguments

PLAN: $ARGUMENTS

## Workflow

Use the /execute_and_review skill, passing PLAN to the agents and having them iterate on the document

## Validation

- [] All document sections are present in the correct order
- [] All goals are covered by at least one feature requirement
- [] User stories use the correct format
- [] Elements use correct indexing formats
- [] Each phase of the implementation plan results in a self-contained, verifiable output (e.g. script that can be run with interpretable output)

## Resources

### Elements of a good PRD

- Document History (updates since prior version + decisions made etc, or "Initial Version")
- Goals
- Non-goals
- Assumptions
- Feature Requirements (mapped to Goals)
  - User stories (as a [role], I need [function] to [benefit])
  - Acceptance Critera (checklist, for each user story)
- Dependency graph for user stories
- Implementation plan (validate assumptions > MVP > add complexity)

### Indexing Format

- Goals: G1, G2...
- Non-Goals: NG1, NG2...
- Feature Reqs: FR1, FR2...
- User Stories: US1, US2...
- Acceptance Criteria: AC1, AC2...

## Output Format

Save document to {project root}/ai_docs/spec/{descriptive name}_prd_v{incrementing version number}.md

## Response

"PRD is ready at {path to file}."
