#!/usr/bin/env python3
"""Specification Consistency Check Example

Demonstrates spec_consistency.py pattern for detecting gaps between
specification and implementation.
"""

import sys
import os

# Add .aget directory to path to import patterns
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.aget'))

from patterns.analysis.spec_consistency import analyze


def main():
    """Run spec consistency check."""

    # Paths to spec and implementation
    spec_file = os.path.join(os.path.dirname(__file__), 'user_management_spec.yaml')
    impl_file = os.path.join(os.path.dirname(__file__), 'user_management.py')

    print("=" * 60)
    print("Specification Consistency Check")
    print("=" * 60)
    print()
    print(f"Specification: {os.path.basename(spec_file)}")
    print(f"Implementation: {os.path.basename(impl_file)}")
    print()

    # Run analysis
    result = analyze({
        "spec_path": spec_file,
        "repo_path": impl_file,
        "language": "python",
        "analysis_type": "all"
    })

    # Display results
    if result["status"] == "success":
        # Coverage summary
        coverage = result['coverage']
        print(f"Coverage: {coverage['percentage']}% ({coverage['implemented']}/{coverage['total_capabilities']})")
        print(f"  Implemented: {coverage['implemented']}")
        print(f"  Not Implemented: {coverage['not_implemented']}")
        print()

        # Spec format
        print(f"Spec Format: {result['spec_format']}")
        print()

        # Gaps (missing capabilities)
        if result['gaps']:
            print("Missing Capabilities (Gaps):")
            for gap in result['gaps']:
                priority_symbol = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(gap['priority'], '⚪')

                print(f"  {priority_symbol} {gap['capability_id']}: {gap['description']}")
                print(f"     Priority: {gap['priority']}")
            print()

        # Drift (scope changes)
        if result['drift']:
            print("Scope Drift Detected:")
            for drift_item in result['drift']:
                print(f"  - {drift_item}")
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
        print("Analysis Types:")
        print("- coverage: Calculate implementation percentage")
        print("- gaps: Identify missing capabilities")
        print("- drift: Detect scope expansion/reduction")
        print("- all: Run all analyses (default)")
        print()
        print("Spec Format Support:")
        print("- YAML (with capabilities or EARS requirements)")
        print("- Markdown (CAP-XXX or REQ-XXX identifiers)")
        print("- Plain text (numbered or bulleted lists)")

    else:
        print(f"Error: {result['message']}")


if __name__ == "__main__":
    main()
