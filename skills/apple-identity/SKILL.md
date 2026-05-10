---
name: apple-identity
description: Use this skill when any Apple internal service requires a DSID, AppleConnect credentials, or Westgate JWT. Trigger phrases include "what is my DSID", "find my DSID", "CA Trino username", "AppleConnect DSID", "Westgate token", "CA JWT", "core analytics credentials", or any time a numeric Apple user ID is needed for authentication.
version: 0.1.0
---

# Apple Identity

Provides Apple internal identity information (DSID, AppleConnect username, Westgate tokens) needed for authenticating with internal services.

## Known Identity

| Field | Value |
|---|---|
| **DSID** | `2701107795` |
| **AppleConnect username** | `patrick_e_laporte` |
| **Email** | `patrick_e_laporte@apple.com` |
| **Name** | Patrick Laporte |

Use the DSID as the **username** when authenticating with CA Trino (`ca-trino-proxy.g.apple.com`).

## Re-derive DSID (if rotated or uncertain)

Run the bundled script — it decodes the Westgate JWT to extract current identity claims:

```bash
python3 ~/.claude/skills/apple-identity/scripts/get_dsid.py
```

This works as long as there is an active AppleConnect session (`wgtool` must be authenticated).

## Minting a CA JWT

CA Trino requires a separate long-lived JWT scoped to specific CA views:

```bash
# 1. Get a short-lived Westgate token (~10 hours)
WG=$(wgtool token coreanalytics-api.corp.apple.com)

# 2. Mint a 6-month CA JWT for a specific view
curl -sX POST https://coreanalytics-api.corp.apple.com/api/v1/tokens \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WG" \
  -d '{"views": "EnergyTelemetrySummary_v2"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])'

# List existing (still-valid) tokens
curl -s -H "Authorization: Bearer $WG" \
  https://coreanalytics-api.corp.apple.com/api/v1/tokens \
  | python3 -m json.tool
```

CA JWTs are valid 6 months. Request access per-view; a single JWT can cover multiple views if listed comma-separated in `"views"`.

## Service Credentials Quick Reference

| Service | Username | Password / Token |
|---|---|---|
| CA Trino (`ca-trino-proxy.g.apple.com`) | DSID (`2701107795`) | CA JWT (view-scoped, 6-month) |
| UPAX Trino (`upax-trino.swe.apple.com`) | AppleConnect username | OD password (prompted by Tableau) |
| Westgate-protected APIs | N/A (use `wgtool token <audience>`) | N/A |

## Notes

- The DSID is a numeric identifier and does NOT match the AppleConnect username (`patrick_e_laporte`).
- `wgtool token <audience>` mints a short-lived (~10h) Westgate token. The `<audience>` is the hostname of the API you need to call, e.g., `coreanalytics-api.corp.apple.com`.
- The Westgate token itself encodes the DSID in the `dsid` JWT claim — that is how the script above derives it without hardcoding.
