#!/usr/bin/env python3
"""Debugging Assistance Example

Demonstrates debug_assist.py pattern for error analysis and root cause investigation.
"""

import sys
import os

# Add .aget directory to path to import patterns
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.aget'))

from patterns.analysis.debug_assist import analyze


def main():
    """Analyze error scenario."""

    print("=" * 60)
    print("Debugging Assistance Example")
    print("=" * 60)
    print()

    # Simulate error scenario
    error_scenario = {
        "error_type": "TypeError",
        "error_message": "'NoneType' object is not subscriptable",
        "stack_trace": """Traceback (most recent call last):
  File "error_scenario.py", line 38, in <module>
    process_email(999)
  File "error_scenario.py", line 22, in process_email
    email_parts = user['email'].split('@')
TypeError: 'NoneType' object is not subscriptable""",
        "code_context": {
            "file": "error_scenario.py",
            "function": "process_email",
            "line": 22,
            "code_snippet": "email_parts = user['email'].split('@')"
        },
        "language": "python"
    }

    print("Error Details:")
    print(f"  Type: {error_scenario['error_type']}")
    print(f"  Message: {error_scenario['error_message']}")
    print(f"  Location: {error_scenario['code_context']['file']}:{error_scenario['code_context']['line']}")
    print(f"  Code: {error_scenario['code_context']['code_snippet']}")
    print()

    # Run analysis
    result = analyze(error_scenario)

    # Display results
    if result["status"] == "success":
        print(f"Error Pattern: {result['error_pattern']}")
        print(f"Analysis Confidence: {result['confidence']}")
        print()

        # Root cause hypotheses
        print("Root Cause Hypotheses (ranked):")
        print()
        for hypothesis in result['root_cause_hypotheses']:
            print(f"{hypothesis['rank']}. {hypothesis['cause']} ({hypothesis['confidence']} confidence)")
            print(f"   Evidence:")
            for evidence in hypothesis['evidence']:
                print(f"     - {evidence}")
            print()
            print(f"   Fix Strategy:")
            # Print first few lines of fix strategy
            fix_lines = hypothesis['fix_strategy'].split('\n')
            for line in fix_lines[:10]:
                if line.strip():
                    print(f"     {line}")
            print()
            print(f"   Prevention: {hypothesis['prevention']}")
            print()

        # Investigation path
        print("Investigation Path:")
        for step in result['investigation_path']:
            print(f"  {step}")
        print()

        # Recommendations
        if result.get('recommendations'):
            print("Immediate Action:")
            for rec in result['recommendations']:
                print(f"  Priority: {rec['priority']}")
                print(f"  Action: {rec['action']}")
                print(f"  Rationale: {rec['rationale']}")
            print()

        print("=" * 60)
        print()
        print("Key Takeaway:")
        print("Always validate that objects exist before accessing attributes.")
        print("Use null checks or try-except blocks to handle missing data gracefully.")

    else:
        print(f"Error: {result['message']}")


if __name__ == "__main__":
    main()
