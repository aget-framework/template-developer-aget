#!/bin/bash
# ARCH-001 Template Compliance Test
# Tests that template creates self-contained projects

set -e

echo "========================================"
echo "ARCH-001 TEMPLATE COMPLIANCE TEST"
echo "========================================"
echo ""

# Test in isolation
TESTDIR=$(mktemp -d)
echo "📍 Test directory: $TESTDIR"

# Copy template
echo "📦 Copying template..."
cp -r . $TESTDIR/test-aget
cd $TESTDIR/test-aget

# Clean git to ensure fresh state
rm -rf .git
git init -q

echo ""
echo "Test 1: Checking for external paths..."
echo "----------------------------------------"
# Exclude test scripts and verification scripts which check for these patterns
if grep -r "/Users/\|C:\\\\Users\\\\" . \
    --exclude-dir=.git \
    --exclude="*.md" \
    --exclude="*.pyc" \
    --exclude="*.bak" \
    --exclude="security_check.py" \
    --exclude="verify_dependencies.py" \
    --exclude="test_template_compliance.sh" \
    -I 2>/dev/null | grep -v "^Binary file" > /dev/null; then
    echo "❌ Found external paths"
    grep -r "/Users/\|C:\\\\Users\\\\" . \
        --exclude-dir=.git \
        --exclude="*.md" \
        --exclude="*.pyc" \
        --exclude="*.bak" \
        --exclude="security_check.py" \
        --exclude="verify_dependencies.py" \
        --exclude="test_template_compliance.sh" \
        -I 2>/dev/null | grep -v "^Binary file" | head -5
    exit 1
else
    echo "✅ No external paths found"
fi

echo ""
echo "Test 2: Testing wake protocol..."
echo "----------------------------------------"
if python3 scripts/aget_session_protocol.py wake > /dev/null 2>&1; then
    echo "✅ Wake protocol works"
else
    echo "❌ Wake protocol failed"
    python3 scripts/aget_session_protocol.py wake
    exit 1
fi

echo ""
echo "Test 3: Testing pattern availability..."
echo "----------------------------------------"
if [ -f patterns/documentation/smart_reader.py ]; then
    echo "✅ smart_reader.py exists"
else
    echo "❌ smart_reader.py missing"
    exit 1
fi

echo ""
echo "Test 4: Testing verification script..."
echo "----------------------------------------"
if python3 scripts/verify_dependencies.py > /dev/null 2>&1; then
    echo "✅ Verification passed"
else
    echo "❌ Verification failed"
    python3 scripts/verify_dependencies.py
    exit 1
fi

echo ""
echo "Test 5: Testing pattern installation..."
echo "----------------------------------------"
if python3 scripts/install_pattern.py --help > /dev/null 2>&1; then
    echo "✅ Pattern installer works"
else
    echo "❌ Pattern installer failed"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ ALL TESTS PASSED"
echo "========================================"
echo ""
echo "Template is ARCH-001 compliant:"
echo "- No hardcoded paths"
echo "- Self-contained patterns"
echo "- Working infrastructure"
echo "- Isolated operation verified"
echo ""
echo "🎉 Template ready for Gate 2!"

# Cleanup
cd /
rm -rf $TESTDIR