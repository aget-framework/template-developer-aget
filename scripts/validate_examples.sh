#!/bin/bash
# Validate Examples Script
#
# Verifies that all example workflows execute successfully.

set -e  # Exit on first error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXAMPLES_DIR="$REPO_ROOT/examples"

echo "=========================================="
echo "Validating Template Examples"
echo "=========================================="
echo

# Track results
TOTAL=0
PASSED=0
FAILED=0

# Function to run example and capture result
run_example() {
    local example_name="$1"
    local script_name="$2"
    local example_dir="$EXAMPLES_DIR/$example_name"

    TOTAL=$((TOTAL + 1))

    echo "Testing: $example_name"
    echo "  Script: $script_name"

    if [ ! -f "$example_dir/$script_name" ]; then
        echo "  ✗ FAILED: Script not found"
        FAILED=$((FAILED + 1))
        echo
        return 1
    fi

    # Run example and capture output
    cd "$example_dir"
    if output=$(python3 "$script_name" 2>&1); then
        echo "  ✓ PASSED"
        PASSED=$((PASSED + 1))
    else
        echo "  ✗ FAILED: Execution error"
        echo "  Output: $output"
        FAILED=$((FAILED + 1))
    fi

    cd "$REPO_ROOT"
    echo
}

# Validate code_quality_analysis example
run_example "code_quality_analysis" "run_analysis.py"

# Validate standards_checking example
run_example "standards_checking" "run_check.py"

# Validate debugging_assistance example
run_example "debugging_assistance" "run_debug.py"

# Validate spec_consistency example
run_example "spec_consistency" "run_check.py"

# Summary
echo "=========================================="
echo "Validation Summary"
echo "=========================================="
echo "Total examples: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo

if [ $FAILED -eq 0 ]; then
    echo "✓ All examples validated successfully"
    exit 0
else
    echo "✗ $FAILED example(s) failed validation"
    exit 1
fi
