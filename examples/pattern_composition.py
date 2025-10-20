#!/usr/bin/env python3
"""
Pattern Composition Examples

Demonstrates how to combine multiple AGET patterns for complex workflows.
These examples show real-world usage of pattern combinations.
"""

import sys
import os
from pathlib import Path
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.session.wake import wake_protocol
from patterns.session.wind_down import wind_down_protocol
from patterns.session.sign_off import sign_off_protocol
from patterns.housekeeping.cleanup import cleanup_project
from patterns.housekeeping.doc_check import check_documentation
from patterns.meta.project_scanner import ProjectScanner


class PatternComposition:
    """Examples of combining patterns for workflows."""

    def morning_routine(self):
        """
        Morning Routine Workflow:
        1. Wake up and check status
        2. Validate configuration
        3. Check documentation quality
        """
        print("=" * 60)
        print("Morning Routine: Wake → Validate → Documentation Check")
        print("=" * 60)

        # Step 1: Wake up
        print("\n📍 Step 1: Wake Up Protocol")
        wake_result = wake_protocol()
        if not wake_result.get('success', False):
            print("⚠️  Wake protocol reported issues")

        # Step 2: Validate configuration
        print("\n📍 Step 2: Validate Configuration")
        from src.aget.commands.validate import ProjectValidator
        validator = ProjectValidator()
        is_valid = validator.validate_all()
        print(f"   Configuration valid: {is_valid}")
        if validator.warnings:
            print(f"   Warnings: {len(validator.warnings)}")

        # Step 3: Check documentation
        print("\n📍 Step 3: Documentation Check")
        doc_result = check_documentation()
        if doc_result:
            print(f"   Documentation grade: {doc_result.get('grade', 'N/A')}")
            if doc_result.get('issues'):
                print(f"   Issues found: {len(doc_result['issues'])}")

        print("\n✅ Morning routine complete!")

    def cleanup_workflow(self):
        """
        Cleanup Workflow:
        1. Run housekeeping cleanup
        2. Check for migration artifacts
        3. Save work
        """
        print("=" * 60)
        print("Cleanup Workflow: Housekeeping → Migration Check → Wind Down")
        print("=" * 60)

        # Step 1: Housekeeping
        print("\n📍 Step 1: Housekeeping Cleanup")
        cleanup_result = cleanup_project(dry_run=True)
        if cleanup_result:
            print(f"   Files to clean: {cleanup_result.get('total_files', 0)}")
            print(f"   Space to recover: {cleanup_result.get('total_size', 0)} bytes")

        # Step 2: Migration cleanup
        print("\n📍 Step 2: Migration Artifact Check")
        from patterns.housekeeping.migration_cleanup import MigrationCleanup
        migration_cleanup = MigrationCleanup(dry_run=True)
        artifacts = migration_cleanup.scan_for_artifacts()
        if artifacts:
            print(f"   Migration artifacts found: {len(artifacts)}")
        else:
            print("   No migration artifacts found")

        # Step 3: Wind down
        print("\n📍 Step 3: Wind Down Protocol")
        wind_down_result = wind_down_protocol()
        if wind_down_result.get('success', False):
            print(f"   Session saved: {wind_down_result.get('session_file', 'N/A')}")

        print("\n✅ Cleanup workflow complete!")

    def full_session_lifecycle(self):
        """
        Full Session Lifecycle:
        1. Wake up
        2. Do work (simulated)
        3. Wind down
        4. Sign off
        """
        print("=" * 60)
        print("Full Session: Wake → Work → Wind Down → Sign Off")
        print("=" * 60)

        # Step 1: Wake up
        print("\n📍 Step 1: Wake Up")
        wake_result = wake_protocol()
        session_number = wake_result.get('session_number', 0)
        print(f"   Session #{session_number} started")

        # Step 2: Simulate work
        print("\n📍 Step 2: Simulated Work")
        print("   Working...")
        time.sleep(1)  # Simulate work
        print("   Created 3 files (simulated)")
        print("   Modified 5 files (simulated)")

        # Step 3: Wind down
        print("\n📍 Step 3: Wind Down")
        wind_down_result = wind_down_protocol()
        if wind_down_result.get('success', False):
            print("   Changes saved and documented")

        # Step 4: Sign off
        print("\n📍 Step 4: Sign Off")
        sign_off_result = sign_off_protocol()
        if sign_off_result.get('success', False):
            print("   Signed off successfully")

        print(f"\n✅ Full session lifecycle complete (Session #{session_number})!")

    def multi_project_scan(self):
        """
        Multi-Project Management:
        1. Scan all projects
        2. Identify migration needs
        3. Generate reports
        """
        print("=" * 60)
        print("Multi-Project: Scan → Analyze → Report")
        print("=" * 60)

        # Step 1: Scan projects
        print("\n📍 Step 1: Scanning Projects")
        scanner = ProjectScanner("..")  # Scan parent directory
        scanner.scan_all_projects()

        print(f"   Found {scanner.summary['total_projects']} projects")
        print(f"   Migrated: {scanner.summary['migrated']}")
        print(f"   Partial: {scanner.summary['partial']}")
        print(f"   Not started: {scanner.summary['not_started']}")

        # Step 2: Analyze migration needs
        print("\n📍 Step 2: Analyzing Migration Needs")
        needs_migration = []
        for name, project in scanner.projects.items():
            if project['score'] < 60:
                needs_migration.append(name)

        if needs_migration:
            print(f"   Projects needing migration: {', '.join(needs_migration[:5])}")
        else:
            print("   All projects adequately migrated")

        # Step 3: Generate report
        print("\n📍 Step 3: Generating Report")
        report_file = scanner.save_report()
        print(f"   Report saved to: {report_file}")

        print("\n✅ Multi-project scan complete!")

    def development_workflow(self):
        """
        Development Workflow:
        1. Wake up
        2. Run tests
        3. Validate patterns
        4. Wind down
        """
        print("=" * 60)
        print("Development: Wake → Test → Validate → Wind Down")
        print("=" * 60)

        # Step 1: Wake up
        print("\n📍 Step 1: Wake Up")
        wake_protocol()

        # Step 2: Run pattern tests
        print("\n📍 Step 2: Running Pattern Tests")
        test_files = list(Path('tests').glob('test_*.py'))
        print(f"   Found {len(test_files)} test files")

        # Step 3: Validate patterns
        print("\n📍 Step 3: Validating Patterns")
        from src.aget.commands.validate import PatternValidator

        patterns_dir = Path('patterns')
        pattern_files = list(patterns_dir.rglob('*.py'))
        valid_count = 0

        for pattern_file in pattern_files[:5]:  # Check first 5
            if pattern_file.name.startswith('__'):
                continue
            validator = PatternValidator(pattern_file)
            if validator.validate():
                valid_count += 1

        print(f"   Validated {valid_count} patterns")

        # Step 4: Wind down
        print("\n📍 Step 4: Wind Down")
        wind_down_protocol()

        print("\n✅ Development workflow complete!")


def main():
    """Run example compositions."""
    composer = PatternComposition()

    print("\n🎯 PATTERN COMPOSITION EXAMPLES\n")

    # Choose which example to run
    examples = {
        '1': ('Morning Routine', composer.morning_routine),
        '2': ('Cleanup Workflow', composer.cleanup_workflow),
        '3': ('Full Session Lifecycle', composer.full_session_lifecycle),
        '4': ('Multi-Project Scan', composer.multi_project_scan),
        '5': ('Development Workflow', composer.development_workflow),
    }

    print("Available examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")

    choice = input("\nSelect example (1-5) or 'all' for all examples: ").strip()

    if choice == 'all':
        for name, func in examples.values():
            print(f"\n{'='*60}")
            print(f"Running: {name}")
            print('='*60)
            try:
                func()
            except Exception as e:
                print(f"❌ Error in {name}: {e}")
            time.sleep(1)
    elif choice in examples:
        name, func = examples[choice]
        try:
            func()
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()