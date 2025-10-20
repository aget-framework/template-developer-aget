#!/usr/bin/env python3
"""
organize_docs.py - Clean up documentation files in AGET repositories

This pattern implements the documentation organization standard from
docs/DOCUMENTATION_STANDARDS.md#file-organization-standards

Usage:
    python3 organize_docs.py --dry-run  # Show what would be moved
    python3 organize_docs.py --execute  # Actually move files
    python3 organize_docs.py --rollback # Undo the last organization
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# File organization rules based on DOCUMENTATION_STANDARDS.md
ORGANIZATION_RULES = {
    'sessions': {
        'patterns': ['SESSION_*.md', 'CHECKPOINT_*.md'],
        'target': 'sessions',
        'description': 'Session and checkpoint files'
    },
    'planning': {
        'patterns': ['*_STATUS.md', '*_PLAN.md', '*_REPORT.md', '*_ANALYSIS.md',
                    '*_CHECKLIST.md', '*_PROPOSAL.md', '*_READINESS*.md'],
        'target': 'docs/planning',
        'description': 'Planning and status documents'
    },
    'vision': {
        'patterns': ['VISION_*.md', 'STRATEGY_*.md', 'FUTURE_*.md',
                    'USERS.md', 'WHATS_NEW.md', 'WHEN_TO_*.md'],
        'target': 'vision',
        'description': 'Vision and strategy documents'
    },
    'development': {
        'patterns': ['LESSONS_*.md', 'BUG_*.md', 'SYNC_*.md',
                    'CONTROLLED_*.md', 'ADVANCED_*.md'],
        'target': '.aget/evolution',
        'description': 'Development artifacts'
    },
    'architecture': {
        'patterns': ['ARCHITECTURE.md', 'CHARTER.md', 'MISSION.md',
                    'GOVERNANCE_*.md', 'AGENTS_AGET*.md'],
        'target': 'docs',
        'description': 'Architecture and governance'
    },
    'releases': {
        'patterns': ['RELEASE_NOTES*.md', 'ROADMAP*.md'],
        'target': 'docs/releases',
        'description': 'Release documentation'
    }
}

# Files that should always stay in root
KEEP_IN_ROOT = [
    'README.md',
    'CHANGELOG.md',
    'LICENSE',
    'LICENSE.md',
    'CONTRIBUTING.md',
    'SECURITY.md',
    'AGENTS.md',
    'CLAUDE.md',
    'PREREQUISITES.md',
    'UPGRADING.md'
]

class DocumentOrganizer:
    def __init__(self, root_path: Path = None):
        self.root = Path(root_path) if root_path else Path.cwd()
        self.manifest_file = self.root / '.aget' / 'organization_manifest.json'
        self.backup_dir = self.root / '.aget' / 'backups' / 'doc_organization'

    def scan_files(self) -> Dict[str, List[Path]]:
        """Scan root directory and categorize files"""
        categorized = {
            'keep': [],
            'move': []
        }

        # Get all .md files in root
        md_files = list(self.root.glob('*.md'))

        for file in md_files:
            if file.name in KEEP_IN_ROOT:
                categorized['keep'].append(file)
            else:
                categorized['move'].append(file)

        return categorized

    def determine_target(self, file: Path) -> Tuple[str, Path]:
        """Determine where a file should be moved"""
        from fnmatch import fnmatch

        for category, rules in ORGANIZATION_RULES.items():
            for pattern in rules['patterns']:
                if fnmatch(file.name, pattern):
                    target_dir = self.root / rules['target']
                    return category, target_dir / file.name

        # Default to docs/misc if no pattern matches
        return 'misc', self.root / 'docs' / 'misc' / file.name

    def create_manifest(self, moves: List[Dict]) -> Path:
        """Create a manifest of all moves for rollback"""
        self.manifest_file.parent.mkdir(parents=True, exist_ok=True)

        manifest = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'moves': moves
        }

        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        return self.manifest_file

    def backup_file(self, file: Path) -> Path:
        """Create a backup of a file before moving"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = self.backup_dir / file.name
        shutil.copy2(file, backup_path)
        return backup_path

    def execute_moves(self, dry_run: bool = True) -> Dict:
        """Execute the file organization"""
        categorized = self.scan_files()
        moves = []

        print(f"\n📊 Found {len(categorized['keep'])} files to keep in root")
        print(f"📦 Found {len(categorized['move'])} files to organize\n")

        if not categorized['move']:
            print("✅ Root directory is already clean!")
            return {'moved': 0, 'kept': len(categorized['keep'])}

        print("Files to keep in root:")
        for file in categorized['keep']:
            print(f"  ✅ {file.name}")

        print("\nFiles to organize:")
        for file in categorized['move']:
            category, target = self.determine_target(file)
            moves.append({
                'source': str(file),
                'target': str(target),
                'category': category
            })

            status = "[DRY RUN]" if dry_run else "[MOVING]"
            print(f"  {status} {file.name} → {target.parent.relative_to(self.root)}/")

            if not dry_run:
                # Create target directory
                target.parent.mkdir(parents=True, exist_ok=True)

                # Backup file
                self.backup_file(file)

                # Move file
                shutil.move(str(file), str(target))

        if not dry_run:
            # Create manifest for rollback
            self.create_manifest(moves)
            print(f"\n✅ Moved {len(moves)} files")
            print(f"📝 Manifest saved to {self.manifest_file.relative_to(self.root)}")
        else:
            print(f"\n🔍 Dry run complete. Would move {len(moves)} files")
            print("   Run with --execute to perform the organization")

        return {
            'moved': len(moves),
            'kept': len(categorized['keep']),
            'manifest': str(self.manifest_file) if not dry_run else None
        }

    def rollback(self) -> bool:
        """Rollback the last organization"""
        if not self.manifest_file.exists():
            print("❌ No manifest found. Nothing to rollback.")
            return False

        with open(self.manifest_file, 'r') as f:
            manifest = json.load(f)

        print(f"🔄 Rolling back {len(manifest['moves'])} moves from {manifest['timestamp']}")

        for move in manifest['moves']:
            source = Path(move['target'])
            target = Path(move['source'])

            if source.exists():
                print(f"  ↩️  {source.relative_to(self.root)} → {target.name}")
                shutil.move(str(source), str(target))
            else:
                print(f"  ⚠️  {source.relative_to(self.root)} not found, skipping")

        # Remove manifest after successful rollback
        self.manifest_file.unlink()
        print("✅ Rollback complete")
        return True

