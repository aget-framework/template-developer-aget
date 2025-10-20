#!/usr/bin/env python3
"""
Pattern Compatibility Checker - v2.3 Gate A2

Checks pattern version compatibility across AGETs to detect conflicts.
Validates that pattern dependencies are satisfied.
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


class PatternCompatibilityChecker:
    """Check pattern version compatibility."""

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

    def _parse_version(self, version_str: str) -> Tuple[int, int, int]:
        """Parse semantic version string."""
        try:
            parts = version_str.replace('"', '').replace("'", "").split('.')
            if len(parts) != 3:
                raise ValueError
            return tuple(int(p) for p in parts)
        except (ValueError, AttributeError):
            print(f"ERROR: Invalid version format: {version_str}")
            return (0, 0, 0)

    def _satisfies_requirement(self, version: str, requirement: str) -> bool:
        """Check if version satisfies requirement (^x.y.z notation)."""
        if not requirement.startswith('^'):
            # Exact match required
            return version == requirement

        # Caret range (^1.2.3 allows >=1.2.3 <2.0.0)
        req_version = requirement[1:]  # Remove ^
        req_major, req_minor, req_patch = self._parse_version(req_version)
        ver_major, ver_minor, ver_patch = self._parse_version(version)

        # Major version must match
        if ver_major != req_major:
            return False

        # Version must be >= required version
        if (ver_major, ver_minor, ver_patch) >= (req_major, req_minor, req_patch):
            return True

        return False

    def check_dependencies(self) -> List[Dict]:
        """Check all pattern dependencies are satisfied."""
        issues = []

        if 'dependencies' not in self.registry:
            return issues

        for pattern_name, deps in self.registry['dependencies'].items():
            if pattern_name not in self.registry['patterns']:
                issues.append({
                    'pattern': pattern_name,
                    'type': 'missing_pattern',
                    'severity': 'error',
                    'message': f"Pattern {pattern_name} has dependencies but is not in registry"
                })
                continue

            if 'requires' not in deps:
                continue

            for requirement in deps['requires']:
                # Parse requirement (format: "pattern/name: ^1.0.0")
                if isinstance(requirement, dict):
                    for required_pattern, version_req in requirement.items():
                        if required_pattern not in self.registry['patterns']:
                            issues.append({
                                'pattern': pattern_name,
                                'type': 'missing_dependency',
                                'severity': 'error',
                                'required': required_pattern,
                                'version': version_req,
                                'message': f"{pattern_name} requires {required_pattern} {version_req} but it is not in registry"
                            })
                            continue

                        actual_version = self.registry['patterns'][required_pattern]['version']
                        if not self._satisfies_requirement(actual_version, version_req):
                            issues.append({
                                'pattern': pattern_name,
                                'type': 'version_conflict',
                                'severity': 'error',
                                'required': required_pattern,
                                'required_version': version_req,
                                'actual_version': actual_version,
                                'message': f"{pattern_name} requires {required_pattern} {version_req} but found {actual_version}"
                            })

        return issues

    def check_breaking_changes(self) -> List[Dict]:
        """Check for patterns with breaking changes."""
        warnings = []

        for pattern_name, pattern in self.registry['patterns'].items():
            if pattern.get('breaking_changes'):
                for change in pattern['breaking_changes']:
                    warnings.append({
                        'pattern': pattern_name,
                        'type': 'breaking_change',
                        'severity': 'warning',
                        'version': change['version'],
                        'date': change['date'],
                        'description': change['description'],
                        'message': f"{pattern_name} v{change['version']} has breaking change: {change['description']}"
                    })

        return warnings

    def generate_report(self) -> Dict:
        """Generate compatibility report."""
        dependency_issues = self.check_dependencies()
        breaking_changes = self.check_breaking_changes()

        errors = [i for i in dependency_issues if i['severity'] == 'error']
        warnings = breaking_changes + [i for i in dependency_issues if i['severity'] == 'warning']

        return {
            'total_patterns': len(self.registry['patterns']),
            'errors': errors,
            'warnings': warnings,
            'passed': len(errors) == 0
        }

    def print_report(self, report: Dict):
        """Print human-readable compatibility report."""
        print("=" * 70)
        print("PATTERN COMPATIBILITY REPORT")
        print("=" * 70)
        print()
        print(f"Total patterns: {report['total_patterns']}")
        print(f"Errors: {len(report['errors'])}")
        print(f"Warnings: {len(report['warnings'])}")
        print()

        if report['errors']:
            print("ERRORS:")
            print("-" * 70)
            for error in report['errors']:
                print(f"  {error['pattern']}:")
                print(f"    {error['message']}")
            print()

        if report['warnings']:
            print("WARNINGS:")
            print("-" * 70)
            for warning in report['warnings']:
                print(f"  {warning['pattern']}:")
                print(f"    {warning['message']}")
            print()

        if report['passed']:
            print("✅ PASS: All compatibility checks passed")
        else:
            print(f"❌ FAIL: {len(report['errors'])} compatibility errors found")

        print("=" * 70)


def main():
    """Run compatibility checker."""
    parser = argparse.ArgumentParser(
        description="Check pattern version compatibility"
    )
    parser.add_argument(
        '--registry',
        type=Path,
        help='Path to versions.yaml registry'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    checker = PatternCompatibilityChecker(args.registry)
    report = checker.generate_report()
    checker.print_report(report)

    # Exit code
    if not report['passed']:
        sys.exit(1)
    if args.strict and report['warnings']:
        print("\n⚠️  STRICT MODE: Warnings present")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
