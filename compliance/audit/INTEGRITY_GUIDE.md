# Audit Log Integrity & Tamper-Evidence

This script (`scripts/audit_log_integrity.py`) hashes all audit log files in `/compliance/audit/` and stores the results in `audit-hashes.json`.

## Usage

```
python scripts/audit_log_integrity.py
```

- Run this after each deployment or on a schedule (e.g., nightly CI job).
- Store `audit-hashes.json` in a secure, versioned location (e.g., cloud object storage, backup, or external SIEM).
- For high-assurance environments, sign the hash file with a GPG key and store the signature separately.

## Why?
- Ensures audit logs are tamper-evident and immutable.
- Supports compliance with SOX, SOC2, and GDPR audit requirements.

---
*For more, see compliance/audit-log-spec.md and compliance/audit/README.md.*
