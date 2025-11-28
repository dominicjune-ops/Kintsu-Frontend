#!/usr/bin/env python3
"""
Compliance Dashboard Generator
- Summarizes audit log activity, documentation status, and compliance health
- Outputs a markdown report for stakeholders
"""
import json
from pathlib import Path
from datetime import datetime

AUDIT_DIR = Path(__file__).parent.parent / "compliance" / "audit"
DOC_DIR = Path("compliance")
REPORT_FILE = AUDIT_DIR / "compliance-dashboard.md"

def summarize_audit_logs():
    entries = 0
    for log_file in AUDIT_DIR.glob("audit-*.log"):
        with open(log_file, "r", encoding="utf-8") as f:
            entries += sum(1 for _ in f)
    return entries

def summarize_docs():
    docs = list(DOC_DIR.glob("*.md"))
    return len(docs)

def main():
    audit_count = summarize_audit_logs()
    doc_count = summarize_docs()
    now = datetime.utcnow().isoformat() + "Z"
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Compliance Dashboard\n\n")
        f.write(f"**Generated:** {now}\n\n")
        f.write(f"- Total audit log entries: {audit_count}\n")
        f.write(f"- Compliance documentation files: {doc_count}\n")
        f.write(f"- Last dashboard update: {now}\n\n")
        f.write(f"---\n")
        f.write(f"*For more, see compliance/audit-log-spec.md and compliance/README.md.*\n")
    print(f"Compliance dashboard written to {REPORT_FILE}")

if __name__ == "__main__":
    main()
