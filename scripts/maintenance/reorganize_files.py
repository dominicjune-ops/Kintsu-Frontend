#!/usr/bin/env python3
"""
Repo Reorganization Utility
- Default is dry-run (prints planned moves)
- Use --apply to perform moves
- Generates a log of actions to logs/reorg_YYYYmmdd_HHMMSS.log

Supports Windows paths.
"""
import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Example move map (expand in stages)
MOVE_MAP = {
    # Docs consolidation examples
    "STRIPE_MANUAL_CLEANUP.md": "docs/integration/stripe/STRIPE_MANUAL_CLEANUP.md",
    "STRIPE_PRODUCT_UPDATE_CHECKLIST.md": "docs/integration/stripe/STRIPE_PRODUCT_UPDATE_CHECKLIST.md",
    "RENDER_DEPLOYMENT_STATUS.md": "docs/deployment/RENDER_DEPLOYMENT_STATUS.md",
    "archive/deprecated/QUICK_DEPLOY.md": "docs/deployment/archive/deprecated/QUICK_DEPLOY.md",
    "AZURE_ARTIFACTS_SETUP.md": "docs/integration/azure/AZURE_ARTIFACTS_SETUP.md",
    "AZURE_ARTIFACTS_FEED_CREATED.md": "docs/integration/azure/AZURE_ARTIFACTS_FEED_CREATED.md",
    # Stage 2: scripts/integrations/tests rearrangement (non-destructive; only if present)
    # Scripts -> dedicated folders
    "debug_epics.py": "scripts/debug/debug_epics.py",
    "debug_epics_detailed.py": "scripts/debug/debug_epics_detailed.py",
    "debug_update.py": "scripts/debug/debug_update.py",
    "debug_api.py": "scripts/debug/debug_api.py",
    "check_azure_status.py": "scripts/ops/check_azure_status.py",
    "check_current_states.py": "scripts/ops/check_current_states.py",
    "deployment_status.py": "scripts/deployment/deployment_status.py",

    # Tests at root -> tests/misc (non-pytest files or ad-hoc runners)
    "test_comprehensive_epic_review.py": "tests/misc/test_comprehensive_epic_review.py",

    # Integrations
    "azure_devops_realtime_sync.py": "integrations/azure/azure_devops_realtime_sync.py",
}

ALWAYS_CREATE_DIRS = [
    "docs/api",
    "docs/integration/azure",
    "docs/integration/stripe",
    "docs/deployment",
    "scripts/setup",
    "scripts/deployment",
    "scripts/maintenance",
    "scripts/debug",
    "scripts/ops",
    "integrations/azure",
    "tests/misc",
]


def ensure_dirs():
    for rel in ALWAYS_CREATE_DIRS:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)


def plan_moves():
    planned = []
    for src_rel, dst_rel in MOVE_MAP.items():
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if src.exists():
            planned.append((src, dst))
    return planned


def log(msg, fh):
    print(msg)
    fh.write(msg + "\n")


def perform_moves(planned, apply, fh):
    for src, dst in planned:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if apply:
            shutil.move(str(src), str(dst))
            log(f"MOVED: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}", fh)
        else:
            log(f"DRY-RUN: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}", fh)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply file moves")
    args = parser.parse_args()

    ensure_dirs()
    planned = plan_moves()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"reorg_{ts}.log"
    with open(log_file, "w", encoding="utf-8") as fh:
        log(f"Root: {ROOT}", fh)
        log(f"Moves planned: {len(planned)}", fh)
        perform_moves(planned, args.apply, fh)
        log("Done.", fh)

    print(f"Log written to: {log_file}")


if __name__ == "__main__":
    main()
