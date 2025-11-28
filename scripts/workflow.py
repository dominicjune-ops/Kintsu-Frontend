#!/usr/bin/env python3
"""
Development Workflow Script for CareerCoach.ai
Quick commands for common development tasks
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command: str, description: str = ""):
    """Run a command and handle output"""
    if description:
        print(f" {description}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f" Success")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            print(f" Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f" Exception: {e}")
        return False

def show_status():
    """Show current project status"""
    print(" CareerCoach.ai Development Status")
    print("=" * 40)
    
    # Version info
    run_command("python scripts/version_manager.py", "Getting version info")
    
    # Git status
    print("\n📂 Git Status:")
    run_command("git status --porcelain", "Checking git changes")
    
    # Recent commits
    print("\n Recent Commits:")
    run_command("git log --oneline -n 5", "Getting recent commits")
    
    # Environment check
    print("\n🐍 Python Environment:")
    run_command("python --version", "Python version")
    
def quick_commit(message: str):
    """Quick commit with standard format"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    print(f" Quick Commit: {message}")
    print("=" * 40)
    
    # Add all changes
    if run_command("git add .", "Adding changes"):
        # Commit with formatted message
        commit_msg = f"feat: {message}\n\nTimestamp: {timestamp}\nQuick commit via workflow script"
        if run_command(f'git commit -m "{commit_msg}"', "Committing changes"):
            print(" Commit successful!")
            return True
    
    return False

def new_feature(feature_name: str, feature_type: str = "Added"):
    """Start working on a new feature"""
    print(f" Starting new feature: {feature_name}")
    print("=" * 40)
    
    # Add to changelog
    changelog_cmd = f'python scripts/changelog_manager.py unreleased "{feature_type}" "{feature_name}"'
    if run_command(changelog_cmd, "Adding to changelog"):
        print(" Feature added to changelog")
        
        # Optional: Create feature branch
        create_branch = input("Create feature branch? (y/N): ").lower() == 'y'
        if create_branch:
            branch_name = feature_name.lower().replace(' ', '-').replace(',', '')
            branch_cmd = f"git checkout -b feature/{branch_name}"
            run_command(branch_cmd, f"Creating branch feature/{branch_name}")

def deploy_check():
    """Run pre-deployment checks"""
    print(" Pre-Deployment Checks")
    print("=" * 40)
    
    checks = [
        ("python healthcheck.py", "Running health check"),
        ("python -m pytest tests/ -v", "Running tests"),
        ("python -c 'from core.production_app import app; print(\" App imports successfully\")'", "Testing imports"),
    ]
    
    all_passed = True
    for command, description in checks:
        print(f"\n{description}...")
        if not run_command(command, ""):
            all_passed = False
    
    if all_passed:
        print("\n All deployment checks passed!")
        print(" Ready for deployment")
    else:
        print("\n  Some checks failed")
        print(" Fix issues before deploying")
    
    return all_passed

def show_help():
    """Show available commands"""
    print("🛠️  CareerCoach.ai Development Workflow")
    print("=" * 40)
    print("Commands:")
    print("  status                           # Show project status")
    print("  commit <message>                 # Quick commit with message")
    print("  feature <name> [type]           # Start new feature")
    print("  changelog <type> <description>   # Add changelog entry")
    print("  version <bump_type>             # Bump version (patch/minor/major)")
    print("  release <type>                  # Create release")
    print("  deploy-check                    # Run pre-deployment checks")
    print("  server                          # Start development server")
    print("")
    print("Examples:")
    print("  python workflow.py commit 'Add new search filters'")
    print("  python workflow.py feature 'Email notifications' Added")
    print("  python workflow.py version patch")
    print("  python workflow.py release minor")

def main():
    """Main workflow function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_status()
        
    elif command == "commit" and len(sys.argv) >= 3:
        message = " ".join(sys.argv[2:])
        quick_commit(message)
        
    elif command == "feature" and len(sys.argv) >= 3:
        feature_name = sys.argv[2]
        feature_type = sys.argv[3] if len(sys.argv) > 3 else "Added"
        new_feature(feature_name, feature_type)
        
    elif command == "changelog" and len(sys.argv) >= 4:
        entry_type = sys.argv[2]
        description = " ".join(sys.argv[3:])
        run_command(f'python scripts/changelog_manager.py unreleased "{entry_type}" "{description}"')
        
    elif command == "version" and len(sys.argv) >= 3:
        bump_type = sys.argv[2]
        run_command(f'python scripts/version_manager.py bump {bump_type}')
        
    elif command == "release" and len(sys.argv) >= 3:
        bump_type = sys.argv[2]
        description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        run_command(f'python scripts/version_manager.py release {bump_type} {description}')
        
    elif command == "deploy-check":
        deploy_check()
        
    elif command == "server":
        print(" Starting CareerCoach.ai development server...")
        os.system("careercoach-env\\Scripts\\uvicorn.exe core.production_app:app --host 127.0.0.1 --port 8080 --reload")
        
    else:
        print(f" Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()