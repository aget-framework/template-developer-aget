#!/bin/bash
# verify_public_ready.sh
# Verify aget-cli-agent-template is ready for public release

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== AGET Public Release Verification ===${NC}"
echo ""

ISSUES=0
WARNINGS=0

# Function to check for files
check_no_files() {
    local pattern=$1
    local description=$2

    if ls $pattern 2>/dev/null | grep -q .; then
        echo -e "${RED}✗ Found $description files:${NC}"
        ls $pattern
        ((ISSUES++))
    else
        echo -e "${GREEN}✓ No $description files found${NC}"
    fi
}

# Function to check for content
check_no_content() {
    local pattern=$1
    local description=$2

    if grep -r "$pattern" --include="*.md" --exclude-dir=".git" 2>/dev/null | grep -q .; then
        echo -e "${YELLOW}⚠ Found references to $description:${NC}"
        grep -r "$pattern" --include="*.md" --exclude-dir=".git" | head -3
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓ No references to $description${NC}"
    fi
}

# Function to verify required files exist
check_exists() {
    local file=$1

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ Required file exists: $file${NC}"
    else
        echo -e "${RED}✗ Missing required file: $file${NC}"
        ((ISSUES++))
    fi
}

echo "=== Checking for internal files that should be removed ==="
check_no_files "DAY_*" "daily status"
check_no_files "*_TEST_PLAN*" "test plan"
check_no_files "*_STATUS.md" "status report"
check_no_files "MIGRATION_TEST*" "migration test"
check_no_files "TRANSITION_TEST*" "transition test"
check_no_files "SCRIPT_FIX_REPORT*" "internal fix report"

echo ""
echo "=== Checking for internal content references ==="
check_no_content "spotify-aget" "spotify-aget (test project)"
check_no_content "llm-judge-aget" "llm-judge-aget (test project)"
check_no_content "planner-aget" "planner-aget (test project)"
check_no_content "Day [0-9] " "day-by-day testing"
check_no_content "hours spent\|hours tracked" "hours tracking"

echo ""
echo "=== Checking for sensitive directories ==="
if [ -d "SESSION_NOTES" ]; then
    echo -e "${RED}✗ SESSION_NOTES directory still present${NC}"
    ((ISSUES++))
else
    echo -e "${GREEN}✓ No SESSION_NOTES directory${NC}"
fi

echo ""
echo "=== Verifying required user documentation ==="
check_exists "README.md"
check_exists "CHANGELOG.md"
check_exists "LICENSE"
check_exists "docs/GET_STARTED.md"
check_exists "docs/MIGRATE_TO_V2.md"

echo ""
echo "=== Checking code quality indicators ==="

# Check for TODO/FIXME in user-facing docs
TODO_COUNT=$(grep -r "TODO\|FIXME\|XXX" --include="*.md" docs/ README.md 2>/dev/null | wc -l)
if [ $TODO_COUNT -gt 0 ]; then
    echo -e "${YELLOW}⚠ Found $TODO_COUNT TODO/FIXME markers in documentation${NC}"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓ No TODO/FIXME markers in user docs${NC}"
fi

# Check for profanity or frustration
if grep -r "fuck\|shit\|damn\|crap" --include="*.md" 2>/dev/null | grep -q .; then
    echo -e "${RED}✗ Found unprofessional language${NC}"
    ((ISSUES++))
else
    echo -e "${GREEN}✓ No unprofessional language detected${NC}"
fi

echo ""
echo "=== Final Summary ==="
echo "Critical Issues: $ISSUES"
echo "Warnings: $WARNINGS"

if [ $ISSUES -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ READY FOR RELEASE - No issues found!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️ READY WITH WARNINGS - Review warnings above${NC}"
        echo "The repository can be released but consider addressing warnings"
        exit 0
    fi
else
    echo -e "${RED}❌ NOT READY - Critical issues must be fixed${NC}"
    echo ""
    echo "Run cleanup script first:"
    echo "  ./scripts/move_internal_to_private.sh"
    exit 1
fi