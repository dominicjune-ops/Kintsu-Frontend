#!/usr/bin/env python3
"""
Audit Logger Script for CareerCoach.ai Compliance
Appends audit entries to /compliance/audit/audit-YYYY-MM-DD.log (append-only, versioned)
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

AUDIT_DIR = Path(__file__).parent.parent / "compliance" / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def log_audit_entry(user, action, affected_files, compliance_tags, approval_state=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user": user,
        "action": action,
        "affected_files": affected_files,
        "compliance_tags": compliance_tags,
        "approval_state": approval_state
    }
    log_file = AUDIT_DIR / f"audit-{datetime.utcnow().date()}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    # Optionally, set file to read-only after writing (enforced by CI or admin)
    # os.chmod(log_file, 0o444)
    print(f"Audit entry logged: {entry}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python audit_logger.py <user> <action> <affected_files> <compliance_tags> [approval_state]")
        print("Example: python audit_logger.py 'alice' 'delete_user' '[\"users/123.json\"]' '[\"gdpr\",\"delete\"]' 'approved'")
        sys.exit(1)
    user = sys.argv[1]
    action = sys.argv[2]
    affected_files = json.loads(sys.argv[3])
    compliance_tags = json.loads(sys.argv[4])
    approval_state = sys.argv[5] if len(sys.argv) > 5 else None
    log_audit_entry(user, action, affected_files, compliance_tags, approval_state)
