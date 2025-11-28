# Audit Log Retention & Rotation

This script (`scripts/audit_log_retention.py`) rotates audit logs older than 1 year to `/compliance/audit/archive/` and deletes logs older than 7 years.

## Usage

```
python scripts/audit_log_retention.py
```

- Run this as a scheduled job (e.g., monthly CI job) to enforce data retention policies.
- Review archived logs before deletion.

---
*For more, see compliance/audit-log-spec.md and docs/DOCUMENTATION_MAINTENANCE_SCHEDULE.md.*
