#!/usr/bin/env python3
"""
Install patterns from external sources to make AGET self-contained.
Follows the self-contained architecture principle: each AGET has its own copies.
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime


def load_dependencies():
    """Load the dependencies manifest."""
    dep_file = Path(".aget/dependencies.json")
    if not dep_file.exists():
        print("❌ No dependencies.json found")
        return None

    with open(dep_file) as f:
        return json.load(f)


def install_pattern(pattern_name, source_path=None):
    """
    Install a pattern by copying it locally.

    Args:
        pattern_name: Name like "documentation/smart_reader.py"
        source_path: Override source path (optional)
    """
    deps = load_dependencies()
    if not deps:
        return False

    # Find pattern in manifest
    pattern_info = None
    for p in deps.get("required_patterns", []) + deps.get("optional_patterns", []):
        if p["name"] == pattern_name:
            pattern_info = p
            break

    if not pattern_info:
        print(f"❌ Pattern '{pattern_name}' not found in dependencies.json")
        return False

    # Determine source
    source = Path(source_path or pattern_info.get("source", ""))
    if not source.exists():
        print(f"❌ Source not found: {source}")
        print(f"   Pattern status: {pattern_info.get('status', 'unknown')}")
        return False

    # Determine destination
    dest = Path("patterns") / pattern_name
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Copy the pattern
    try:
        shutil.copy2(source, dest)
        print(f"✅ Installed: {pattern_name}")
        print(f"   From: {source}")
        print(f"   To: {dest}")

        # Update manifest
        pattern_info["status"] = "installed"
        pattern_info["installed_date"] = datetime.now().isoformat()
        pattern_info["installed_from"] = str(source)

        with open(".aget/dependencies.json", "w") as f:
            json.dump(deps, f, indent=2)

        return True

    except Exception as e:
        print(f"❌ Failed to install: {e}")
        return False


def install_all_required():
    """Install all required patterns that are missing."""
    deps = load_dependencies()
    if not deps:
        return

    installed = 0
    failed = 0

    for pattern in deps.get("required_patterns", []):
        if pattern.get("status") != "installed":
            print(f"\n📦 Installing {pattern['name']}...")
            if install_pattern(pattern["name"]):
                installed += 1
            else:
                failed += 1

    print(f"\n📊 Summary: {installed} installed, {failed} failed")

    if failed > 0:
        print("\n⚠️  Some patterns failed to install.")
        print("   This AGET may not function correctly.")
        print("   Run 'python3 scripts/verify_dependencies.py' to check.")
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        print("Installing all required patterns...")
        install_all_required()
    elif sys.argv[1] == "--help":
        print("Usage:")
        print("  python3 scripts/install_pattern.py                    # Install all required")
        print("  python3 scripts/install_pattern.py <pattern_name>     # Install specific")
        print("  python3 scripts/install_pattern.py <name> <source>    # Install from path")
    elif len(sys.argv) == 2:
        install_pattern(sys.argv[1])
    elif len(sys.argv) == 3:
        install_pattern(sys.argv[1], sys.argv[2])
    else:
        print("❌ Too many arguments. Use --help for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()