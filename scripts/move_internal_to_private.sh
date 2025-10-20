#!/bin/bash
# move_internal_to_private.sh
# Move internal development docs from public aget-cli-agent-template to private aget-aget

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== AGET Pre-Release Cleanup Script ===${NC}"
echo "This script moves internal docs from public to private repo"
echo ""

# Check we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "patterns" ]; then
    echo -e "${RED}Error: Not in aget-cli-agent-template root directory${NC}"
    exit 1
fi

# Define paths
AGET_AGET_DIR="$HOME/github/aget-aget"
TARGET_DIR="$AGET_AGET_DIR/aget-cli-agent-template-dev"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Check aget-aget exists
if [ ! -d "$AGET_AGET_DIR" ]; then
    echo -e "${RED}Error: aget-aget directory not found at $AGET_AGET_DIR${NC}"
    echo "Please clone aget-aget first"
    exit 1
fi

# Create target directory
echo -e "${YELLOW}Creating target directory...${NC}"
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/archive_$TIMESTAMP"

# Function to move files safely
move_if_exists() {
    local file=$1
    if [ -f "$file" ] || [ -d "$file" ]; then
        echo "  Moving: $file"
        mv "$file" "$TARGET_DIR/"
        return 0
    else
        echo "  Skipping: $file (not found)"
        return 1
    fi
}

echo -e "${YELLOW}Moving internal development files...${NC}"

# Phase 1: Test Documentation
echo "Phase 1: Test documentation"
move_if_exists "DAY_1_STATUS.md"
move_if_exists "DAY_1_TEST_PLAN.md"
move_if_exists "DAY_2_STATUS.md"
move_if_exists "DAY_2_TEST_PLAN.md"
move_if_exists "DAY_3_PREVIEW.md"
move_if_exists "V2_INCREMENTAL_TEST_PLAN.md"
move_if_exists "MIGRATION_TEST_MATRIX.md"
move_if_exists "TRANSITION_TEST_SUITE.md"
move_if_exists "SCRIPT_FIX_REPORT.md"

# Phase 2: Session Notes
echo "Phase 2: Session notes"
move_if_exists "SESSION_NOTES"

# Phase 3: Internal docs from docs/
echo "Phase 3: Internal documentation"
if [ -f "docs/V2_RELEASE_TEST_PLAN.md" ]; then
    mv "docs/V2_RELEASE_TEST_PLAN.md" "$TARGET_DIR/"
fi

# Phase 4: Clean up any test artifacts
echo "Phase 4: Cleaning test artifacts"
find . -name "*test-report*" -o -name "*migration-report*" 2>/dev/null | while read file; do
    echo "  Found artifact: $file"
    mv "$file" "$TARGET_DIR/archive_$TIMESTAMP/"
done

# Create a public-friendly release plan
echo -e "${YELLOW}Creating public release documentation...${NC}"
cat > docs/RELEASE_NOTES_V2.md << 'EOF'
# AGET v2.0 Release Notes

## Release Date
October 7, 2025

## What's New in v2.0

### Major Features
- **Pattern-based architecture**: Reusable workflow patterns
- **Enhanced CLI**: `aget init`, `aget apply`, `aget list` commands
- **Multiple templates**: Choose from minimal, standard, or advanced
- **Session management**: Improved state tracking and recovery
- **Better compatibility**: Works with Claude Code, Cursor, Aider, Windsurf

### Improvements
- 60-second setup (measured and verified)
- Sub-second command response times
- Zero external dependencies
- Full backward compatibility

### Templates Available
- **minimal**: Basic setup for simple projects
- **standard**: Recommended for most projects
- **advanced**: Full feature set for complex projects

## Migration from v1

See [MIGRATE_TO_V2.md](MIGRATE_TO_V2.md) for detailed instructions.

## Support

Report issues: https://github.com/gmelli/aget-cli-agent-template/issues

---
*Making CLI agents better collaborators*
EOF

# Create summary of what was moved
echo -e "${YELLOW}Creating migration summary...${NC}"
cat > "$TARGET_DIR/MIGRATION_SUMMARY.md" << EOF
# Files Moved from Public to Private Repository
Date: $(date)

## Files Moved to $TARGET_DIR

### Test Documentation
$(ls -1 "$TARGET_DIR"/*DAY_* 2>/dev/null | xargs -n1 basename)
$(ls -1 "$TARGET_DIR"/*TEST* 2>/dev/null | xargs -n1 basename)

### Session Notes
$([ -d "$TARGET_DIR/SESSION_NOTES" ] && echo "SESSION_NOTES/ directory moved")

### Archives
$(ls -1 "$TARGET_DIR/archive_$TIMESTAMP/" 2>/dev/null | wc -l) files archived

## Next Steps
1. cd $AGET_AGET_DIR
2. git add aget-cli-agent-template-dev/
3. git commit -m "Archive internal development docs from aget-cli-agent-template"
4. git push

## Then in aget-cli-agent-template:
1. git add -A
2. git commit -m "cleanup: Move internal docs to private repo for release"
3. git push
EOF

echo ""
echo -e "${GREEN}=== Cleanup Complete ===${NC}"
echo "Files moved to: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "1. Review what was moved: ls $TARGET_DIR"
echo "2. Commit in aget-aget: cd $AGET_AGET_DIR && git add ."
echo "3. Commit here: git add -A && git commit -m 'cleanup: Pre-release documentation'"
echo ""
echo -e "${YELLOW}Run verification script to ensure ready for release:${NC}"
echo "  ./scripts/verify_public_ready.sh"