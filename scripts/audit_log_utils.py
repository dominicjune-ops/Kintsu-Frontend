"""
Backend Audit Logging Utility for API/Service Integration
Usage: import and call log_audit_event from backend code (e.g., FastAPI endpoints)
"""
import json
from datetime import datetime
from pathlib import Path

AUDIT_DIR = Path(__file__).parent.parent / "compliance" / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def log_audit_event(user, action, affected_files, compliance_tags, approval_state=None):
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

# Example preferred triggers for API/Backend integration:
# - Call log_audit_event in FastAPI route handlers for POST/PUT/DELETE on sensitive resources
# - Call after user/admin actions (e.g., user deletion, role change, config update)
# - Call in deployment/migration scripts for infra changes
# - Call when a change request is created/approved/rejected
# - Call for manual overrides or emergency actions
