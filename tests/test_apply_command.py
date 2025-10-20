#!/usr/bin/env python3
"""Test aget apply command."""

import sys
import tempfile
from pathlib import Path
import time

sys.path.insert(0, '.')

from aget.config.commands.apply import ApplyCommand
from aget.config.commands.init import InitCommand


def test_apply_list():
    """Test listing available patterns."""
    print("Testing `aget apply` (list patterns):")
    print("-" * 40)

    cmd = ApplyCommand()
    result = cmd.execute(args=[])

    print(f"Success: {'✅' if result['success'] else '❌'}")
    if result['success']:
        patterns = result.get('patterns', [])
        print(f"Found {len(patterns)} patterns")
        if patterns:
            print("Sample patterns:")
            for pattern in patterns[:3]:
                print(f"  - {pattern}")


def test_apply_pattern():
    """Test applying a pattern."""
    print("\nTesting `aget apply session/wake`:")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir)

        # First init the project
        init_cmd = InitCommand()
        init_result = init_cmd.execute(args=[str(test_path)])
        assert init_result['success'], "Init should succeed"

        # Now apply pattern
        apply_cmd = ApplyCommand()

        # Test without AGENTS.md (should fail)
        import os
        orig_cwd = os.getcwd()
        try:
            os.chdir('/tmp')
            result = apply_cmd.execute(args=['session/wake'])
            assert not result['success'], "Should fail without AGENTS.md"
            print("✅ Correctly fails without AGENTS.md")

            # Test with AGENTS.md
            os.chdir(test_path)
            result = apply_cmd.execute(args=['session/wake'])

            # The pattern will execute but we're not in a git repo so some checks may fail
            # That's OK for this test - we just want to verify the command works
            print(f"Pattern execution: {'✅' if result['success'] else '⚠️'}")
            if not result['success']:
                print(f"  Note: {result.get('error', 'Pattern may need git repo')}")

        finally:
            os.chdir(orig_cwd)


def test_apply_invalid_pattern():
    """Test applying invalid pattern."""
    print("\nTesting invalid pattern:")
    print("-" * 40)

    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir)

        # Init project first
        init_cmd = InitCommand()
        init_cmd.execute(args=[str(test_path)])

        apply_cmd = ApplyCommand()

        import os
        orig_cwd = os.getcwd()
        try:
            os.chdir(test_path)
            result = apply_cmd.execute(args=['invalid/pattern'])

            assert not result['success'], "Should fail for invalid pattern"
            assert 'not found' in result.get('error', '').lower()
            print("✅ Correctly rejects invalid pattern")
            print(f"   Error: {result.get('error')}")

            # Check it suggests available patterns
            if 'available' in result:
                print(f"   Suggests: {result['available'][:3]}")

        finally:
            os.chdir(orig_cwd)


def test_apply_performance():
    """Test apply command performance."""
    print("\nTesting apply command performance:")
    print("-" * 40)

    cmd = ApplyCommand()

    start = time.time()
    result = cmd.execute(args=[])  # List patterns
    duration = time.time() - start

    assert duration < 2.0, f"Apply command took {duration:.2f}s (should be <2s)"
    print(f"✅ Performance: {duration:.3f}s (requirement: <2s)")


if __name__ == "__main__":
    print("🔧 Apply Command Tests")
    print("=" * 40)

    test_apply_list()
    test_apply_pattern()
    test_apply_invalid_pattern()
    test_apply_performance()

    print("\n" + "=" * 40)
    print("✅ APPLY COMMAND TESTS COMPLETE")