#!/usr/bin/env python3
"""
Migration Artifact Cleanup Pattern
Part of EP-11: Migration Artifact Cleanup Pattern

Detects and archives migration artifacts left over from transitions.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import argparse

class MigrationCleanup:
    """Clean up migration artifacts from CLAUDE.md to AGET transitions."""

    # Common migration artifact patterns
    ARTIFACT_PATTERNS = {
        'claude_backups': ['CLAUDE.md.backup', 'CLAUDE.md.original', 'CLAUDE.md.old'],
        'session_orphans': ['SESSION_*.md'],
        'old_configs': ['.claude_config', '.claude_settings'],
        'deprecated_scripts': ['claude_*.py', 'claude_*.sh'],
        'temp_migrations': ['*_migration_*.tmp', '*.migrate']
    }

    def __init__(self, root_path='.', dry_run=True):
        self.root_path = Path(root_path)
        self.dry_run = dry_run
        self.backup_dir = self.root_path / '.aget' / 'backups'
        self.artifacts_found = []

    def scan_for_artifacts(self):
        """Scan for migration artifacts."""
        for category, patterns in self.ARTIFACT_PATTERNS.items():
            for pattern in patterns:
                matches = list(self.root_path.glob(pattern))
                for match in matches:
                    if match.is_file():
                        self.artifacts_found.append({
                            'path': match,
                            'category': category,
                            'size': match.stat().st_size
                        })

        return self.artifacts_found

    def archive_artifacts(self):
        """Archive found artifacts to .aget/backups/."""
        if not self.artifacts_found:
            return []

        # Create backup directory structure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        migration_backup_dir = self.backup_dir / f'migration_{timestamp}'

        archived = []
        for artifact in self.artifacts_found:
            category_dir = migration_backup_dir / artifact['category']

            if not self.dry_run:
                category_dir.mkdir(parents=True, exist_ok=True)
                dest = category_dir / artifact['path'].name
                shutil.move(str(artifact['path']), str(dest))
                archived.append(str(dest))
            else:
                archived.append(f"Would archive: {artifact['path']} -> {category_dir}")

        # Create manifest
        if not self.dry_run and archived:
            manifest = migration_backup_dir / 'manifest.json'
            manifest_data = {
                'timestamp': timestamp,
                'artifacts': len(self.artifacts_found),
                'categories': list(set(a['category'] for a in self.artifacts_found)),
                'files': [str(a['path']) for a in self.artifacts_found]
            }
            manifest.write_text(json.dumps(manifest_data, indent=2))

        return archived

    def report(self):
        """Generate cleanup report."""
        if not self.artifacts_found:
            return "No migration artifacts found."

        report_lines = []
        if self.dry_run:
            report_lines.append("DRY RUN - No changes made")

        report_lines.append(f"\nFound {len(self.artifacts_found)} migration artifacts:")

        by_category = {}
        total_size = 0
        for artifact in self.artifacts_found:
            category = artifact['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(artifact)
            total_size += artifact['size']

        for category, items in by_category.items():
            report_lines.append(f"\n{category.replace('_', ' ').title()}:")
            for item in items:
                report_lines.append(f"  - {item['path'].name} ({item['size']} bytes)")

        report_lines.append(f"\nTotal size: {total_size:,} bytes")

        return '\n'.join(report_lines)


def apply_pattern(project_path: Path = None):
    """
    Apply the migration cleanup pattern.

    This function is called by `aget apply housekeeping/migration_cleanup`.
    """
    try:
        if project_path is None:
            project_path = Path.cwd()

        cleanup = MigrationCleanup(project_path, dry_run=True)

        print("🔍 Migration Artifact Cleanup")
        print("=" * 50)

        # Scan for artifacts
        cleanup.scan_for_artifacts()

        # Show report
        print(cleanup.report())

        if cleanup.artifacts_found:
            print("\n💡 Run with --no-dry-run to archive these artifacts")
            return {"status": "success", "artifacts_found": len(cleanup.artifacts_found)}
        else:
            return {"status": "success", "artifacts_found": 0}

    except Exception as e:
        print(f"❌ Error in migration cleanup: {e}")
        return {"status": "error", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Clean up AGET migration artifacts')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Preview changes without making them')
    parser.add_argument('--no-dry-run', action='store_false', dest='dry_run',
                        help='Actually perform the cleanup')
    parser.add_argument('--path', default='.',
                        help='Root path to scan (default: current directory)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')

    args = parser.parse_args()

    cleanup = MigrationCleanup(args.path, args.dry_run)

    # Scan for artifacts
    cleanup.scan_for_artifacts()

    if not args.quiet:
        print("🔍 Migration Artifact Cleanup")
        print("=" * 50)

    # Archive if not dry run
    archived = cleanup.archive_artifacts()

    # Report results
    if args.quiet:
        if cleanup.artifacts_found:
            print(f"Found {len(cleanup.artifacts_found)} artifacts")
    else:
        print(cleanup.report())

        if archived and not args.dry_run:
            print(f"\n✅ Archived to: {cleanup.backup_dir}")

    return 0 if not cleanup.artifacts_found else 1


if __name__ == '__main__':
    exit(main())