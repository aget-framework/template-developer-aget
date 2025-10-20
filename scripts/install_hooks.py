#!/usr/bin/env python3
"""
Install pre-push hooks for AGET development.

Usage:
    python3 scripts/install_hooks.py              # Interactive mode
    python3 scripts/install_hooks.py --advisory   # Phase 1: Advisory only
    python3 scripts/install_hooks.py --critical   # Phase 2: Critical tests
    python3 scripts/install_hooks.py --smart      # Phase 3: Smart detection
    python3 scripts/install_hooks.py --remove     # Remove hooks
"""

import sys
import os
from pathlib import Path
import subprocess
import argparse

HOOK_PHASES = {
    'advisory': '''#!/bin/bash
# AGET Pre-Push Hook - Advisory Mode (Phase 1)
# This only warns, never blocks pushes

echo "🔍 Pre-push checks (advisory only)..."

# Check if tests exist
if [ -f "tests/test_gate2_features.py" ]; then
    echo "⚠️  Remember to run tests before pushing!"
    echo "   Quick test: python3 -m pytest tests/ -q --maxfail=3"
fi

# Check for uncommitted changes
if ! git diff --quiet; then
    echo "⚠️  You have uncommitted changes"
fi

# Check for untracked Python files
UNTRACKED=$(git ls-files --others --exclude-standard | grep "\\.py$" | head -3)
if [ -n "$UNTRACKED" ]; then
    echo "⚠️  Untracked Python files detected:"
    echo "$UNTRACKED" | sed 's/^/     /'
fi

echo "✅ Push proceeding (checks are advisory only)"
exit 0
''',

    'critical': '''#!/bin/bash
# AGET Pre-Push Hook - Critical Tests (Phase 2)
# Blocks on critical test failures only

echo "🔍 Running critical tests (5-10 seconds)..."

# Check for pytest
if ! command -v pytest &> /dev/null; then
    pip3 install -q pytest pytest-cov
fi

# Define critical tests that MUST pass
CRITICAL_TESTS="
    tests/test_gate2_features.py::TestEndToEndWorkflow::test_full_workflow
    tests/test_session_protocol.py::test_pattern_detection
    tests/test_installer.py::test_installer_minimal_template
"

# Run only critical tests with timeout
timeout 10 python3 -m pytest $CRITICAL_TESTS -q --tb=no 2>/dev/null

RESULT=$?
if [ $RESULT -eq 124 ]; then
    echo "⚠️  Tests timed out (>10s). Proceeding anyway..."
    exit 0
elif [ $RESULT -ne 0 ]; then
    echo "❌ Critical tests failed!"
    echo ""
    echo "   Options:"
    echo "   1. Fix tests:     python3 -m pytest $CRITICAL_TESTS -v"
    echo "   2. Skip hook:     git push --no-verify"
    echo "   3. Switch mode:   python3 scripts/install_hooks.py --advisory"
    echo ""
    exit 1
fi

echo "✅ Critical tests passed"
exit 0
''',

    'smart': '''#!/bin/bash
# AGET Pre-Push Hook - Smart Mode (Phase 3)
# Runs tests based on what changed

echo "🔍 Smart pre-push checks..."

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Get list of modified files compared to main
CHANGED_FILES=$(git diff --name-only origin/main...HEAD 2>/dev/null)

# If can't compare to main, just run critical tests
if [ -z "$CHANGED_FILES" ]; then
    echo "   Running critical tests (can't detect changes)..."
    TESTS="tests/test_installer.py::test_installer_minimal_template"
else
    # Build test list based on changes
    TESTS=""

    # Core framework changes
    if echo "$CHANGED_FILES" | grep -q "^aget/"; then
        TESTS="$TESTS tests/test_gate2_features.py"
    fi

    # Pattern changes
    if echo "$CHANGED_FILES" | grep -q "^patterns/"; then
        TESTS="$TESTS tests/test_*pattern*.py"
    fi

    # Installer changes
    if echo "$CHANGED_FILES" | grep -q "install\\.sh\\|installer\\.py"; then
        TESTS="$TESTS tests/test_installer.py tests/test_enhanced_installer.py"
    fi

    # Session protocol changes
    if echo "$CHANGED_FILES" | grep -q "session.*protocol"; then
        TESTS="$TESTS tests/test_session_protocol.py"
    fi
fi

# Run relevant tests if any
if [ -n "$TESTS" ]; then
    echo "📊 Testing affected areas..."
    echo "   Files changed: $(echo "$CHANGED_FILES" | wc -l)"
    echo "   Tests to run: $(echo $TESTS | wc -w)"

    timeout 15 python3 -m pytest $TESTS -q --tb=no --maxfail=3

    RESULT=$?
    if [ $RESULT -eq 124 ]; then
        echo "⚠️  Tests timed out (>15s). Consider running manually."
        echo "   git push --no-verify (to skip)"
        exit 0
    elif [ $RESULT -ne 0 ]; then
        echo "❌ Tests failed for changed files"
        echo ""
        echo "   Changed files in:"
        echo "$CHANGED_FILES" | cut -d'/' -f1 | sort -u | sed 's/^/     - /'
        echo ""
        echo "   Run tests: python3 -m pytest $TESTS -v"
        echo "   Skip hook: git push --no-verify"
        exit 1
    fi
else
    echo "   No test-worthy changes detected"
fi

echo "✅ All relevant tests passed"
exit 0
''',

    'remove': None  # Special case for removal
}


