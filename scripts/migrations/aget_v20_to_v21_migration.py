#!/usr/bin/env python3
"""
AGET v2.0 to v2.1 Migration Script
Automates the upgrade from v2.0 to v2.1 with aget_ prefix convention

Usage: python3 aget_v20_to_v21_migration.py [--dry-run] [--verbose]
"""

import os
import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class V21Migrator:
    """Handles migration from AGET v2.0 to v2.1"""

    # Patterns that need aget_ prefix in v2.1
    PATTERNS_TO_RENAME = {
        'session/wake_up.py': 'session/aget_wake_up.py',
        'session/wind_down.py': 'session/aget_wind_down.py',
        'session/wind_down_safe.py': 'session/aget_wind_down_safe.py',
        'housekeeping/cleanup.py': 'housekeeping/aget_cleanup.py',
        'housekeeping/spring_clean.py': 'housekeeping/aget_spring_clean.py',
        'documentation/smart_reader.py': 'documentation/aget_smart_reader.py',
        'bridge/extract_output.py': 'bridge/aget_extract_output.py',
        'meta/project_scanner.py': 'meta/aget_project_scanner.py',
    }

    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.report = []
        self.errors = []

    def log(self, message: str, level: str = "INFO"):
        """Log message with level"""
        if level == "ERROR":
            self.errors.append(message)
            print(f"❌ {message}", file=sys.stderr)
        else:
            self.report.append(message)
            if self.verbose or level == "SUCCESS":
                icon = "✅" if level == "SUCCESS" else "ℹ️"
                print(f"{icon} {message}")

    def check_v20_compliance(self, base_path: Path) -> bool:
        """Verify agent is at v2.0 before migration"""
        version_file = base_path / '.aget' / 'version.json'

        # Check version file exists
        if not version_file.exists():
            self.log("No .aget/version.json found", "ERROR")
            return False

        # Check version is 2.0.0
        try:
            with open(version_file) as f:
                version_data = json.load(f)
                current_version = version_data.get('aget_version', '')

                # Accept both 2.0.0 and 2.0.0-alpha
                if not current_version.startswith("2.0.0"):
                    self.log(f"Version is {current_version}, not 2.0.0 or 2.0.0-alpha", "ERROR")
                    return False
        except Exception as e:
            self.log(f"Error reading version: {e}", "ERROR")
            return False

        # Check required directories
        required_dirs = [
            base_path / '.aget' / 'patterns',
            base_path / 'sessions',
            base_path / 'workspace',
            base_path / 'products'
        ]

        for dir_path in required_dirs:
            if not dir_path.exists():
                self.log(f"Missing required directory: {dir_path.name}", "ERROR")
                return False

        self.log("v2.0 compliance verified", "SUCCESS")
        return True

    def backup_current_state(self, base_path: Path) -> bool:
        """Create backup before migration"""
        if self.dry_run:
            self.log("Would create backup at .aget.backup-v20", "INFO")
            return True

        backup_path = base_path / '.aget.backup-v20'

        # Remove old backup if exists
        if backup_path.exists():
            shutil.rmtree(backup_path)

        try:
            shutil.copytree(base_path / '.aget', backup_path)
            self.log(f"Backup created at {backup_path}", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Backup failed: {e}", "ERROR")
            return False

    def rename_patterns(self, base_path: Path) -> List[Tuple[str, str]]:
        """Rename patterns to include aget_ prefix"""
        patterns_dir = base_path / '.aget' / 'patterns'
        renamed = []

        for old_path, new_path in self.PATTERNS_TO_RENAME.items():
            old_file = patterns_dir / old_path
            new_file = patterns_dir / new_path

            if old_file.exists():
                if self.dry_run:
                    self.log(f"Would rename: {old_path} → {new_path}", "INFO")
                else:
                    try:
                        old_file.rename(new_file)
                        self.log(f"Renamed: {old_path} → {new_path}", "SUCCESS")
                        renamed.append((old_path, new_path))
                    except Exception as e:
                        self.log(f"Failed to rename {old_path}: {e}", "ERROR")
            else:
                self.log(f"Pattern not found (skipping): {old_path}", "INFO")

        return renamed

    def update_version_file(self, base_path: Path) -> bool:
        """Update version.json to v2.1.0"""
        version_file = base_path / '.aget' / 'version.json'

        try:
            with open(version_file) as f:
                version_data = json.load(f)

            version_data['aget_version'] = '2.1.0'
            version_data['migrated_from_v20'] = datetime.now().isoformat()
            version_data['migration_type'] = 'automated'

            if self.dry_run:
                self.log("Would update version.json to 2.1.0", "INFO")
            else:
                with open(version_file, 'w') as f:
                    json.dump(version_data, f, indent=2)
                self.log("Updated version.json to 2.1.0", "SUCCESS")

            return True
        except Exception as e:
            self.log(f"Failed to update version: {e}", "ERROR")
            return False

    def update_claude_md(self, base_path: Path, renamed_patterns: List[Tuple[str, str]]) -> bool:
        """Update CLAUDE.md or AGENTS.md with new pattern names"""
        # Check for CLAUDE.md or AGENTS.md
        claude_file = base_path / 'CLAUDE.md'
        if not claude_file.exists():
            claude_file = base_path / 'AGENTS.md'
            if not claude_file.exists():
                self.log("No CLAUDE.md or AGENTS.md found to update", "INFO")
                return True

        if self.dry_run:
            self.log(f"Would update {claude_file.name} with new pattern names", "INFO")
            return True

        try:
            with open(claude_file) as f:
                content = f.read()

            # Replace old pattern names with new ones
            original_content = content
            for old_name, new_name in renamed_patterns:
                old_ref = old_name.split('/')[-1]  # Get filename only
                new_ref = new_name.split('/')[-1]
                content = content.replace(old_ref, new_ref)

            # Add v2.1 migration note if content changed
            if content != original_content:
                migration_note = f"\n\n<!-- Migrated to v2.1.0 on {datetime.now().strftime('%Y-%m-%d')} -->\n"
                if migration_note not in content:
                    content += migration_note

                with open(claude_file, 'w') as f:
                    f.write(content)

                self.log(f"Updated {claude_file.name} with v2.1 pattern names", "SUCCESS")
            else:
                self.log("No pattern references needed updating", "INFO")

            return True
        except Exception as e:
            self.log(f"Failed to update documentation: {e}", "ERROR")
            return False

    def create_migration_record(self, base_path: Path) -> bool:
        """Document the migration in .aget/evolution/"""
        if self.dry_run:
            self.log("Would create migration record", "INFO")
            return True

        evolution_dir = base_path / '.aget' / 'evolution'
        evolution_dir.mkdir(exist_ok=True)

        record_file = evolution_dir / f"v21_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        content = f"""# v2.0 to v2.1 Migration Record

## Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
## Migration Type: Automated

## Changes Applied:

### Pattern Renames (aget_ prefix):
{chr(10).join(f"- {old} → {new}" for old, new in self.PATTERNS_TO_RENAME.items())}

### Version Update:
- From: 2.0.0
- To: 2.1.0

### Status:
- Errors: {len(self.errors)}
- Warnings: 0

## Report:
{chr(10).join(f"- {item}" for item in self.report)}

## Errors:
{chr(10).join(f"- {error}" for error in self.errors) if self.errors else "None"}

---
*Automated migration using aget_v20_to_v21_migration.py*
"""

        try:
            with open(record_file, 'w') as f:
                f.write(content)
            self.log(f"Migration record created: {record_file.name}", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"Failed to create record: {e}", "ERROR")
            return False

    def migrate(self, base_path: Path = None) -> bool:
        """Execute the full migration"""
        if base_path is None:
            base_path = Path.cwd()

        print(f"\n{'DRY RUN: ' if self.dry_run else ''}Migrating {base_path} from v2.0 to v2.1...\n")

        # Step 1: Check v2.0 compliance
        if not self.check_v20_compliance(base_path):
            print("\n❌ Agent is not v2.0 compliant. Please migrate to v2.0 first.")
            return False

        # Step 2: Backup
        if not self.backup_current_state(base_path):
            print("\n❌ Backup failed. Aborting migration.")
            return False

        # Step 3: Rename patterns
        renamed = self.rename_patterns(base_path)

        # Step 4: Update version
        if not self.update_version_file(base_path):
            print("\n⚠️ Version update failed but continuing...")

        # Step 5: Update documentation
        if not self.update_claude_md(base_path, renamed):
            print("\n⚠️ Documentation update failed but continuing...")

        # Step 6: Create migration record
        if not self.create_migration_record(base_path):
            print("\n⚠️ Record creation failed but migration complete")

        # Summary
        print(f"\n{'='*50}")
        if self.errors:
            print(f"⚠️ Migration completed with {len(self.errors)} errors")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("✅ Migration completed successfully!")

        print(f"\n📊 Summary:")
        print(f"  - Patterns renamed: {len(renamed)}")
        print(f"  - Version updated: {'Yes' if not self.dry_run else 'Would update'}")
        print(f"  - Backup created: {'Yes' if not self.dry_run else 'Would create'}")

        if self.dry_run:
            print("\n💡 This was a dry run. Use without --dry-run to apply changes.")

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(description='Migrate AGET agents from v2.0 to v2.1')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed progress')
    parser.add_argument('--path', type=Path, default=None,
                       help='Path to agent directory (default: current directory)')

    args = parser.parse_args()

    migrator = V21Migrator(dry_run=args.dry_run, verbose=args.verbose)
    success = migrator.migrate(args.path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()