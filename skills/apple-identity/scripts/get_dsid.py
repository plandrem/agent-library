#!/usr/bin/env python3
"""Decode Westgate JWT to extract DSID and other identity claims."""
import base64, json, subprocess, sys

wg = subprocess.run(
    ["wgtool", "token", "coreanalytics-api.corp.apple.com"],
    capture_output=True, text=True,
)
if wg.returncode != 0:
    print("wgtool failed — ensure you have a valid AppleConnect session", file=sys.stderr)
    sys.exit(1)

token = wg.stdout.strip()
parts = token.split(".")
if len(parts) != 3:
    print(f"unexpected token format ({len(parts)} parts)", file=sys.stderr)
    sys.exit(1)

payload = parts[1]
payload += "=" * (-len(payload) % 4)
claims = json.loads(base64.urlsafe_b64decode(payload))

dsid = claims.get("dsid")
user = claims.get("usr") or claims.get("mail")
print(f"DSID:     {dsid}")
print(f"username: {user}")
print(f"name:     {claims.get('fn')} {claims.get('ln')}")
print(f"email:    {claims.get('mail')}")
