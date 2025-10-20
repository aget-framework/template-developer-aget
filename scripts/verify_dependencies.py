#!/usr/bin/env python3
"""
Verify AGET is self-contained per ARCH-001.
Part of the self-contained architecture implementation.
"""

import json
import sys
import subprocess
from pathlib import Path


def check_dependencies_manifest():
    """Check if dependencies.json exists and is valid."""
    dep_file = Path(".aget/dependencies.json")
    if not dep_file.exists():
        print("❌ Missing .aget/dependencies.json")
        return False

    try:
        with open(dep_file) as f:
            deps = json.load(f)
        print("✅ dependencies.json found and valid")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ dependencies.json is invalid JSON: {e}")
        return False


def check_no_external_paths():
    """Check for hardcoded external paths in Python files."""
    has_external = False

    # Patterns to check for
    patterns = ["/Users/", "C:\\Users\\", "C:/Users/"]

    # Files to exclude from check
    exclude_files = {"security_check.py", "verify_dependencies.py"}

    for p in Path(".").rglob("*.py"):
        # Skip excluded files
        if p.name in exclude_files:
            continue

        # Skip test files
        if "test" in str(p):
            continue

        try:
            content = p.read_text()
            for pattern in patterns:
                if pattern in content:
                    print(f"❌ External path '{pattern}' in {p}")
                    has_external = True
                    break
        except Exception as e:
            print(f"⚠️  Could not read {p}: {e}")

    if not has_external:
        print("✅ No external paths in Python files")

    return not has_external


def check_required_scripts():
    """Check if required scripts exist."""
    required = [
        "scripts/aget_session_protocol.py",
        "scripts/install_pattern.py",
        "scripts/verify_dependencies.py"
    ]

    all_present = True
    for script in required:
        if Path(script).exists():
            print(f"✅ {script} exists")
        else:
            print(f"❌ {script} missing")
            all_present = False

    return all_present


def check_pattern_installation():
    """Check if patterns can be installed."""
    try:
        result = subprocess.run(
            ["python3", "scripts/install_pattern.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ install_pattern.py is functional")
            return True
        else:
            print(f"❌ install_pattern.py failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Could not run install_pattern.py: {e}")
        return False


def check_arch_compliance():
    """Check for ARCH-001 documentation."""
    arch_file = Path("docs/adr/ARCH-001-SELF-CONTAINED-PROJECTS.md")
    if arch_file.exists():
        print(f"✅ {arch_file} exists")
        return True
    else:
        print(f"⚠️  {arch_file} not found (documentation missing)")
        # Not a failure - just documentation
        return True


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("ARCH-001 SELF-CONTAINED VERIFICATION")
    print("=" * 60)
    print()

    checks = [
        ("Dependencies manifest", check_dependencies_manifest),
        ("No external paths", check_no_external_paths),
        ("Required scripts", check_required_scripts),
        ("Pattern installation", check_pattern_installation),
        ("Architecture documentation", check_arch_compliance)
    ]

    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        print("-" * 40)
        results.append(check_func())

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ All {total} checks passed - AGET is self-contained")
        return 0
    else:
        print(f"❌ {total - passed} of {total} checks failed")
        print("\nTo fix:")
        print("1. Run: python3 scripts/install_pattern.py")
        print("2. Check for hardcoded paths in Python files")
        print("3. Ensure all required scripts are present")
        return 1


if __name__ == "__main__":
    sys.exit(main())