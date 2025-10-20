#!/usr/bin/env python3
"""
Sync Checker - Makes SYNC_WITH_AGET.md executable
Validates that fundamental standards are actually shared with AGET.
"""

import os
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

# Define what MUST be synchronized (from SYNC_WITH_AGET.md)
FUNDAMENTAL_FILES = {
    # Core patterns that define AGET
    "patterns/session/wake.py": "Core pattern - wake protocol",
    "patterns/session/wind_down.py": "Core pattern - wind down protocol",
    "patterns/session/sign_off.py": "Core pattern - sign off protocol",
}

FUNDAMENTAL_CONTENT = {
    # Mission must contain this exact string
    "MISSION": "Help software creators achieve their vision (with their linguistic AI collaborator)",
    # Pattern structure must have this function
    "PATTERN_STRUCTURE": "def apply_pattern(",
}

def check_fundamental_files() -> List[str]:
    """Check if fundamental files exist and match AGET."""
    issues = []
    aget_path = Path(__file__).parent.parent.parent / "aget-cli-agent-template"
    local_path = Path(__file__).parent.parent

    for file_path, description in FUNDAMENTAL_FILES.items():
        aget_file = aget_path / file_path
        local_file = local_path / file_path

        if not local_file.exists():
            # We don't have this fundamental file
            issues.append(f"Missing fundamental: {file_path} - {description}")
            continue

        if aget_file.exists():
            # Compare hashes
            with open(aget_file, 'rb') as f:
                aget_hash = hashlib.md5(f.read()).hexdigest()
            with open(local_file, 'rb') as f:
                local_hash = hashlib.md5(f.read()).hexdigest()

            if aget_hash != local_hash:
                issues.append(f"Diverged fundamental: {file_path}")

    return issues

def check_mission_alignment() -> List[str]:
    """Verify mission statement contains core commitment."""
    issues = []
    mission_files = [
        Path(__file__).parent.parent / "docs" / "MISSION.md",
        Path(__file__).parent.parent / "README.md",
    ]

    mission_found = False
    for mission_file in mission_files:
        if mission_file.exists():
            content = mission_file.read_text()
            if FUNDAMENTAL_CONTENT["MISSION"] in content:
                mission_found = True
                break

    if not mission_found:
        issues.append("Mission statement doesn't contain AGET's core mission")

    return issues

def check_experimental_freedom() -> List[str]:
    """Verify we're actually experimenting (not just copying)."""
    issues = []

    # Check if we have experiments
    workspace = Path(__file__).parent
    experiments = list(workspace.glob("experiment_*.py"))

    if len(experiments) == 0:
        issues.append("No experiments found - not living up to innovation lab purpose")

    return issues

def generate_sync_report() -> str:
    """Generate a report on sync status."""
    report = ["# Sync Status Report\n"]

    # Check fundamentals
    fundamental_issues = check_fundamental_files()
    if fundamental_issues:
        report.append("## ❌ Fundamental Standards Issues")
        for issue in fundamental_issues:
            report.append(f"- {issue}")
    else:
        report.append("## ✅ Fundamental Standards Aligned")

    # Check mission
    mission_issues = check_mission_alignment()
    if mission_issues:
        report.append("\n## ❌ Mission Alignment Issues")
        for issue in mission_issues:
            report.append(f"- {issue}")
    else:
        report.append("\n## ✅ Mission Aligned")

    # Check experiments
    experiment_issues = check_experimental_freedom()
    if experiment_issues:
        report.append("\n## ⚠️ Innovation Warnings")
        for issue in experiment_issues:
            report.append(f"- {issue}")
    else:
        report.append("\n## ✅ Innovation Active")

    return "\n".join(report)

def update_sync_status():
    """Update the SYNC_WITH_AGET.md file with current status."""
    sync_file = Path(__file__).parent.parent / "SYNC_WITH_AGET.md"

    if not sync_file.exists():
        print("❌ SYNC_WITH_AGET.md not found")
        return

    # Read current content
    content = sync_file.read_text()

    # Generate new status section
    status = generate_sync_report()

    # Update or append status
    marker = "## Current Sync Status"
    if marker in content:
        # Replace existing status
        parts = content.split(marker)
        new_content = parts[0] + marker + "\n\n" + status + "\n"
    else:
        # Append status
        new_content = content + f"\n{marker}\n\n{status}\n"

    # Write back
    sync_file.write_text(new_content)
    print("✅ Updated SYNC_WITH_AGET.md with current status")

def main():
    """Run sync checker."""
    print("🔍 Checking sync status with AGET...")

    report = generate_sync_report()
    print(report)

    if "--update" in sys.argv:
        update_sync_status()
    else:
        print("\nRun with --update to update SYNC_WITH_AGET.md")

    # Exit with error if fundamental issues
    if "❌" in report:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())