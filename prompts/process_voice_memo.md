---
description: remove ums and add line breaks
argument-hint: [path]
---

I've provided a file with a recorded voice memo. The transcript needs to be cleaned.

## Arguments
PATH: $1
OUTPUT_PATH: docs/voice_memos/processed/{base_name}.txt

If PATH is not provided, use the most recently modified/created txt file under docs/voice_memos/raw

## Workflow

1. Remove any filler speech (ums, uhs, like, etc)
2. Insert paragraph breaks at appropriate locations
3. Resolve spelling issues (see below)

## Spelling Issues

There are two spelling issues to consider:

1. The voice transcription is notoriously terrible at spelling. Names of people, workplace jargon etc may be totally malformed. Use your knowledge base context to flag and correct any likely misspellings
2. I will often spell new names or terms out sequentially. In these cases, you should REPLACE the appropriate term with the correct spelling, and remove the guidance. For example:

<Original>
"I'm introducing sum name, spelled S-O-M-E N-A-M-E".
</Original>

<Corrected>
"I'm introducing Some Name.
</Corrected>

## Output Format

Processed file should be raw text with corrections applied

## Response to User

1. Path to output file
2. bulleted list containing [spelling error, replacement]
