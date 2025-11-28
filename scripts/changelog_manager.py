#!/usr/bin/env python3
"""
Changelog Management Tool for Kintsu
Helps maintain and update the project changelog
"""

import os
import re
from datetime import datetime
from typing import List, Dict

class ChangelogManager:
    def __init__(self, changelog_path: str = "CHANGELOG.md"):
        self.changelog_path = changelog_path
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        
    def add_entry(self, version: str, entry_type: str, description: str):
        """Add a new entry to the changelog"""
        
        # Entry types: Added, Changed, Deprecated, Removed, Fixed, Security
        valid_types = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security", "Improved"]
        
        if entry_type not in valid_types:
            print(f" Invalid entry type. Use one of: {', '.join(valid_types)}")
            return
            
        # Read current changelog
        with open(self.changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the unreleased section or create new version
        unreleased_pattern = r'## \[Unreleased\]'
        
        if version == "unreleased":
            # Add to unreleased section
            new_entry = f"\n###  {entry_type}\n- {description}"
            
            if "## [Unreleased]" in content:
                # Add to existing unreleased section
                content = re.sub(
                    r'(## \[Unreleased\])',
                    f'\\1{new_entry}',
                    content
                )
            else:
                # Create unreleased section
                new_section = f"## [Unreleased]{new_entry}\n\n"
                content = re.sub(
                    r'(# Kintsu Changelog.*?\n\n)',
                    f'\\1{new_section}',
                    content,
                    flags=re.DOTALL
                )
        else:
            # Create new version section
            new_section = f"## [{version}] - {self.current_date}\n\n###  {entry_type}\n- {description}\n\n"
            content = re.sub(
                r'(## \[Unreleased\].*?\n\n)',
                f'\\1{new_section}',
                content,
                flags=re.DOTALL
            )
        
        # Write back to file
        with open(self.changelog_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Added {entry_type.lower()} entry to changelog")
        
    def create_release(self, version: str):
        """Convert unreleased changes to a new version release"""
        
        with open(self.changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace [Unreleased] with version and date
        content = re.sub(
            r'## \[Unreleased\]',
            f'## [{version}] - {self.current_date}',
            content
        )
        
        # Add new unreleased section
        content = re.sub(
            f'(## \\[{version}\\] - {self.current_date})',
            f'## [Unreleased]\n\n\\1',
            content
        )
        
        with open(self.changelog_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f" Created release {version}")
        
    def get_latest_changes(self) -> List[str]:
        """Get the latest changes from the changelog"""
        
        with open(self.changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract latest version changes
        pattern = r'## \[(.*?)\] - (.*?)\n(.*?)(?=## \[|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        if matches:
            version, date, changes = matches[0]
            return {
                'version': version,
                'date': date,
                'changes': changes.strip()
            }
        
        return None
        
    def interactive_add(self):
        """Interactive mode to add changelog entries"""
        
        print(" Kintsu Changelog Manager")
        print("=" * 40)
        
        # Get entry details
        print("\nEntry Types:")
        types = ["Added", "Changed", "Fixed", "Improved", "Removed", "Security", "Deprecated"]
        for i, entry_type in enumerate(types, 1):
            print(f"  {i}. {entry_type}")
        
        try:
            type_choice = int(input("\nSelect entry type (1-7): ")) - 1
            entry_type = types[type_choice]
        except (ValueError, IndexError):
            print(" Invalid choice")
            return
            
        description = input("\nDescribe the change: ").strip()
        if not description:
            print(" Description cannot be empty")
            return
            
        version = input("\nVersion (or 'unreleased'): ").strip() or "unreleased"
        
        # Add the entry
        self.add_entry(version, entry_type, description)
        
        # Show current changelog snippet
        print("\n Latest Changelog Entries:")
        print("-" * 30)
        latest = self.get_latest_changes()
        if latest:
            print(f"Version: {latest['version']} ({latest['date']})")
            print(latest['changes'][:200] + "..." if len(latest['changes']) > 200 else latest['changes'])

def main():
    """Main function for command-line usage"""
    import sys
    
    manager = ChangelogManager()
    
    if len(sys.argv) == 1:
        # Interactive mode
        manager.interactive_add()
    elif len(sys.argv) == 4:
        # Command-line mode: python changelog_manager.py <version> <type> <description>
        version, entry_type, description = sys.argv[1], sys.argv[2], sys.argv[3]
        manager.add_entry(version, entry_type, description)
    elif len(sys.argv) == 3 and sys.argv[1] == "release":
        # Release mode: python changelog_manager.py release <version>
        version = sys.argv[2]
        manager.create_release(version)
    else:
        print("Usage:")
        print("  python changelog_manager.py                                    # Interactive mode")
        print("  python changelog_manager.py <version> <type> <description>     # Add entry")
        print("  python changelog_manager.py release <version>                  # Create release")
        print("\nExample:")
        print("  python changelog_manager.py unreleased Added 'New search filters'")
        print("  python changelog_manager.py release 1.2.1")

if __name__ == "__main__":
    main()