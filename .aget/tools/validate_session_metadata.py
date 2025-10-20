#!/usr/bin/env python3
"""
Session Metadata Validator - v2.3 Gate A3

Validates session metadata against JSON Schema.
Ensures metadata completeness and correctness.
"""

import argparse
import json
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class SessionMetadataValidator:
    """Validate session metadata against schema."""

    def __init__(self, schema_path: Path = None):
        self.project_root = Path.cwd()
        self.schema_path = schema_path or self.project_root / ".aget/schemas/session_metadata_v1.0.json"
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict:
        """Load JSON Schema."""
        if not self.schema_path.exists():
            print(f"ERROR: Schema not found: {self.schema_path}")
            sys.exit(1)

        with open(self.schema_path, 'r') as f:
            return json.load(f)

    def extract_frontmatter(self, content: str) -> Optional[Dict]:
        """Extract YAML frontmatter from markdown file."""
        # Check for frontmatter
        if not content.startswith('---\n'):
            return None

        # Find end of frontmatter
        end_match = re.search(r'\n---\n', content[4:])
        if not end_match:
            return None

        # Extract and parse YAML
        yaml_content = content[4:4 + end_match.start()]
        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in frontmatter: {e}")
            return None

    def validate_metadata(self, metadata: Dict) -> List[str]:
        """Validate metadata against schema (simplified validation)."""
        errors = []

        # Check required fields
        required = self.schema.get('required', [])
        for field in required:
            if field not in metadata:
                errors.append(f"Missing required field: {field}")

        # Validate specific fields
        if 'date' in metadata:
            date_str = str(metadata['date'])  # Handle datetime.date objects
            if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date_str):
                errors.append(f"Invalid date format: {date_str} (expected YYYY-MM-DD)")

        if 'duration_minutes' in metadata:
            if not isinstance(metadata['duration_minutes'], int):
                errors.append(f"duration_minutes must be integer, got {type(metadata['duration_minutes'])}")
            elif metadata['duration_minutes'] < 1 or metadata['duration_minutes'] > 600:
                errors.append(f"duration_minutes must be 1-600, got {metadata['duration_minutes']}")

        if 'objectives' in metadata:
            if not isinstance(metadata['objectives'], list):
                errors.append("objectives must be array")
            elif len(metadata['objectives']) == 0:
                errors.append("objectives must have at least one item")

        if 'outcomes' in metadata:
            if not isinstance(metadata['outcomes'], list):
                errors.append("outcomes must be array")
            elif len(metadata['outcomes']) == 0:
                errors.append("outcomes must have at least one item")

        # Validate learnings
        if 'learnings' in metadata:
            if not isinstance(metadata['learnings'], list):
                errors.append("learnings must be array")
            else:
                for i, learning in enumerate(metadata['learnings']):
                    if not isinstance(learning, dict):
                        errors.append(f"learnings[{i}] must be object")
                        continue
                    if 'id' not in learning:
                        errors.append(f"learnings[{i}] missing 'id' field")
                    elif not re.match(r'^L[0-9]+$', learning['id']):
                        errors.append(f"learnings[{i}].id invalid format: {learning['id']} (expected L[0-9]+)")
                    if 'description' not in learning:
                        errors.append(f"learnings[{i}] missing 'description' field")

        # Validate commits
        if 'commits' in metadata:
            if not isinstance(metadata['commits'], list):
                errors.append("commits must be array")
            else:
                for i, commit in enumerate(metadata['commits']):
                    if not isinstance(commit, dict):
                        errors.append(f"commits[{i}] must be object")
                        continue
                    if 'hash' not in commit:
                        errors.append(f"commits[{i}] missing 'hash' field")
                    elif not re.match(r'^[a-f0-9]{7,40}$', commit['hash']):
                        errors.append(f"commits[{i}].hash invalid format: {commit['hash']}")
                    if 'message' not in commit:
                        errors.append(f"commits[{i}] missing 'message' field")

        # Validate patterns_used
        if 'patterns_used' in metadata:
            if not isinstance(metadata['patterns_used'], list):
                errors.append("patterns_used must be array")
            else:
                for i, pattern in enumerate(metadata['patterns_used']):
                    if not isinstance(pattern, dict):
                        errors.append(f"patterns_used[{i}] must be object")
                        continue
                    if 'name' not in pattern:
                        errors.append(f"patterns_used[{i}] missing 'name' field")
                    if 'version' not in pattern:
                        errors.append(f"patterns_used[{i}] missing 'version' field")
                    elif not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', pattern['version']):
                        errors.append(f"patterns_used[{i}].version invalid semver: {pattern['version']}")

        return errors

    def validate_session_file(self, session_file: Path) -> Dict:
        """Validate session file."""
        result = {
            'file': str(session_file),
            'has_metadata': False,
            'valid': False,
            'errors': [],
            'warnings': []
        }

        if not session_file.exists():
            result['errors'].append("File not found")
            return result

        # Read file
        try:
            content = session_file.read_text()
        except Exception as e:
            result['errors'].append(f"Could not read file: {e}")
            return result

        # Extract frontmatter
        metadata = self.extract_frontmatter(content)
        if not metadata:
            result['warnings'].append("No metadata frontmatter found")
            return result

        result['has_metadata'] = True

        # Validate metadata
        errors = self.validate_metadata(metadata)
        result['errors'] = errors
        result['valid'] = len(errors) == 0

        # Calculate completeness
        optional_fields = ['learnings', 'issues_filed', 'commits', 'files_changed',
                          'patterns_used', 'agets_collaborated', 'pain_points', 'next_steps']
        present_optional = sum(1 for f in optional_fields if f in metadata)
        result['completeness'] = f"{present_optional}/{len(optional_fields)} optional fields"

        return result

    def scan_sessions(self, sessions_dir: Path = None) -> Dict:
        """Scan all session files in directory."""
        sessions_dir = sessions_dir or self.project_root / "sessions"

        if not sessions_dir.exists():
            return {
                'total_files': 0,
                'with_metadata': 0,
                'valid': 0,
                'invalid': 0,
                'files': []
            }

        results = []
        for session_file in sorted(sessions_dir.glob("*.md")):
            result = self.validate_session_file(session_file)
            results.append(result)

        return {
            'total_files': len(results),
            'with_metadata': sum(1 for r in results if r['has_metadata']),
            'valid': sum(1 for r in results if r['valid']),
            'invalid': sum(1 for r in results if r['has_metadata'] and not r['valid']),
            'files': results
        }

    def print_report(self, scan_results: Dict):
        """Print validation report."""
        print("=" * 70)
        print("SESSION METADATA VALIDATION REPORT")
        print("=" * 70)
        print()
        print(f"Total session files: {scan_results['total_files']}")
        print(f"With metadata: {scan_results['with_metadata']}")
        print(f"Valid metadata: {scan_results['valid']}")
        print(f"Invalid metadata: {scan_results['invalid']}")
        print(f"Adoption rate: {scan_results['with_metadata'] / max(scan_results['total_files'], 1) * 100:.1f}%")
        print()

        # Show invalid files
        invalid_files = [f for f in scan_results['files'] if f['has_metadata'] and not f['valid']]
        if invalid_files:
            print("INVALID METADATA:")
            print("-" * 70)
            for file_result in invalid_files:
                print(f"\n{Path(file_result['file']).name}:")
                for error in file_result['errors']:
                    print(f"  ❌ {error}")

        # Show files without metadata
        no_metadata = [f for f in scan_results['files'] if not f['has_metadata']]
        if no_metadata:
            print("\nFILES WITHOUT METADATA:")
            print("-" * 70)
            for file_result in no_metadata:
                fname = Path(file_result['file']).name
                warnings = file_result.get('warnings', [])
                warning_str = f" ({warnings[0]})" if warnings else ""
                print(f"  ⚠️  {fname}{warning_str}")

        print()
        print("=" * 70)


