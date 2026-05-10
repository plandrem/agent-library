---
description: Browser automation — playwright-cli skill plus the companion agent for delegated browser work
---

# Playwright

Headless browser automation for Claude Code.

## Included

- `playwright-cli` skill — token-efficient CLI with parallel named sessions, screenshots, and scraping. Does not load tool schemas into context.
- `playwright-cli-agent` agent — delegate long-running or parallel browser work without polluting the main context

## Usage

- Use the **skill** directly for one-off scripted flows where you want to see what the browser is doing inline.
- Use the **agent** for parallel sessions, multi-step flows, or when the browser work shouldn't interrupt the main conversation.
