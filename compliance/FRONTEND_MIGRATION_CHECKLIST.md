# Kintsu Frontend Compliance & Governance Migration Checklist

This checklist will help you migrate and activate the full compliance, audit, and SecOps automation framework in the Kintsu frontend repository.

---

## 1. Copy Files & Folders
- [ ] Copy the entire `compliance/` directory from the backend repo to the frontend repo root.
- [ ] Copy the entire `scripts/` directory (all Python scripts) to the frontend repo root.
- [ ] Copy `.github/workflows/compliance-policy.yml` to `.github/workflows/` in the frontend repo.
- [ ] Copy `.github/pull_request_template.md` to `.github/` in the frontend repo.
- [ ] Copy `compliance/policy/` directory as-is.

## 2. Adjust Integration Points
- [ ] For frontend admin panels, call audit logging scripts for destructive/config actions.
- [ ] Integrate audit logging into frontend CI/CD (deployments, config changes, etc.).
- [ ] Update any script paths if the frontend repo structure differs.

## 3. Enable Workflows
- [ ] Commit and push all copied files to the frontend repo.
- [ ] Enable GitHub Actions (or your CI/CD system) for the frontend repo.
- [ ] Schedule compliance scripts (integrity, retention, doc drift, dashboard) as needed.

## 4. Documentation & Training
- [ ] Ensure all compliance guides, checklists, and integration docs are present in the frontend repo.
- [ ] Notify all contributors of the new compliance requirements and workflow.

## 5. Review & Activate
- [ ] Test audit logging from both scripts and frontend code.
- [ ] Confirm policy enforcement in PRs and CI/CD.
- [ ] Review compliance dashboard and documentation drift reports.

---

*For questions or help, see `compliance/README.md` and `compliance/audit/INTEGRATION_GUIDE.md`.*
