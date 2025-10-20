# Pre-Push Hook Implementation Plan

## Goal
Prevent broken code from reaching GitHub while maintaining fast development workflow.

## Design Principles
1. **Start minimal** - Don't block developers initially
2. **Incremental adoption** - Gradually increase coverage
3. **Fast feedback** - Keep hooks under 10 seconds
4. **Opt-in first** - Let developers choose their level
5. **Clear escape hatches** - Allow bypassing when needed

## Implementation Phases

### Phase 1: Advisory Mode (Week 1)
**Goal**: Inform without blocking

```bash
#!/bin/bash
# .git/hooks/pre-push (chmod +x)

echo "🔍 Pre-push checks (advisory only)..."

# Check if tests exist
if [ -f "tests/test_gate2_features.py" ]; then
    echo "⚠️  Remember to run tests before pushing!"
    echo "   Run: python3 -m pytest tests/ -q"
fi

# Check for uncommitted changes
if ! git diff --quiet; then
    echo "⚠️  You have uncommitted changes"
fi

echo "✅ Push proceeding (checks are advisory only)"
exit 0  # Always allow push
```

### Phase 2: Critical Tests Only (Week 2)
**Goal**: Block only on critical failures

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "🔍 Running critical tests (5-10 seconds)..."

# Define critical tests that MUST pass
CRITICAL_TESTS="
    tests/test_gate2_features.py::TestEndToEndWorkflow::test_full_workflow
    tests/test_session_protocol.py::test_pattern_detection
    tests/test_installer.py::test_installer_minimal_template
"

# Run only critical tests
python3 -m pytest $CRITICAL_TESTS -q --tb=no 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Critical tests failed!"
    echo "   Run full tests: python3 -m pytest tests/"
    echo "   Skip hook: git push --no-verify"
    exit 1
fi

echo "✅ Critical tests passed"
exit 0
```

### Phase 3: Smart Detection (Week 3)
**Goal**: Run tests based on what changed

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "🔍 Smart pre-push checks..."

# Get list of modified files
CHANGED_FILES=$(git diff --name-only HEAD origin/main 2>/dev/null)

# Determine what to test based on changes
RUN_TESTS=""

# If core files changed, run core tests
if echo "$CHANGED_FILES" | grep -q "aget/"; then
    RUN_TESTS="$RUN_TESTS tests/test_gate2_features.py"
fi

# If patterns changed, test patterns
if echo "$CHANGED_FILES" | grep -q "patterns/"; then
    RUN_TESTS="$RUN_TESTS tests/test_*pattern*.py"
fi

# If installer changed, test installer
if echo "$CHANGED_FILES" | grep -q "install.sh\|installer.py"; then
    RUN_TESTS="$RUN_TESTS tests/test_installer.py"
fi

if [ -n "$RUN_TESTS" ]; then
    echo "📊 Testing affected areas..."
    python3 -m pytest $RUN_TESTS -q --tb=no

    if [ $? -ne 0 ]; then
        echo "❌ Tests failed for changed files"
        echo "   Details: python3 -m pytest $RUN_TESTS"
        echo "   Force: git push --no-verify"
        exit 1
    fi
fi

echo "✅ All relevant tests passed"
exit 0
```

### Phase 4: Full Integration (Week 4)
**Goal**: Complete safety net with performance optimization

```bash
#!/bin/bash
# .git/hooks/pre-push

# Load configuration
HOOK_CONFIG=".git/hooks/config"
if [ -f "$HOOK_CONFIG" ]; then
    source "$HOOK_CONFIG"
fi

# Default settings
MAX_TIME=${HOOK_MAX_TIME:-10}
TEST_LEVEL=${HOOK_TEST_LEVEL:-smart}  # none, critical, smart, full

case "$TEST_LEVEL" in
    none)
        echo "⚠️  Pre-push hooks disabled"
        exit 0
        ;;
    critical)
        TEST_CMD="python3 -m pytest tests/test_critical.txt -q"
        ;;
    smart)
        # Smart detection logic here
        TEST_CMD="python3 scripts/smart_test_selector.py"
        ;;
    full)
        TEST_CMD="python3 -m pytest tests/ -q --maxfail=3"
        ;;
esac

# Run with timeout
echo "🔍 Running $TEST_LEVEL tests (max ${MAX_TIME}s)..."
timeout $MAX_TIME $TEST_CMD

RESULT=$?
if [ $RESULT -eq 124 ]; then
    echo "⚠️  Tests timed out after ${MAX_TIME}s"
    echo "   Configure: echo 'HOOK_MAX_TIME=20' >> .git/hooks/config"
    exit 1
elif [ $RESULT -ne 0 ]; then
    echo "❌ Tests failed"
    echo "   Skip: git push --no-verify"
    echo "   Configure: echo 'HOOK_TEST_LEVEL=none' >> .git/hooks/config"
    exit 1
fi

echo "✅ Pre-push checks passed"
exit 0
```

