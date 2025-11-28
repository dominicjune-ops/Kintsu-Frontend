#!/usr/bin/env python3
"""
Version Management Script for CareerCoach.ai
Automatically manages version bumping and changelog releases
"""

import os
import re
import json
from datetime import datetime
from typing import Tuple

class VersionManager:
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.version_files = [
            "CHANGELOG.md",
            "core/production_app.py",
            "CareerCoach.ai.pyproj"
        ]
        
    def get_current_version(self) -> str:
        """Get current version from changelog"""
        try:
            with open("CHANGELOG.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the latest version
            pattern = r'## \[([\d\.]+)\] - \d{4}-\d{2}-\d{2}'
            matches = re.findall(pattern, content)
            
            if matches:
                return matches[0]
            else:
                return "1.0.0"  # Default if no version found
        except FileNotFoundError:
            return "1.0.0"
    
    def parse_version(self, version: str) -> Tuple[int, int, int]:
        """Parse version string into major, minor, patch"""
        try:
            major, minor, patch = map(int, version.split('.'))
            return major, minor, patch
        except ValueError:
            return 1, 0, 0
    
    def bump_version(self, bump_type: str = "patch") -> str:
        """Bump version based on type (major, minor, patch)"""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError("bump_type must be 'major', 'minor', or 'patch'")
        
        return f"{major}.{minor}.{patch}"
    
    def update_version_in_files(self, new_version: str):
        """Update version in all relevant files"""
        
        # Update FastAPI app version
        if os.path.exists("core/production_app.py"):
            with open("core/production_app.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update version in FastAPI app
            content = re.sub(
                r'version="[\d\.]+"',
                f'version="{new_version}"',
                content
            )
            
            with open("core/production_app.py", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f" Updated version in core/production_app.py")
        
        # Update .pyproj file version
        if os.path.exists("CareerCoach.ai.pyproj"):
            with open("CareerCoach.ai.pyproj", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add version property if not exists
            if "<Version>" not in content:
                content = re.sub(
                    r'(<Name>Kintsu</Name>)',
                    f'\\1\n    <Version>{new_version}</Version>',
                    content
                )
            else:
                content = re.sub(
                    r'<Version>[\d\.]+</Version>',
                    f'<Version>{new_version}</Version>',
                    content
                )
            
            with open("CareerCoach.ai.pyproj", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f" Updated version in CareerCoach.ai.pyproj")
    
    def create_release(self, bump_type: str = "patch", description: str = ""):
        """Create a new release with version bump"""
        
        # Get new version
        new_version = self.bump_version(bump_type)
        
        # Update changelog (convert unreleased to release)
        if os.path.exists("CHANGELOG.md"):
            with open("CHANGELOG.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace [Unreleased] with new version
            content = re.sub(
                r'## \[Unreleased\]',
                f'## [{new_version}] - {self.current_date}',
                content
            )
            
            # Add new unreleased section at top
            content = re.sub(
                f'(## \\[{new_version}\\] - {self.current_date})',
                f'## [Unreleased]\n\n\\1',
                content
            )
            
            with open("CHANGELOG.md", 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f" Updated CHANGELOG.md with version {new_version}")
        
        # Update version in other files
        self.update_version_in_files(new_version)
        
        # Create release summary
        print(f"\nRelease {new_version} created!")
        print(f"📅 Date: {self.current_date}")
        print(f" Bump type: {bump_type}")
        if description:
            print(f" Description: {description}")
        
        return new_version
    
    def generate_release_notes(self, version: str = None) -> str:
        """Generate release notes for a specific version"""
        
        if not version:
            version = self.get_current_version()
        
        try:
            with open("CHANGELOG.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract release notes for version
            pattern = f'## \\[{re.escape(version)}\\] - (.*?)\\n(.*?)(?=## \\[|$)'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                date, notes = match.groups()
                return f"# Release {version} ({date})\n\n{notes.strip()}"
            else:
                return f"# Release {version}\n\nNo release notes found."
                
        except FileNotFoundError:
            return f"# Release {version}\n\nChangelog not found."

def main():
    """Main function for command-line usage"""
    import sys
    
    manager = VersionManager()
    
    if len(sys.argv) == 1:
        # Show current version
        current = manager.get_current_version()
        print(f"Current version: {current}")
        print("\nUsage:")
        print("  python version_manager.py bump <major|minor|patch>  # Bump version")
        print("  python version_manager.py release <type>            # Create release")
        print("  python version_manager.py notes [version]           # Generate release notes")
        
    elif len(sys.argv) >= 2:
        command = sys.argv[1]
        
        if command == "bump" and len(sys.argv) == 3:
            bump_type = sys.argv[2]
            new_version = manager.bump_version(bump_type)
            print(f"🔼 Next {bump_type} version: {new_version}")
            
        elif command == "release" and len(sys.argv) >= 3:
            bump_type = sys.argv[2]
            description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            manager.create_release(bump_type, description)
            
        elif command == "notes":
            version = sys.argv[2] if len(sys.argv) > 2 else None
            notes = manager.generate_release_notes(version)
            print(notes)
            
        else:
            print(" Invalid command or arguments")

if __name__ == "__main__":
    main()