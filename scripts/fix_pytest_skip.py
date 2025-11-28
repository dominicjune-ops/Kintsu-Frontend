#!/usr/bin/env python3
"""
Quick fix script for pytest.skip() syntax errors
Run this to automatically fix the TypeError in test files
"""

import os
import re
from pathlib import Path


def fix_pytest_skip(file_path: Path) -> bool:
    """
    Fix pytest.skip() calls with incorrect 'msg' parameter.
    
    Args:
        file_path: Path to the test file
        
    Returns:
        bool: True if file was modified, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match: pytest.skip(allow_module_level=True, msg="...")
        # Replace with: pytest.skip("...", allow_module_level=True)
        pattern = r'pytest\.skip\(allow_module_level=True,\s*msg=(\"|\')([^\"\']*)\1\)'
        replacement = r'pytest.skip(\1\2\1, allow_module_level=True)'
        
        content = re.sub(pattern, replacement, content)
        
        # If content changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f" Fixed: {file_path}")
            return True
        else:
            print(f"ℹ️  No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f" Error processing {file_path}: {e}")
        return False


def main():
    """Main function to fix all affected test files"""
    
    # Files that need fixing based on error report
    files_to_fix = [
        'tests/test_timing_integration.py',
        'tests/test_timing_ml_model.py'
    ]
    
    print(" pytest.skip() Syntax Fixer\n")
    print("=" * 60)
    
    fixed_count = 0
    for file_path in files_to_fix:
        path = Path(file_path)
        if path.exists():
            if fix_pytest_skip(path):
                fixed_count += 1
        else:
            print(f"  File not found: {file_path}")
    
    print("=" * 60)
    print(f"\n✨ Fixed {fixed_count} file(s)")
    
    if fixed_count > 0:
        print("\n Next steps:")
        print("1. Run: pytest --collect-only")
        print("2. If successful, run: pytest --maxfail=5 --disable-warnings")
        print("3. Check coverage: pytest --cov=src --cov-report=term")
    
    return fixed_count


if __name__ == '__main__':
    main()