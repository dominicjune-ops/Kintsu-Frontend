# OPA/Conftest Policy: Enforce Audit Log and Change Request for Destructive Actions

package main

default allow = true

# Block destructive PRs unless audit log and CR are present
allow {
  not input.destructive_action
}

allow {
  input.audit_log_present
  input.cr_approval_present
}

# Example input:
# {
#   "destructive_action": true,
#   "audit_log_present": true,
#   "cr_approval_present": true
# }
