#!/bin/bash
#
# Pre-release checks for AGET template
# Ensures the template is ready for release
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "===================================================="
echo "AGET Template Pre-Release Checks"
echo "===================================================="
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: File Permissions
echo "1. Checking file permissions..."
if python3 "$SCRIPT_DIR/aget_check_permissions.py" --path "$ROOT_DIR" > /tmp/perms_check.log 2>&1; then
    echo -e "${GREEN}✅ File permissions are correct${NC}"
else
    echo -e "${RED}❌ File permission issues found${NC}"
    cat /tmp/perms_check.log
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 2: Template Compliance (skipped - script not yet created)
echo "2. Checking template compliance..."
echo -e "${YELLOW}⚠️  Template compliance check skipped (test script not yet created)${NC}"
echo ""

# Check 3: Python Syntax Check
echo "3. Checking Python syntax..."
SYNTAX_ERRORS=0
for py_file in $(find "$ROOT_DIR" -name "*.py" -type f -not -path "*/__pycache__/*" -not -path "*/.git/*"); do
    if ! python3 -m py_compile "$py_file" 2>/dev/null; then
        echo -e "${RED}   Syntax error in: $py_file${NC}"
        SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
    fi
done
if [ $SYNTAX_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All Python files have valid syntax${NC}"
else
    echo -e "${RED}❌ Found $SYNTAX_ERRORS Python syntax errors${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 4: Shell Script Syntax Check
echo "4. Checking shell script syntax..."
SHELL_ERRORS=0
for sh_file in $(find "$ROOT_DIR" -name "*.sh" -type f -not -path "*/.git/*"); do
    if ! bash -n "$sh_file" 2>/dev/null; then
        echo -e "${RED}   Syntax error in: $sh_file${NC}"
        SHELL_ERRORS=$((SHELL_ERRORS + 1))
    fi
done
if [ $SHELL_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All shell scripts have valid syntax${NC}"
else
    echo -e "${RED}❌ Found $SHELL_ERRORS shell script syntax errors${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 5: Required Files
echo "5. Checking required files exist..."
REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "SECURITY.md"
    "CONTRIBUTING.md"
    "CHANGELOG.md"
    "install.sh"
    "aget.sh"
    "setup.py"
    "requirements.txt"
    "VERSION"
    ".gitignore"
)
MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$ROOT_DIR/$file" ]; then
        echo -e "${RED}   Missing: $file${NC}"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done
if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}✅ All required files present${NC}"
else
    echo -e "${RED}❌ Missing $MISSING_FILES required files${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 6: No uncommitted changes
echo "6. Checking git status..."
cd "$ROOT_DIR"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
else
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    git status --short
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check 7: Version consistency
echo "7. Checking version consistency..."
VERSION_FILE="$ROOT_DIR/VERSION"
if [ -f "$VERSION_FILE" ]; then
    VERSION=$(cat "$VERSION_FILE")
    echo "   Current version: $VERSION"

    # Check if version is in semantic format
    if [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo -e "${GREEN}✅ Version format is correct${NC}"
    else
        echo -e "${RED}❌ Version format invalid (expected: X.Y.Z)${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ VERSION file not found${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check 8: Documentation quality
echo "8. Checking documentation..."
DOC_ISSUES=0

# Check README has minimum sections
if ! grep -q "## Installation" "$ROOT_DIR/README.md"; then
    echo -e "${YELLOW}   ⚠️  README missing Installation section${NC}"
    DOC_ISSUES=$((DOC_ISSUES + 1))
fi
if ! grep -q "## Usage" "$ROOT_DIR/README.md"; then
    echo -e "${YELLOW}   ⚠️  README missing Usage section${NC}"
    DOC_ISSUES=$((DOC_ISSUES + 1))
fi

if [ $DOC_ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ Documentation structure is good${NC}"
else
    echo -e "${YELLOW}⚠️  Found $DOC_ISSUES documentation issues${NC}"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check 9: No sensitive data
echo "9. Checking for sensitive data..."
SENSITIVE_PATTERNS=(
    "api_key"
    "API_KEY"
    "secret"
    "SECRET"
    "password"
    "PASSWORD"
    "token"
    "TOKEN"
)
SENSITIVE_FOUND=0
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    # Exclude this script and documentation from the check
    if grep -r "$pattern" "$ROOT_DIR" --exclude-dir=.git --exclude-dir=__pycache__ \
           --exclude="*.md" --exclude="pre-release.sh" --exclude="*.log" 2>/dev/null | \
           grep -v "# Example:" | grep -v "# TODO:" | grep -v "print(" > /dev/null; then
        echo -e "${YELLOW}   ⚠️  Found pattern: $pattern${NC}"
        SENSITIVE_FOUND=$((SENSITIVE_FOUND + 1))
    fi
done
if [ $SENSITIVE_FOUND -eq 0 ]; then
    echo -e "${GREEN}✅ No obvious sensitive data patterns found${NC}"
else
    echo -e "${YELLOW}⚠️  Found $SENSITIVE_FOUND potential sensitive patterns (review manually)${NC}"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check 10: README links validation
echo "10. Checking README links..."
BROKEN_LINKS=0
# Extract markdown links from README and check if files exist
while IFS= read -r link; do
    # Extract just the path from the markdown link
    path=$(echo "$link" | sed 's/.*(\([^)]*\))/\1/')
    # Skip URLs (http/https)
    if [[ "$path" =~ ^https?:// ]]; then
        continue
    fi
    # Check if file exists
    if [ ! -f "$ROOT_DIR/$path" ]; then
        echo -e "${RED}   ❌ Broken link: $path${NC}"
        BROKEN_LINKS=$((BROKEN_LINKS + 1))
    fi
done < <(grep -o '\[.*\]([^)]*\.md)' "$ROOT_DIR/README.md" 2>/dev/null)

if [ $BROKEN_LINKS -eq 0 ]; then
    echo -e "${GREEN}✅ All README links are valid${NC}"
else
    echo -e "${RED}❌ Found $BROKEN_LINKS broken links${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Summary
echo "===================================================="
echo "Pre-Release Check Summary"
echo "===================================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED - Ready for release!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  PASSED with $WARNINGS warnings${NC}"
    echo "Review warnings before releasing."
    exit 0
else
    echo -e "${RED}❌ FAILED with $ERRORS errors and $WARNINGS warnings${NC}"
    echo "Fix errors before releasing."
    exit 1
fi