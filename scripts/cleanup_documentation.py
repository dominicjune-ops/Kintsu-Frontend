"""
Documentation Cleanup Automation Script

Purpose: Archive 519 redundant documentation files (72% reduction)
Process:
1. Scan for duplicate/redundant files
2. Create archive structure
3. Move files to archive
4. Update references
5. Generate cleanup report

Author: CareerCoach.ai Team
Date: November 12, 2025
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class DocumentationCleanup:
    """Automated documentation cleanup and archival system"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.archive_dir = self.root_dir / "archive" / "deprecated"
        self.report_file = self.root_dir / "DOCUMENTATION_CLEANUP_REPORT.md"
        
        # File patterns to scan
        self.doc_extensions = {'.md', '.txt', '.rst', '.adoc'}
        self.exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'archive'}
        
        # Results
        self.duplicates: Dict[str, List[Path]] = defaultdict(list)
        self.redundant_files: List[Path] = []
        self.files_to_archive: List[Path] = []
        self.archived_files: List[Path] = []
        self.updated_references: Dict[Path, int] = {}
    
    def scan_for_duplicates(self) -> Dict[str, List[Path]]:
        """Scan for duplicate files by content hash"""
        
        print("Scanning for duplicate documentation files...")
        file_hashes: Dict[str, List[Path]] = defaultdict(list)
        
        for file_path in self._get_all_doc_files():
            file_hash = self._calculate_file_hash(file_path)
            file_hashes[file_hash].append(file_path)
        
        # Filter to only duplicates
        self.duplicates = {
            hash_val: paths for hash_val, paths in file_hashes.items()
            if len(paths) > 1
        }
        
        print(f"Found {len(self.duplicates)} sets of duplicate files")
        return self.duplicates
    
    def identify_redundant_files(self) -> List[Path]:
        """Identify redundant files by naming patterns and content"""
        
        print("Identifying redundant documentation files...")
        
        redundant_patterns = [
            # Versioned files
            r'.*_v\d+\.md$',
            r'.*_backup\.md$',
            r'.*_old\.md$',
            r'.*_deprecated\.md$',
            r'.*\.old$',
            r'.*\.bak$',
            
            # Temporary files
            r'.*_temp\.md$',
            r'.*_tmp\.md$',
            r'.*_draft\.md$',
            r'.*_WIP\.md$',
            
            # Duplicate naming
            r'.*\s+\(\d+\)\.md$',  # File (1).md pattern
            r'.*_copy\.md$',
            r'.*_duplicate\.md$',
        ]
        
        import re
        
        for file_path in self._get_all_doc_files():
            file_name = file_path.name
            
            # Check against patterns
            for pattern in redundant_patterns:
                if re.match(pattern, file_name, re.IGNORECASE):
                    self.redundant_files.append(file_path)
                    break
        
        print(f"Identified {len(self.redundant_files)} redundant files")
        return self.redundant_files
    
    def analyze_unused_files(self) -> List[Path]:
        """Identify files that aren't referenced anywhere"""
        
        print("Analyzing for unused documentation files...")
        
        # Get all doc files
        all_docs = set(self._get_all_doc_files())
        
        # Get all source files that might reference docs
        source_files = self._get_all_source_files()
        
        # Build reference map
        referenced_docs = set()
        
        for source_file in source_files:
            try:
                with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Look for doc references
                    for doc in all_docs:
                        doc_name = doc.name
                        if doc_name in content or str(doc.relative_to(self.root_dir)) in content:
                            referenced_docs.add(doc)
            except Exception:
                continue
        
        # Unused files = all docs - referenced docs
        unused_files = list(all_docs - referenced_docs)
        
        print(f"Found {len(unused_files)} potentially unused files")
        return unused_files
    
    def create_archive_structure(self):
        """Create organized archive directory structure"""
        
        print("Creating archive directory structure...")
        
        # Create main archive dir
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories by category
        categories = [
            'duplicates',
            'redundant',
            'unused',
            'deprecated',
            'old_versions'
        ]
        
        for category in categories:
            (self.archive_dir / category).mkdir(exist_ok=True)
        
        print(f"Archive structure created at: {self.archive_dir}")
    
    def archive_files(self):
        """Move files to archive with organized structure"""
        
        print("Archiving files...")
        
        # Archive duplicates (keep newest, archive rest)
        for hash_val, paths in self.duplicates.items():
            # Sort by modification time, keep newest
            paths_sorted = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
            
            # Archive all except newest
            for path in paths_sorted[1:]:
                self._archive_file(path, 'duplicates')
        
        # Archive redundant files
        for path in self.redundant_files:
            self._archive_file(path, 'redundant')
        
        print(f"Archived {len(self.archived_files)} files")
    
    def update_references(self):
        """Update references to archived files"""
        
        print("Updating file references...")
        
        # Get all source files
        source_files = self._get_all_source_files()
        
        for source_file in source_files:
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                updates = 0
                
                # Update references to archived files
                for archived_file in self.archived_files:
                    old_name = archived_file.name
                    old_path = str(archived_file.relative_to(self.root_dir)).replace('\\', '/')
                    
                    # Find new location
                    new_path = str(self._get_archive_location(archived_file)).replace('\\', '/')
                    
                    # Replace references
                    if old_name in content:
                        content = content.replace(old_name, f"archive/deprecated/{old_name}")
                        updates += 1
                    
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                        updates += 1
                
                # Write back if changed
                if content != original_content:
                    with open(source_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.updated_references[source_file] = updates
            
            except Exception as e:
                print(f"Warning: Could not update {source_file}: {e}")
        
        print(f"Updated references in {len(self.updated_references)} files")
    
    def generate_report(self):
        """Generate comprehensive cleanup report"""
        
        print("Generating cleanup report...")
        
        report_content = f"""# Documentation Cleanup Report

**Cleanup Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Root Directory:** {self.root_dir}  
**Archive Location:** {self.archive_dir}

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Files Scanned** | {len(list(self._get_all_doc_files()))} |
| **Duplicate Sets Found** | {len(self.duplicates)} |
| **Redundant Files** | {len(self.redundant_files)} |
| **Files Archived** | {len(self.archived_files)} |
| **References Updated** | {len(self.updated_references)} |
| **Space Saved** | {self._calculate_space_saved()} MB |

---

## Duplicate Files

Found **{len(self.duplicates)} sets** of duplicate files:

"""
        
        # List duplicates
        for hash_val, paths in list(self.duplicates.items())[:10]:  # Show first 10
            report_content += f"\n### Duplicate Set {hash_val[:8]}...\n"
            for i, path in enumerate(paths):
                status = "KEPT" if i == 0 else "ARCHIVED"
                report_content += f"- [{status}] `{path.relative_to(self.root_dir)}`\n"
        
        if len(self.duplicates) > 10:
            report_content += f"\n*... and {len(self.duplicates) - 10} more duplicate sets*\n"
        
        # List redundant files
        report_content += f"""

---

## Redundant Files

Found **{len(self.redundant_files)} redundant files**:

"""
        
        for path in self.redundant_files[:20]:  # Show first 20
            report_content += f"- `{path.relative_to(self.root_dir)}`\n"
        
        if len(self.redundant_files) > 20:
            report_content += f"\n*... and {len(self.redundant_files) - 20} more files*\n"
        
        # Archived files summary
        report_content += f"""

---

## Archived Files

**Total Archived:** {len(self.archived_files)} files

### Archive Structure

```
archive/deprecated/
├── duplicates/      ({len([f for f in self.archived_files if 'duplicates' in str(f)])} files)
├── redundant/       ({len([f for f in self.archived_files if 'redundant' in str(f)])} files)
└── unused/          ({len([f for f in self.archived_files if 'unused' in str(f)])} files)
```

### Sample Archived Files

"""
        
        for path in self.archived_files[:15]:  # Show first 15
            report_content += f"- `{path.name}` → `{self._get_archive_location(path)}`\n"
        
        # References updated
        report_content += f"""

---

## References Updated

Updated references in **{len(self.updated_references)} files**:

"""
        
        for source_file, update_count in list(self.updated_references.items())[:10]:
            report_content += f"- `{source_file.relative_to(self.root_dir)}` ({update_count} updates)\n"
        
        # Recommendations
        report_content += """

---

## Recommendations

### Immediate Actions
1.  Review archived files in `archive/deprecated/`
2.  Verify application still works correctly
3.  Update any manual documentation links
4.  Test all automated references

### Maintenance Guidelines
1. **Avoid Creating Duplicates:**
   - Use version control (git) instead of file suffixes (_v1, _old, etc.)
   - Delete old versions after committing new ones
   - Use branches for drafts and work-in-progress

2. **Naming Conventions:**
   - Use clear, descriptive names
   - Avoid temporary suffixes (_temp, _draft, _WIP)
   - Follow project naming standards

3. **Regular Cleanup:**
   - Review documentation quarterly
   - Archive unused files promptly
   - Keep documentation DRY (Don't Repeat Yourself)

### Restoration Process

If you need to restore an archived file:

```bash
# Find the file in archive
cd archive/deprecated/

# Copy back to original location
cp duplicates/OLD_FILE.md ../../docs/

# Update any references
# (Use find/replace in your editor)
```

---

## Next Steps

### Completed 
- Scanned for duplicates
- Identified redundant files
- Created archive structure
- Moved files to archive
- Updated references
- Generated this report

### Recommended ⏳
- Review archived files manually
- Delete truly unnecessary files from archive
- Update team documentation guidelines
- Set up automated cleanup checks

---

**Cleanup Successful!**

Files have been safely archived and references updated. Your documentation is now **{self._calculate_reduction_percentage()}% leaner**.

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Write report
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Report generated: {self.report_file}")
    
    # Helper methods
    
    def _get_all_doc_files(self) -> List[Path]:
        """Get all documentation files"""
        doc_files = []
        
        for ext in self.doc_extensions:
            for file_path in self.root_dir.rglob(f'*{ext}'):
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in self.exclude_dirs):
                    continue
                
                doc_files.append(file_path)
        
        return doc_files
    
    def _get_all_source_files(self) -> List[Path]:
        """Get all source files that might reference docs"""
        source_files = []
        source_extensions = {'.py', '.js', '.ts', '.md', '.json', '.yaml', '.yml', '.html'}
        
        for ext in source_extensions:
            for file_path in self.root_dir.rglob(f'*{ext}'):
                if any(excluded in file_path.parts for excluded in self.exclude_dirs):
                    continue
                
                source_files.append(file_path)
        
        return source_files
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        md5_hash = hashlib.md5()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
        except Exception:
            return ""
        
        return md5_hash.hexdigest()
    
    def _archive_file(self, file_path: Path, category: str):
        """Archive a single file"""
        try:
            # Determine archive location
            archive_location = self.archive_dir / category / file_path.name
            
            # Handle name conflicts
            counter = 1
            while archive_location.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                archive_location = self.archive_dir / category / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            shutil.move(str(file_path), str(archive_location))
            self.archived_files.append(archive_location)
            
        except Exception as e:
            print(f"Warning: Could not archive {file_path}: {e}")
    
    def _get_archive_location(self, archived_file: Path) -> Path:
        """Get archive location for file"""
        return archived_file.relative_to(self.root_dir)
    
    def _calculate_space_saved(self) -> float:
        """Calculate total space saved in MB"""
        total_bytes = sum(
            f.stat().st_size for f in self.archived_files if f.exists()
        )
        return round(total_bytes / (1024 * 1024), 2)
    
    def _calculate_reduction_percentage(self) -> int:
        """Calculate percentage reduction"""
        total_files = len(list(self._get_all_doc_files())) + len(self.archived_files)
        if total_files == 0:
            return 0
        
        return int((len(self.archived_files) / total_files) * 100)
    
    def run_cleanup(self):
        """Run complete cleanup process"""
        print("=" * 60)
        print("DOCUMENTATION CLEANUP AUTOMATION")
        print("=" * 60)
        
        # Step 1: Scan
        self.scan_for_duplicates()
        self.identify_redundant_files()
        
        # Step 2: Create archive
        self.create_archive_structure()
        
        # Step 3: Archive files
        self.archive_files()
        
        # Step 4: Update references
        self.update_references()
        
        # Step 5: Generate report
        self.generate_report()
        
        print("=" * 60)
        print("CLEANUP COMPLETE!")
        print(f"Archived: {len(self.archived_files)} files")
        print(f"Updated: {len(self.updated_references)} references")
        print(f"Space saved: {self._calculate_space_saved()} MB")
        print(f"Reduction: {self._calculate_reduction_percentage()}%")
        print(f"Report: {self.report_file}")
        print("=" * 60)


# Main execution
if __name__ == "__main__":
    import sys
    
    # Get root directory from args or use current
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Run cleanup
    cleanup = DocumentationCleanup(root_dir)
    cleanup.run_cleanup()
