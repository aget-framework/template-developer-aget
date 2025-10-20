#!/usr/bin/env python3
"""
Pattern Version Bump Tool - v2.3 Gate A2

Bumps semantic version of patterns in the version registry.
Supports major, minor, and patch version increments.
"""

import argparse
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple


class PatternVersionBumper:
    """Manage pattern version bumps."""

    def __init__(self, registry_path: Path = None):
        self.project_root = Path.cwd()
        self.registry_path = registry_path or self.project_root / ".aget/patterns/versions.yaml"
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load version registry."""
        if not self.registry_path.exists():
            print(f"ERROR: Registry not found: {self.registry_path}")
            sys.exit(1)

        with open(self.registry_path, 'r') as f:
            return yaml.safe_load(f)

    def _save_registry(self):
        """Save version registry."""
        with open(self.registry_path, 'w') as f:
            yaml.dump(self.registry, f, default_flow_style=False, sort_keys=False)

    def _parse_version(self, version_str: str) -> Tuple[int, int, int]:
        """Parse semantic version string."""
        try:
            parts = version_str.split('.')
            if len(parts) != 3:
                raise ValueError
            return tuple(int(p) for p in parts)
        except (ValueError, AttributeError):
            print(f"ERROR: Invalid version format: {version_str}")
            sys.exit(1)

    def _format_version(self, major: int, minor: int, patch: int) -> str:
        """Format semantic version tuple."""
        return f"{major}.{minor}.{patch}"

    def bump_version(self, pattern_name: str, bump_type: str, breaking_change: str = None) -> str:
        """Bump pattern version."""
        # Validate pattern exists
        if pattern_name not in self.registry['patterns']:
            print(f"ERROR: Pattern not found: {pattern_name}")
            print(f"Available patterns:")
            for p in sorted(self.registry['patterns'].keys()):
                print(f"  - {p}")
            sys.exit(1)

        pattern = self.registry['patterns'][pattern_name]
        current_version = pattern['version']
        major, minor, patch = self._parse_version(current_version)

        # Bump version based on type
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'patch':
            patch += 1
        else:
            print(f"ERROR: Invalid bump type: {bump_type}")
            print("Valid types: major, minor, patch")
            sys.exit(1)

        new_version = self._format_version(major, minor, patch)

        # Update registry
        pattern['version'] = new_version
        pattern['last_modified'] = datetime.now().strftime("%Y-%m-%d")

        # Add breaking change if major bump
        if bump_type == 'major':
            if not breaking_change:
                print("ERROR: Major version bump requires --breaking-change description")
                sys.exit(1)
            if 'breaking_changes' not in pattern:
                pattern['breaking_changes'] = []
            pattern['breaking_changes'].append({
                'version': new_version,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'description': breaking_change
            })

        # Update metadata
        self.registry['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")

        self._save_registry()

        return new_version

    def show_version(self, pattern_name: str):
        """Show current pattern version."""
        if pattern_name not in self.registry['patterns']:
            print(f"ERROR: Pattern not found: {pattern_name}")
            sys.exit(1)

        pattern = self.registry['patterns'][pattern_name]
        print(f"Pattern: {pattern_name}")
        print(f"Version: {pattern['version']}")
        print(f"Category: {pattern['category']}")
        print(f"File: {pattern['file']}")
        print(f"Description: {pattern['description']}")
        print(f"Last Modified: {pattern['last_modified']}")

        if pattern.get('breaking_changes'):
            print("\nBreaking Changes:")
            for change in pattern['breaking_changes']:
                print(f"  {change['version']} ({change['date']}): {change['description']}")

    def list_patterns(self):
        """List all patterns with versions."""
        print("Pattern Version Registry")
        print("=" * 70)
        print()

        by_category = {}
        for name, pattern in self.registry['patterns'].items():
            category = pattern['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((name, pattern))

        for category in sorted(by_category.keys()):
            print(f"{category}:")
            for name, pattern in sorted(by_category[category]):
                version = pattern['version']
                desc = pattern['description']
                print(f"  {name:40} v{version:10} {desc}")
            print()

        print(f"Total patterns: {len(self.registry['patterns'])}")


def main():
    """Run pattern version bumper."""
    parser = argparse.ArgumentParser(
        description="Bump pattern versions in registry"
    )
    parser.add_argument(
        'pattern',
        nargs='?',
        help='Pattern name (e.g., github/create_issue)'
    )
    parser.add_argument(
        '--major',
        action='store_const',
        const='major',
        dest='bump_type',
        help='Bump major version (breaking change)'
    )
    parser.add_argument(
        '--minor',
        action='store_const',
        const='minor',
        dest='bump_type',
        help='Bump minor version (new features)'
    )
    parser.add_argument(
        '--patch',
        action='store_const',
        const='patch',
        dest='bump_type',
        help='Bump patch version (bug fixes)'
    )
    parser.add_argument(
        '--breaking-change',
        type=str,
        help='Description of breaking change (required for --major)'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Show pattern version info'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all patterns'
    )

    args = parser.parse_args()

    bumper = PatternVersionBumper()

    if args.list:
        bumper.list_patterns()
        return

    if not args.pattern:
        print("ERROR: Pattern name required (or use --list)")
        parser.print_help()
        sys.exit(1)

    if args.show:
        bumper.show_version(args.pattern)
        return

    if not args.bump_type:
        print("ERROR: Bump type required (--major, --minor, or --patch)")
        parser.print_help()
        sys.exit(1)

    # Perform version bump
    old_version = bumper.registry['patterns'][args.pattern]['version']
    new_version = bumper.bump_version(
        args.pattern,
        args.bump_type,
        args.breaking_change
    )

    print(f"✅ Bumped {args.pattern}: v{old_version} → v{new_version}")
    if args.bump_type == 'major':
        print(f"   Breaking change: {args.breaking_change}")
    print(f"   Registry updated: {bumper.registry_path}")


if __name__ == "__main__":
    main()
