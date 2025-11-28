#!/usr/bin/env python3
"""
Log Rotation & Data Retention Script
- Rotates audit logs older than 1 year to /compliance/audit/archive/
- Deletes logs older than 7 years (per retention policy)
"""
import os
from pathlib import Path
from datetime import datetime, timedelta

AUDIT_DIR = Path(__file__).parent.parent / "compliance" / "audit"
ARCHIVE_DIR = AUDIT_DIR / "archive"
ARCHIVE_DIR.mkdir(exist_ok=True)

now = datetime.now()
one_year_ago = now - timedelta(days=365)
seven_years_ago = now - timedelta(days=365*7)

for log_file in AUDIT_DIR.glob("audit-*.log"):
    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
    if mtime < seven_years_ago:
        log_file.unlink()
        print(f"Deleted old audit log: {log_file}")
    elif mtime < one_year_ago:
        log_file.rename(ARCHIVE_DIR / log_file.name)
        print(f"Archived audit log: {log_file}")