def install_hook(phase='advisory', force=False):
    """Install pre-push hook for given phase."""
    git_dir = Path('.git')
    if not git_dir.exists():
        print("❌ Not a git repository")
        return False

    hooks_dir = git_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)

    pre_push = hooks_dir / 'pre-push'

    # Check if hook exists
    if pre_push.exists() and not force:
        print(f"⚠️  Hook already exists: {pre_push}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False

    # Write hook content
    hook_content = HOOK_PHASES.get(phase)
    if hook_content:
        pre_push.write_text(hook_content)
        pre_push.chmod(0o755)
        print(f"✅ Installed {phase} mode pre-push hook")
        print(f"   Location: {pre_push}")
        return True

    return False


def remove_hook():
    """Remove pre-push hook."""
    pre_push = Path('.git/hooks/pre-push')
    if pre_push.exists():
        pre_push.unlink()
        print("✅ Pre-push hook removed")
        return True
    else:
        print("ℹ️  No pre-push hook found")
        return False


def test_hook():
    """Test the current hook without pushing."""
    pre_push = Path('.git/hooks/pre-push')
    if not pre_push.exists():
        print("❌ No pre-push hook installed")
        return False

    print("🧪 Testing pre-push hook...")
    result = subprocess.run([str(pre_push)], capture_output=False)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Install AGET pre-push hooks')
    parser.add_argument('--advisory', action='store_true',
                        help='Install Phase 1: Advisory mode (warns only)')
    parser.add_argument('--critical', action='store_true',
                        help='Install Phase 2: Critical tests only')
    parser.add_argument('--smart', action='store_true',
                        help='Install Phase 3: Smart detection')
    parser.add_argument('--remove', action='store_true',
                        help='Remove pre-push hook')
    parser.add_argument('--test', action='store_true',
                        help='Test current hook')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite existing hook without asking')

    args = parser.parse_args()

    # Handle special cases
    if args.remove:
        return remove_hook()

    if args.test:
        return test_hook()

    # Determine which phase to install
    if args.advisory:
        phase = 'advisory'
    elif args.critical:
        phase = 'critical'
    elif args.smart:
        phase = 'smart'
    else:
        # Interactive mode
        print("AGET Pre-Push Hook Installer")
        print("="*40)
        print("\nAvailable modes:")
        print("  1. Advisory  - Warns but never blocks (recommended to start)")
        print("  2. Critical  - Blocks on critical test failures only")
        print("  3. Smart     - Runs tests based on changes")
        print("  4. Remove    - Remove existing hook")
        print("  5. Test      - Test current hook")
        print("  0. Cancel")

        choice = input("\nSelect mode (1-5, 0 to cancel): ")

        if choice == '0':
            print("Cancelled")
            return False
        elif choice == '1':
            phase = 'advisory'
        elif choice == '2':
            phase = 'critical'
        elif choice == '3':
            phase = 'smart'
        elif choice == '4':
            return remove_hook()
        elif choice == '5':
            return test_hook()
        else:
            print("❌ Invalid choice")
            return False

    return install_hook(phase, args.force)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)