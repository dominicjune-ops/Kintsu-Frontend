# RBAC & Credential Governance Checklist

## Role-Based Access Control (RBAC)
- [ ] Review repository, CI/CD, and cloud access roles quarterly
- [ ] Enforce least privilege for all users and service accounts
- [ ] Remove unused or stale accounts immediately
- [ ] Require MFA for all privileged accounts

## Credential Rotation
- [ ] Rotate all secrets and credentials at least every 90 days
- [ ] Use short-lived tokens for automation and CI/CD
- [ ] Store secrets in secure vaults (GitHub/Azure variable groups, Key Vault)
- [ ] Audit secret usage and access logs regularly

## Automation
- [ ] Add a scheduled job to check for stale users and credentials
- [ ] Alert on privilege escalations or suspicious access

---
*For more, see compliance/policies.md and compliance/roles-and-responsibilities.md.*
