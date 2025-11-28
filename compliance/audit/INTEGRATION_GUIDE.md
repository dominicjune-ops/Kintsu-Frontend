# Audit Logging Integration Guide

This guide explains how to use the audit logging automation for compliance in CareerCoach.ai.

## 1. CLI/Script Usage
Use `scripts/audit_logger.py` to append audit entries from the command line or other scripts:

```
python scripts/audit_logger.py <user> <action> <affected_files> <compliance_tags> [approval_state]

# Example:
python scripts/audit_logger.py 'alice' 'delete_user' '["users/123.json"]' '["gdpr","delete"]' 'approved'
```

## 2. Backend/API Integration
Import and call `log_audit_event` from `scripts/audit_log_utils.py` in your backend code (e.g., FastAPI):

```python
from scripts.audit_log_utils import log_audit_event

# Example trigger in a FastAPI endpoint:
@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: str, current_user: str):
    # ... perform deletion ...
    log_audit_event(
        user=current_user,
        action="delete_user",
        affected_files=[f"users/{user_id}.json"],
        compliance_tags=["gdpr", "delete"],
        approval_state="approved"
    )
    return {"status": "deleted"}
```

### Preferred Triggers for API/Backend Integration
- **User/Admin Actions:** Data deletion, role changes, config updates
- **API Endpoints:** POST/PUT/DELETE on sensitive resources (users, jobs, applications, resumes)
- **Deployment/CI Events:** Deployments, migrations, or infra changes
- **Change Requests:** When a CR is created, approved, or rejected
- **Manual Overrides:** Emergency or manual admin actions

## 3. Immutability & Versioning
- Log files are append-only and versioned by date (e.g., `audit-2025-11-25.log`).
- Do not modify or delete existing log entries.
- Optionally, set log files to read-only after writing (enforced by CI or admin).

## 4. Review & Compliance
- Review logs in `/compliance/audit/` for audit readiness.
- Ensure all destructive actions have a corresponding audit entry and CR approval.

---
*For full requirements, see ../audit-log-spec.md.*
