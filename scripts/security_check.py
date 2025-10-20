#!/usr/bin/env python3
"""
Security check before making repository public
"""

import re
from pathlib import Path

# Patterns that might indicate secrets
SECRET_PATTERNS = [
    (r'(?i)(api[_\s-]?key|apikey)[\s:=]+["\']?[a-zA-Z0-9]{20,}', 'API Key'),
    (r'(?i)(secret|token|password)[\s:=]+["\']?[a-zA-Z0-9]{10,}', 'Secret/Token'),
    (r'sk-[a-zA-Z0-9]{48}', 'OpenAI API Key'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Token'),
    (r'(?i)bearer\s+[a-zA-Z0-9\-._~+/]{20,}', 'Bearer Token'),
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'Email Address'),
    (r'/Users/[a-zA-Z]+/', 'User Path'),
    (r'/home/[a-zA-Z]+/', 'Home Path'),
]

def scan_file(filepath):
    """Scan a single file for potential secrets"""
    issues = []
    try:
        content = filepath.read_text()
        for line_num, line in enumerate(content.splitlines(), 1):
            # Skip example/documentation lines
            if any(indicator in line.lower() for indicator in ['example', 'you:', 'agent:']):
                continue

            for pattern, desc in SECRET_PATTERNS:
                if re.search(pattern, line):
                    # Skip generic user paths in examples
                    if desc == 'User Path' and '/Users/you/' in line:
                        continue
                    issues.append(f"{filepath}:{line_num} - Potential {desc}")
    except Exception:
        pass  # Skip binary files
    return issues

def main():
    """Run security scan"""
    print("🔍 Security Check - Scanning for sensitive data...\n")

    # Skip these directories
    skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'SESSION_NOTES'}

    # Skip files matching .gitignore patterns
    skip_patterns = ['.aider*', '*.log', '*.pyc', '.DS_Store']

    all_issues = []
    for filepath in Path('.').rglob('*'):
        if filepath.is_file():
            # Skip if in ignored directory
            if any(skip in filepath.parts for skip in skip_dirs):
                continue
            # Skip this script and test files
            if filepath.name == 'security_check.py' or 'test' in filepath.name:
                continue
            # Skip files matching gitignore patterns
            if any(filepath.match(pattern) for pattern in skip_patterns):
                continue

            issues = scan_file(filepath)
            all_issues.extend(issues)

    if all_issues:
        print("⚠️  FOUND POTENTIAL ISSUES:\n")
        for issue in all_issues[:20]:  # Show first 20
            print(f"  {issue}")
        if len(all_issues) > 20:
            print(f"\n  ... and {len(all_issues) - 20} more")
        print("\n❌ Review these before going public!")
        return 1
    else:
        print("✅ No obvious secrets detected")
        print("✅ Safe to make repository public")
        return 0

if __name__ == '__main__':
    exit(main())