## Installation Guide

### Quick Start (Phase 1 - Advisory)
```bash
# Create hook file
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "⚠️  Remember to test before pushing!"
echo "   python3 -m pytest tests/ -q"
exit 0
EOF

# Make executable
chmod +x .git/hooks/pre-push
```

### Developer Options
```bash
# Configure your preference
echo "HOOK_TEST_LEVEL=critical" >> .git/hooks/config  # Fast, essential only
echo "HOOK_TEST_LEVEL=smart" >> .git/hooks/config     # Balanced (default)
echo "HOOK_TEST_LEVEL=full" >> .git/hooks/config      # Comprehensive
echo "HOOK_TEST_LEVEL=none" >> .git/hooks/config      # Disable

# Set timeout
echo "HOOK_MAX_TIME=5" >> .git/hooks/config   # Faster
echo "HOOK_MAX_TIME=30" >> .git/hooks/config  # More thorough
```

### Team Rollout

#### Week 1: Soft Launch
- Install advisory hooks for volunteers
- Collect feedback on workflow impact
- Measure typical test run times

#### Week 2: Critical Path
- Enable critical tests for core contributors
- Document bypass procedures
- Create test categorization

#### Week 3: Smart Mode Beta
- Deploy smart detection to early adopters
- Refine file-to-test mapping
- Optimize test selection algorithm

#### Week 4: Full Rollout
- Make hooks part of setup process
- Document in CONTRIBUTING.md
- Add to onboarding checklist

## Supporting Infrastructure

### 1. Test Categorization File
Create `tests/critical.txt`:
```
tests/test_gate2_features.py::TestEndToEndWorkflow
tests/test_session_protocol.py::test_pattern_detection
tests/test_installer.py::test_installer_minimal_template
```

### 2. Smart Test Selector
Create `scripts/smart_test_selector.py`:
```python
#!/usr/bin/env python3
"""Select tests based on git changes."""

import subprocess
import sys
from pathlib import Path

def get_changed_files():
    """Get list of changed files."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "origin/main"],
        capture_output=True, text=True
    )
    return result.stdout.strip().split('\n')

def map_files_to_tests(changed_files):
    """Map changed files to relevant tests."""
    tests = set()

    for file in changed_files:
        if 'aget/' in file:
            tests.add('tests/test_gate2_features.py')
        if 'patterns/' in file:
            tests.add('tests/test_*pattern*.py')
        if 'installer' in file:
            tests.add('tests/test_installer.py')

    return list(tests)

if __name__ == "__main__":
    changed = get_changed_files()
    tests = map_files_to_tests(changed)

    if tests:
        cmd = ["python3", "-m", "pytest"] + tests + ["-q"]
        sys.exit(subprocess.run(cmd).returncode)

    print("No relevant tests to run")
    sys.exit(0)
```

### 3. Performance Monitor
Track hook performance:
```bash
# Add to pre-push hook
START_TIME=$(date +%s)
# ... run tests ...
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "Hook completed in ${DURATION}s" >> .git/hooks/performance.log
```

## Success Metrics

### Phase 1 (Advisory)
- [ ] 0% push blockage
- [ ] Developer awareness increased
- [ ] Feedback collected

### Phase 2 (Critical)
- [ ] <5% false positives
- [ ] <10 second average runtime
- [ ] 90% adoption rate

### Phase 3 (Smart)
- [ ] <10% unnecessary test runs
- [ ] <15 second average runtime
- [ ] Test relevant to changes 95% of time

### Phase 4 (Full)
- [ ] 0 broken pushes to main
- [ ] <20 second worst case
- [ ] 100% configurable by developers

## Escape Hatches

Always provide ways to bypass:
1. `git push --no-verify` - Skip all hooks
2. `SKIP_TESTS=1 git push` - Environment variable
3. `.git/hooks/config` - Personal configuration
4. Emergency bypass: `rm .git/hooks/pre-push`

## FAQ

**Q: What if I need to push a WIP?**
A: Use `git push --no-verify` or push to a feature branch

**Q: Can I customize which tests run?**
A: Yes, edit `.git/hooks/config` or `tests/critical.txt`

**Q: What if tests are too slow?**
A: Reduce `HOOK_MAX_TIME` or switch to `critical` mode

**Q: How do I disable for one project?**
A: Set `HOOK_TEST_LEVEL=none` in `.git/hooks/config`

## Next Steps

1. [ ] Get team feedback on this plan
2. [ ] Start with Phase 1 (advisory mode)
3. [ ] Create `tests/critical.txt` file
4. [ ] Document in CONTRIBUTING.md
5. [ ] Add to setup scripts

---
*Plan created: 2025-09-25*
*Estimated rollout: 4 weeks*
*Risk level: Low (incremental approach)*