#!/usr/bin/env python3
"""Quick Python 3.8 compatibility check - no dependencies."""
import sys
from pathlib import Path

# Methods/features not available in Python 3.8
PYTHON_39_PLUS = [
    'readlink',  # Path.readlink()
    'removeprefix',  # str.removeprefix()
    'removesuffix',  # str.removesuffix()
    'is_relative_to',  # Path.is_relative_to()
]

def check_file(filepath):
    """Check single file for compatibility issues."""
    issues = []
    try:
        code = filepath.read_text()

        # Check for newer methods
        for method in PYTHON_39_PLUS:
            if f'.{method}(' in code:
                # Find line number
                for i, line in enumerate(code.splitlines(), 1):
                    if f'.{method}(' in line:
                        # Skip if it's os.readlink (which is fine)
                        if method == 'readlink' and 'os.readlink' in line:
                            continue
                        issues.append(f"{filepath}:{i} - Uses {method}() (Python 3.9+)")

        # Check for dict union operator
        if ' | ' in code and '.py' in str(filepath):
            for i, line in enumerate(code.splitlines(), 1):
                if ' | ' in line and not '#' in line.split(' | ')[0]:
                    # Might be dict union, warn
                    if 'dict' in line.lower() or '{' in line:
                        issues.append(f"{filepath}:{i} - Possible dict union | operator (Python 3.9+)")

    except Exception:
        pass  # Skip files that can't be read

    return issues

def main():
    """Check all Python files for compatibility."""
    print("Checking Python 3.8 compatibility...")

    issues = []
    files_checked = 0

    for pyfile in Path('.').rglob('*.py'):
        # Skip virtual environments and build directories
        if any(part in str(pyfile) for part in ['venv', '.tox', 'build', 'dist', '__pycache__']):
            continue

        # Skip this file to avoid false positives
        if 'check_compatibility.py' in str(pyfile):
            continue

        files_checked += 1
        issues.extend(check_file(pyfile))

    if issues:
        print(f"\n⚠️  Found {len(issues)} Python 3.8 compatibility issues:\n")
        for issue in issues:
            print(f"  {issue}")
        print("\nFix these before pushing to avoid CI failures.")
        return 1
    else:
        print(f"✅ All {files_checked} files are Python 3.8 compatible")
        return 0

if __name__ == '__main__':
    sys.exit(main())