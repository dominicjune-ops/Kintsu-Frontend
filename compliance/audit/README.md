# Audit Log Directory

This directory contains immutable, versioned audit logs for all compliance-relevant actions in CareerCoach.ai.

## Log Format
Each log entry is a JSON object with the following fields:
- timestamp (ISO 8601)
- user
- action
- affected_files
- compliance_tags
- approval_state

## Usage
- All actions must be logged using the audit logger script or backend utility.
- Log files are named `audit-YYYY-MM-DD.log` and are append-only.
- Do not modify or delete existing log entries.

## Review
- Review logs regularly for compliance and audit readiness.
- For destructive actions, ensure a change request (CR) approval is present before proceeding.

---
*See ../audit-log-spec.md for full requirements.*
