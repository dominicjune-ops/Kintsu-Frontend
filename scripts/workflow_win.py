#!/usr/bin/env python3
"""
CareerCoach.ai Development Workflow Script (Windows Compatible)
Unified script for common development tasks without Unicode emojis
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Execute a command and return result with status indicators"""
    try:
        print(f"Running: {description}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, 
                              encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print("SUCCESS")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            print(f"ERROR: {result.stderr.strip()}")
        
        return result
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return None

def cmd_status():
    """Show current development status"""
    print("CareerCoach.ai Development Status")
    print("=" * 40)
    
    # Version info
    print("\nVersion Info:")
    run_command("python scripts\\version_manager.py", "Getting version info")
    
    # Git status
    print("\nGit Status:")
    run_command("git status --porcelain", "Checking git changes")
    
    # Recent commits
    print("\nRecent Commits:")
    run_command("git log --oneline -5", "Getting recent commits")
    
    # Python environment
    print("\nPython Environment:")
    run_command("python --version", "Python version")

def cmd_commit(message):
    """Add all changes and commit with message"""
    if not message:
        print("ERROR: Commit message required")
        print("Usage: workflow.py commit \"Your commit message\"")
        return
    
    # Add all changes
    run_command("git add -A", "Adding all changes")
    
    # Commit
    result = run_command(f'git commit -m "{message}"', "Committing changes")
    if result and result.returncode == 0:
        print("Commit successful!")

def cmd_feature(feature_name):
    """Add a new feature entry to changelog"""
    if not feature_name:
        print("ERROR: Feature name required")
        print("Usage: workflow.py feature \"Feature description\"")
        return
    
    result = run_command(f'python scripts\\changelog_manager.py add Added "{feature_name}"', 
                        "Adding feature to changelog")
    if result and result.returncode == 0:
        print("Feature added to changelog")

def cmd_changelog():
    """Interactive changelog management"""
    run_command("python scripts\\changelog_manager.py", "Opening changelog manager")

def cmd_version(bump_type=None):
    """Version management"""
    if bump_type:
        run_command(f"python scripts\\version_manager.py bump {bump_type}", 
                   f"Bumping {bump_type} version")
    else:
        run_command("python scripts\\version_manager.py", "Showing version info")

def cmd_deploy_check():
    """Run deployment readiness checks"""
    print("Deployment Readiness Check")
    print("=" * 30)
    
    checks = [
        ("python -m py_compile core/production_app.py", "Syntax check"),
        ("python -c \"import core.production_app\"", "Import check"),
        ("python healthcheck.py", "Health check"),
    ]
    
    all_passed = True
    for command, description in checks:
        result = run_command(command, description)
        if not result or result.returncode != 0:
            all_passed = False
    
    if all_passed:
        print("\nREADY for deployment")
    else:
        print("\nFIX issues before deploying")

def cmd_logs(log_type=None):
    """View application logs"""
    if log_type:
        run_command(f"python scripts\\log_viewer.py view --type {log_type}", f"Viewing {log_type} logs")
    else:
        run_command("python scripts\\log_viewer.py", "Opening log viewer")

def cmd_errors():
    """View recent errors"""
    run_command("python scripts\\log_viewer.py errors --since 24h", "Checking recent errors")

def cmd_server():
    """Start the development server"""
    print("Starting development server...")
    print("Press Ctrl+C to stop")
    try:
        subprocess.run([
            "python", "-m", "uvicorn", 
            "core.production_app:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped")

def show_help():
    """Show available commands"""
    print("CareerCoach.ai Development Workflow")
    print("=" * 35)
    print()
    print("Available commands:")
    print("  status              - Show development status")
    print("  commit <message>    - Add all changes and commit")
    print("  feature <name>      - Add feature to changelog")
    print("  changelog           - Interactive changelog management")
    print("  version [type]      - Show/bump version (major|minor|patch)")
    print("  deploy-check        - Run deployment readiness checks")
    print("  logs [type]         - View application logs (error, api, app, etc.)")
    print("  errors              - View recent errors")
    print("  server              - Start development server")
    print("  help                - Show this help message")
    print()
    print("Examples:")
    print("  python workflow_win.py status")
    print("  python workflow_win.py commit \"Add new feature\"")
    print("  python workflow_win.py feature \"Enhanced job search\"")
    print("  python workflow_win.py version minor")
    print("  python workflow_win.py logs error")
    print("  python workflow_win.py errors")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    if command == "status":
        cmd_status()
    elif command == "commit":
        message = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_commit(message)
    elif command == "feature":
        feature = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_feature(feature)
    elif command == "changelog":
        cmd_changelog()
    elif command == "version":
        bump_type = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_version(bump_type)
    elif command == "deploy-check":
        cmd_deploy_check()
    elif command == "logs":
        log_type = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_logs(log_type)
    elif command == "errors":
        cmd_errors()
    elif command == "server":
        cmd_server()
    elif command == "help":
        show_help()
    else:
        print(f"ERROR: Unknown command: {command}")
        print("Use 'python workflow_win.py help' for available commands")

if __name__ == "__main__":
    main()