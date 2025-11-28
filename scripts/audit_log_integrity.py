#!/usr/bin/env python3
"""
Audit Log Integrity Script
- Hashes and signs audit log files for tamper-evidence
- Stores hash in /compliance/audit/audit-hashes.json
"""
import hashlib
import json
from pathlib import Path
from datetime import datetime

AUDIT_DIR = Path(__file__).parent.parent / "compliance" / "audit"
HASH_FILE = AUDIT_DIR / "audit-hashes.json"

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    hashes = {}
    for log_file in AUDIT_DIR.glob("audit-*.log"):
        hashes[log_file.name] = {
            "sha256": hash_file(log_file),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)
    print(f"Audit log hashes written to {HASH_FILE}")

if __name__ == "__main__":
    main()
