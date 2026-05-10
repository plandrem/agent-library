---
description: Dex — coaching/chief-of-staff persona with the weekly ritual layer and voice memo tooling
---

# Dex

Dex is your professional and life coach, chief of staff, and operational thought-partner. This bundle installs the ritual layer that keeps Dex grounded in your week.

## Rituals

- `/daily-standup` — morning orientation, inbox triage, commit to today's one thing
- `/weekly-plan` — Monday outlook and weekly commitment
- `/weekly-review` — Friday retrospective

## Voice capture

- `/ingest_voice_memo [path]` — read a voice memo transcript
- `/process_voice_memo [path]` — clean up a transcript (remove ums, add line breaks)

## Continuity

The `claude-mem-expert` agent is included for cross-session memory lookups — reach for it when Dex needs context on what happened in prior conversations.

## Usage

Invoke the specific ritual you need. Dex assumes persistent memory at `~/.claude/projects/-Users-patrick-ai-dex/memory/`.
