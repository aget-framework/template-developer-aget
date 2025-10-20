#!/usr/bin/env python3
"""
Experiment 001: Pattern Validator
Goal: Create a tool that validates AGET patterns meet quality standards
Status: Active experiment
Started: 2025-09-25

This could graduate to AGET if successful, or remain a private QA tool.
"""

import os
import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def validate_pattern(pattern_file: Path) -> Tuple[bool, List[str]]:
    """Validate a single pattern file meets AGET standards."""
    issues = []

    # Check file exists
    if not pattern_file.exists():
        return False, [f"File not found: {pattern_file}"]

    # Read and parse the Python file
    try:
        with open(pattern_file, 'r') as f:
            content = f.read()
            tree = ast.parse(content)
    except SyntaxError as e:
        return False, [f"Syntax error: {e}"]

    # Check for required apply_pattern function
    has_apply_pattern = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'apply_pattern':
            has_apply_pattern = True
            # Check it returns a dict
            # This is a simple check - could be more sophisticated
            break

    if not has_apply_pattern:
        issues.append("Missing required apply_pattern() function")

    # Check for docstring
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
        docstring = tree.body[0].value.s
        if len(docstring) < 20:
            issues.append("Docstring too short (should explain pattern purpose)")
    else:
        issues.append("Missing module docstring")

    # Check for proper error handling
    has_try_except = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            has_try_except = True
            break

    if not has_try_except:
        issues.append("No error handling (patterns should handle failures gracefully)")

    return len(issues) == 0, issues

def scan_patterns(pattern_dir: Path) -> Dict[str, Tuple[bool, List[str]]]:
    """Scan all patterns in a directory."""
    results = {}

    for pattern_file in pattern_dir.rglob("*.py"):
        if "__pycache__" in str(pattern_file):
            continue
        if pattern_file.name == "__init__.py":
            continue

        relative_path = pattern_file.relative_to(pattern_dir)
        results[str(relative_path)] = validate_pattern(pattern_file)

    return results

def main():
    """Run pattern validation experiment."""
    print("🧪 AGET Pattern Validator - Experiment 001")
    print("=" * 50)

    # Look for patterns directory
    if len(sys.argv) > 1:
        pattern_dir = Path(sys.argv[1])
    else:
        # Try to find AGET patterns
        pattern_dir = Path(__file__).parent.parent.parent / "aget-cli-agent-template" / "patterns"

    if not pattern_dir.exists():
        print(f"❌ Pattern directory not found: {pattern_dir}")
        return 1

    print(f"📁 Scanning: {pattern_dir}")
    print()

    results = scan_patterns(pattern_dir)

    # Report results
    passed = 0
    failed = 0

    for pattern, (is_valid, issues) in sorted(results.items()):
        if is_valid:
            print(f"✅ {pattern}")
            passed += 1
        else:
            print(f"❌ {pattern}")
            for issue in issues:
                print(f"   - {issue}")
            failed += 1

    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")

    # This experiment's learning
    if failed > 0:
        print("\n💡 Learning: AGET patterns need better validation")
        print("   Consider adding this validator to AGET itself")
    else:
        print("\n💡 Learning: AGET patterns are well-structured")
        print("   Current standards are working")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())