#!/usr/bin/env python3
"""Coding Standards Checking Example

Demonstrates standards_check.py pattern on sample code with PEP-8 violations.
"""

import sys
import os

# Add .aget directory to path to import patterns
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.aget'))

from patterns.analysis.standards_check import analyze


def main():
    """Run standards compliance check on sample_code.py."""

    # Path to sample code
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_code.py')

    print("=" * 60)
    print("Coding Standards Compliance Check")
    print("=" * 60)
    print()
    print(f"Checking: {sample_file}")
    print()

    # Run analysis
    result = analyze({
        "repo_path": sample_file,
        "language": "python",
        "standards": "auto"  # Use built-in PEP-8
    })

    # Display results
    if result["status"] == "success":
        print(f"Compliance Rating: {result['compliance_rating']}/10")
        print(f"Standards Applied: {result['standards_applied']}")
        print()

        # Violation summary
        summary = result['violation_summary']
        print("Violation Summary:")
        print(f"  Errors: {summary['error']}")
        print(f"  Warnings: {summary['warning']}")
        print(f"  Info: {summary['info']}")
        print(f"  Total: {summary['total']}")
        print()

        # List violations
        if result['violations']:
            print("Violations Found:")
            for violation in result['violations']:
                severity_symbol = {
                    'error': '✗',
                    'warning': '⚠',
                    'info': 'ℹ'
                }.get(violation['severity'], '•')

                print(f"  {severity_symbol} {violation['file']}:{violation['line']}")
                print(f"     [{violation['code']}] {violation['message']}")
                print(f"     Fix: {violation['fix_example']}")
                print()

        # Recommendations
        if result.get('recommendations'):
            print("Recommendations:")
            for rec in result['recommendations']:
                print(f"  [{rec['priority']}] {rec['message']}")
                print(f"      → {rec['action']}")
            print()

        print("=" * 60)
        print()
        print("Standards Precedence Order:")
        print("1. Repo-specific (.coding-standards.md in repo root)")
        print("2. Agent-level (custom standards in .aget/)")
        print("3. Built-in (PEP-8 for Python, ESLint for JavaScript, etc.)")

    else:
        print(f"Error: {result['message']}")


if __name__ == "__main__":
    main()
