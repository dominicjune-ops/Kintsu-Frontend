#!/usr/bin/env python3
"""
Documentation Drift Checker
- Checks for missing or outdated compliance documentation
- Flags files that have not been updated in the last 90 days
"""
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

DOC_DIRS = [
    Path("compliance"),
    Path("docs"),
]
DAYS_THRESHOLD = 90

def check_drift():
    now = datetime.now()
    cutoff = now - timedelta(days=DAYS_THRESHOLD)
    flagged = []
    for doc_dir in DOC_DIRS:
        if not doc_dir.exists():
            continue
        for root, _, files in os.walk(doc_dir):
            for f in files:
                if f.endswith(".md"):
                    path = Path(root) / f
                    mtime = datetime.fromtimestamp(path.stat().st_mtime)
                    if mtime < cutoff:
                        flagged.append(str(path))
    if flagged:
        print("Documentation drift detected in:")
        for f in flagged:
            print(f" - {f}")
    else:
        print("All compliance documentation is up to date.")

if __name__ == "__main__":
    check_drift()