def main():
    parser = argparse.ArgumentParser(
        description='Organize documentation files in AGET repositories'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be moved without actually moving'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually move the files'
    )
    parser.add_argument(
        '--rollback',
        action='store_true',
        help='Undo the last organization'
    )
    parser.add_argument(
        '--path',
        type=str,
        help='Path to repository root (default: current directory)'
    )

    args = parser.parse_args()

    # Validate arguments
    if sum([args.dry_run, args.execute, args.rollback]) != 1:
        print("❌ Please specify exactly one of: --dry-run, --execute, or --rollback")
        sys.exit(1)

    organizer = DocumentOrganizer(args.path)

    print("🧹 AGET Documentation Organizer")
    print(f"📁 Working in: {organizer.root}\n")

    if args.rollback:
        success = organizer.rollback()
        sys.exit(0 if success else 1)
    else:
        result = organizer.execute_moves(dry_run=args.dry_run)

        if args.execute:
            print("\n📋 Next steps:")
            print("1. Update any broken links in remaining files")
            print("2. Test that documentation is still accessible")
            print("3. Commit changes with message: 'docs: Organize files per DOCUMENTATION_STANDARDS.md'")
            print("4. If issues arise, run: python3 organize_docs.py --rollback")

if __name__ == '__main__':
    main()