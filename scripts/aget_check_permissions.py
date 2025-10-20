#!/usr/bin/env python3
"""
Check file permissions for AGET template release.

This script verifies that all files in the template have correct permissions:
- Shell scripts (.sh): 755 (executable)
- Python scripts with shebang: 755 (executable)
- Python modules/libraries: 644 (non-executable)
- Directories: 755
- Documentation/config files: 644
"""

import os
import stat
import sys
from pathlib import Path
from typing import List, Tuple

def get_file_permissions(path: Path) -> str:
    """Get octal permissions string for a file."""
    mode = path.stat().st_mode
    return oct(stat.S_IMODE(mode))[-3:]

def has_shebang(path: Path) -> bool:
    """Check if file starts with shebang."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            return first_line.startswith('#!')
    except Exception:
        return False

def check_permissions(root_dir: Path) -> Tuple[List[str], List[str]]:
    """Check all file permissions in the template."""
    errors = []
    warnings = []

    # Directories to skip
    skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'aget_cli_agent_template.egg-info',
                 '.archive', 'SESSION_NOTES', '.claude'}

    for path in root_dir.rglob('*'):
        # Skip certain directories
        if any(skip_dir in path.parts for skip_dir in skip_dirs):
            continue

        rel_path = path.relative_to(root_dir)
        perms = get_file_permissions(path)

        if path.is_dir():
            # Directories should be 755
            if perms not in ['755', '700']:  # 700 for private dirs like .aget, .claude
                if path.name in ['.aget', '.claude']:
                    continue  # These can be 700
                errors.append(f"Directory {rel_path}: has {perms}, expected 755")

        elif path.is_file():
            # Check shell scripts
            if path.suffix == '.sh':
                if perms != '755':
                    errors.append(f"Shell script {rel_path}: has {perms}, expected 755")

            # Check Python files
            elif path.suffix == '.py':
                # Test files should not have shebangs or be executable
                is_test = 'test' in path.name or path.parts[-2] == 'tests' if len(path.parts) > 1 else False

                if is_test:
                    if has_shebang(path):
                        warnings.append(f"Test file {rel_path}: has shebang but test files shouldn't")
                    if perms == '755':
                        warnings.append(f"Test file {rel_path}: is executable but test files shouldn't be")
                elif has_shebang(path):
                    # Python scripts with shebang should be executable
                    if perms != '755':
                        # Some files legitimately have shebangs but aren't meant to be run directly
                        # (e.g., example files, templates)
                        if any(skip in str(path) for skip in ['examples/', 'templates/', 'tests/']):
                            warnings.append(f"Python file {rel_path}: has shebang but in {path.parts[-2]}/ directory")
                        else:
                            errors.append(f"Python script {rel_path}: has shebang but permissions are {perms}, expected 755")
                else:
                    # Python modules should not be executable
                    if perms == '755':
                        # Check if it's intentionally executable (like in .aget/patterns)
                        if '.aget/patterns' in str(path):
                            continue  # Pattern scripts can be executable
                        warnings.append(f"Python module {rel_path}: is executable ({perms}) but has no shebang")

            # Check other executables
            elif perms == '755' and path.suffix not in ['.sh']:
                # Special cases
                if path.name in ['install.sh', 'aget.sh', 'session_logger.sh']:
                    continue
                if path.suffix == '':  # No extension, might be intentional
                    continue
                warnings.append(f"File {rel_path}: is executable ({perms}) but may not need to be")

    return errors, warnings

def fix_permissions(root_dir: Path, dry_run: bool = True) -> None:
    """Fix file permissions (with dry-run option)."""
    errors, _ = check_permissions(root_dir)

    if not errors:
        print("✅ All file permissions are correct!")
        return

    print(f"Found {len(errors)} permission issues:")
    for error in errors:
        print(f"  ❌ {error}")

    if dry_run:
        print("\nTo fix these issues, run with --fix flag")
    else:
        print("\nFixing permissions...")
        for error in errors:
            # Parse the error to get path and expected permissions
            if ":" in error:
                path_str = error.split(":")[0].strip()
                if "Shell script" in error:
                    path_str = path_str.replace("Shell script ", "")
                elif "Python script" in error:
                    path_str = path_str.replace("Python script ", "")
                elif "Directory" in error:
                    path_str = path_str.replace("Directory ", "")

                full_path = root_dir / path_str
                if full_path.exists():
                    if "expected 755" in error:
                        full_path.chmod(0o755)
                        print(f"  ✅ Fixed: {path_str}")
                    elif "expected 644" in error:
                        full_path.chmod(0o644)
                        print(f"  ✅ Fixed: {path_str}")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Check file permissions for AGET template')
    parser.add_argument('--fix', action='store_true', help='Fix permission issues')
    parser.add_argument('--path', type=str, default='.', help='Path to check (default: current directory)')
    args = parser.parse_args()

    root_dir = Path(args.path).resolve()

    if not root_dir.exists():
        print(f"❌ Error: Path {root_dir} does not exist")
        sys.exit(1)

    print(f"Checking file permissions in: {root_dir}")
    print("=" * 60)

    if args.fix:
        fix_permissions(root_dir, dry_run=False)
    else:
        errors, warnings = check_permissions(root_dir)

        if errors:
            print(f"❌ Found {len(errors)} permission errors:")
            for error in errors:
                print(f"  • {error}")
            print("\nRun with --fix to correct these issues")
            sys.exit(1)
        else:
            print("✅ All file permissions are correct!")

        if warnings:
            print(f"\n⚠️  {len(warnings)} warnings:")
            for warning in warnings:
                print(f"  • {warning}")

    sys.exit(0)

if __name__ == "__main__":
    main()