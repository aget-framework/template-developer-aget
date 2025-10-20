#!/usr/bin/env python3
"""Code Quality Analysis Example

Demonstrates code_quality.py pattern on sample code with quality issues.
"""

import sys
import os

# Add .aget directory to path to import patterns
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.aget'))

from patterns.analysis.code_quality import analyze


def main():
    """Run code quality analysis on sample_code.py."""

    # Path to sample code
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_code.py')

    print("=" * 60)
    print("Code Quality Analysis Example")
    print("=" * 60)
    print()
    print(f"Analyzing: {sample_file}")
    print()

    # Run analysis
    result = analyze({
        "repo_path": sample_file,
        "language": "python"
    })

    # Display results
    if result["status"] == "success":
        print(f"Overall Quality: {result['overall_quality']}/10")
        print()

        # Complexity metrics
        complexity = result['metrics']['complexity']
        print("Complexity Metrics:")
        print(f"  Average Cyclomatic Complexity: {complexity['avg_cyclomatic']}")
        print(f"  Maximum Complexity: {complexity['max_cyclomatic']}")

        if complexity['high_complexity_functions']:
            print()
            print("  High Complexity Functions:")
            for func in complexity['high_complexity_functions'][:3]:
                print(f"    - {func['function']}() in {func['file']}: {func['complexity']}")

        print()

        # Maintainability
        maintainability = result['metrics']['maintainability']
        print("Maintainability:")
        print(f"  Index: {maintainability['index']}/100 ({maintainability['status']})")
        print()

        # Technical debt
        debt = result['metrics']['technical_debt']
        print("Technical Debt:")
        print(f"  TODO comments: {debt['todo_count']}")
        print(f"  FIXME comments: {debt['fixme_count']}")

        if debt['items']:
            print()
            print("  Debt Items:")
            for item in debt['items'][:3]:
                print(f"    - {item['type']} at line {item['line']}: {item['text']}")

        print()

        # Code smells
        smells = result['metrics']['code_smells']
        if smells:
            print("Code Smells Detected:")
            for smell in smells[:5]:
                if smell['type'] == 'long_method':
                    print(f"  - Long method: {smell['function']}() ({smell['lines']} lines)")
                elif smell['type'] == 'high_complexity':
                    print(f"  - High complexity: {smell['function']}() (complexity: {smell['complexity']})")
                elif smell['type'] == 'nested_conditionals':
                    print(f"  - Nested conditionals: {smell['function']}() (depth: {smell['depth']})")
            print()

        # Recommendations
        if result.get('recommendations'):
            print("Recommendations:")
            for rec in result['recommendations'][:3]:
                print(f"  [{rec['priority']}] {rec['message']}")
                print(f"      → {rec['fix_strategy']}")
            print()

        print("=" * 60)
        print()
        print("Interpretation:")
        print("- Complexity >10: Consider refactoring")
        print("- Maintainability <65: Needs improvement")
        print("- TODO/FIXME: Address technical debt")
        print("- Code smells: Indicators of design issues")

    else:
        print(f"Error: {result['message']}")


if __name__ == "__main__":
    main()