def main():
    """Run session metadata validator."""
    parser = argparse.ArgumentParser(
        description="Validate session metadata"
    )
    parser.add_argument(
        'file',
        nargs='?',
        type=Path,
        help='Specific session file to validate'
    )
    parser.add_argument(
        '--scan',
        action='store_true',
        help='Scan all sessions in sessions/ directory'
    )
    parser.add_argument(
        '--schema',
        type=Path,
        help='Path to JSON Schema file'
    )

    args = parser.parse_args()

    validator = SessionMetadataValidator(args.schema)

    if args.scan:
        # Scan all sessions
        results = validator.scan_sessions()
        validator.print_report(results)

        # Exit code based on validity
        if results['invalid'] > 0:
            sys.exit(1)
    elif args.file:
        # Validate single file
        result = validator.validate_session_file(args.file)

        print(f"File: {result['file']}")
        print(f"Has metadata: {result['has_metadata']}")
        if result['has_metadata']:
            print(f"Valid: {result['valid']}")
            print(f"Completeness: {result.get('completeness', 'N/A')}")

            if result['errors']:
                print("\nErrors:")
                for error in result['errors']:
                    print(f"  ❌ {error}")
            else:
                print("\n✅ Metadata is valid")
        else:
            print("⚠️  No metadata found")

        sys.exit(0 if result['valid'] else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
