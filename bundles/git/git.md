---
description: Git hygiene — disciplined commits and worktree management for isolated feature work
---

# Git

Small toolkit for disciplined git workflow.

## Included

- `/commit` — git commit with disciplined message style (no AI attribution, avoid staging sensitive files)
- `/worktree` — create a git worktree for isolated feature work

## Usage

- `/worktree` — invoke before starting feature work that should stay isolated from the main checkout
- `/commit` — invoke when changes are ready to land; follows repo commit-message conventions

This bundle will grow as more git-related primitives are added (PR creation, rebase helpers, etc.).
