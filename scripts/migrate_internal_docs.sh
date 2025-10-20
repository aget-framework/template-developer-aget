#!/bin/bash
# Migration script for internal documentation
# Moves internal docs from aget-cli-agent-template to aget-aget

set -e  # Exit on error

# Configuration
SOURCE_REPO="."
TARGET_REPO="../aget-aget"
DRY_RUN=${1:-"--dry-run"}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Internal Documentation Migration Script${NC}"
echo "========================================="
echo "Mode: $DRY_RUN"
echo "Timestamp: $TIMESTAMP"
echo ""

# Check if aget-aget repo exists
if [ ! -d "$TARGET_REPO" ]; then
    echo -e "${RED}Error: Target repository $TARGET_REPO does not exist${NC}"
    echo "Please ensure aget-aget repository is cloned at ../aget-aget"
    exit 1
fi

# Function to show what will be done
show_action() {
    local action=$1
    local source=$2
    local target=$3
    if [ "$DRY_RUN" == "--dry-run" ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} $action: $source → $target"
    else
        echo -e "${GREEN}[EXECUTE]${NC} $action: $source → $target"
    fi
}

# Function to execute or simulate command
run_command() {
    local cmd=$1
    if [ "$DRY_RUN" == "--dry-run" ]; then
        echo -e "${YELLOW}  Would run:${NC} $cmd"
    else
        eval "$cmd"
    fi
}

echo -e "${BLUE}Step 1: Creating target directory structure${NC}"
echo "---------------------------------------------"

# Create directory structure in aget-aget
DIRECTORIES=(
    "testing/v2_release"
    "testing/protocols"
    "testing/plans"
    "sessions/2025-09"
    "sessions/archive"
    "development/roadmaps"
    "development/decisions"
    "development/metrics"
    "projects/spotify-aget"
    "projects/llm-judge-aget"
    "projects/test_results"
)

for dir in "${DIRECTORIES[@]}"; do
    show_action "Create directory" "-" "$TARGET_REPO/$dir"
    run_command "mkdir -p $TARGET_REPO/$dir"
done

echo ""
echo -e "${BLUE}Step 2: Migrating test documentation${NC}"
echo "--------------------------------------"

# Migration function for each file
migrate_file() {
    local source=$1
    local target=$2

    if [ -f "$SOURCE_REPO/$source" ]; then
        show_action "Move" "$source" "$TARGET_REPO/$target"
        run_command "cp '$SOURCE_REPO/$source' '$TARGET_REPO/$target'"

        # Create redirect note in original location
        if [ "$DRY_RUN" != "--dry-run" ]; then
            echo "# Document Moved" > "$SOURCE_REPO/$source.moved"
            echo "This document has been moved to the private aget-aget repository." >> "$SOURCE_REPO/$source.moved"
            echo "Location: $target" >> "$SOURCE_REPO/$source.moved"
            echo "Date: $(date +%Y-%m-%d)" >> "$SOURCE_REPO/$source.moved"
        fi
    else
        echo -e "${YELLOW}Warning: Source file not found: $source${NC}"
    fi
}

# Perform migrations
migrate_file "DAY_1_STATUS.md" "testing/v2_release/DAY_01_RESULTS.md"
migrate_file "DAY_1_TEST_PLAN.md" "testing/v2_release/DAY_01_TEST_PLAN.md"
migrate_file "DAY_2_STATUS.md" "testing/v2_release/DAY_02_RESULTS.md"
migrate_file "DAY_2_TEST_PLAN.md" "testing/v2_release/DAY_02_TEST_PLAN.md"
migrate_file "DAY_3_PREVIEW.md" "testing/v2_release/DAY_03_PREVIEW.md"
migrate_file "MIGRATION_TEST_MATRIX.md" "testing/v2_release/TEST_MATRIX.md"
migrate_file "V2_INCREMENTAL_TEST_PLAN.md" "testing/plans/V2_INCREMENTAL_PLAN.md"
migrate_file "docs/V2_RELEASE_TEST_PLAN.md" "testing/plans/V2_RELEASE_PLAN.md"
migrate_file "CURSOR_TEST_PROTOCOL.md" "testing/protocols/CURSOR_TESTING_PROTOCOL.md"
migrate_file "TRANSITION_TEST_SUITE.md" "testing/protocols/TRANSITION_SUITE.md"

echo ""
echo -e "${BLUE}Step 3: Migrating SESSION_NOTES${NC}"
echo "---------------------------------"

if [ -d "$SOURCE_REPO/SESSION_NOTES" ]; then
    show_action "Move directory" "SESSION_NOTES" "$TARGET_REPO/sessions"
    run_command "cp -r $SOURCE_REPO/SESSION_NOTES/* $TARGET_REPO/sessions/ 2>/dev/null || true"

    # Archive old sessions (>30 days)
    if [ "$DRY_RUN" != "--dry-run" ]; then
        find "$TARGET_REPO/sessions" -name "*.md" -mtime +30 -exec mv {} "$TARGET_REPO/sessions/archive/" \; 2>/dev/null || true
    fi
else
    echo -e "${YELLOW}Warning: SESSION_NOTES directory not found${NC}"
fi

echo ""
echo -e "${BLUE}Step 4: Creating migration inventory${NC}"
echo "-------------------------------------"

# Create inventory file
INVENTORY_FILE="$TARGET_REPO/MIGRATION_INVENTORY_$TIMESTAMP.md"
if [ "$DRY_RUN" != "--dry-run" ]; then
    cat > "$INVENTORY_FILE" << EOF
# Migration Inventory - $TIMESTAMP

## Files Migrated from aget-cli-agent-template

### Test Documentation
- DAY_1_STATUS.md → testing/v2_release/DAY_01_RESULTS.md
- DAY_1_TEST_PLAN.md → testing/v2_release/DAY_01_TEST_PLAN.md
- DAY_2_STATUS.md → testing/v2_release/DAY_02_RESULTS.md
- DAY_2_TEST_PLAN.md → testing/v2_release/DAY_02_TEST_PLAN.md
- DAY_3_PREVIEW.md → testing/v2_release/DAY_03_PREVIEW.md
- MIGRATION_TEST_MATRIX.md → testing/v2_release/TEST_MATRIX.md
- V2_INCREMENTAL_TEST_PLAN.md → testing/plans/V2_INCREMENTAL_PLAN.md
- docs/V2_RELEASE_TEST_PLAN.md → testing/plans/V2_RELEASE_PLAN.md
- CURSOR_TEST_PROTOCOL.md → testing/protocols/CURSOR_TESTING_PROTOCOL.md
- TRANSITION_TEST_SUITE.md → testing/protocols/TRANSITION_SUITE.md

### Session Notes
- SESSION_NOTES/ → sessions/

## Post-Migration Checklist
- [ ] Remove original files from public repo
- [ ] Update references in remaining docs
- [ ] Commit changes in both repos
- [ ] Update CI/CD configurations
- [ ] Notify team of new locations

## Verification Commands
\`\`\`bash
# Check for remaining internal docs in public repo
find . -name "DAY_*.md" -o -name "*_TEST_*.md" -o -name "*_STATUS.md"

# Verify no internal references
grep -r "DAY_[0-9]" --include="*.md" .
\`\`\`
EOF
    echo -e "${GREEN}Created inventory: $INVENTORY_FILE${NC}"
fi

echo ""
echo -e "${BLUE}Step 5: Cleanup commands for public repo${NC}"
echo "-----------------------------------------"

if [ "$DRY_RUN" == "--dry-run" ]; then
    echo -e "${YELLOW}After verifying the migration, run these commands:${NC}"
else
    echo -e "${GREEN}Run these commands to complete cleanup:${NC}"
fi

cat << EOF

# Remove migrated files
git rm DAY_*.md MIGRATION_TEST_MATRIX.md V2_INCREMENTAL_TEST_PLAN.md
git rm CURSOR_TEST_PROTOCOL.md TRANSITION_TEST_SUITE.md
git rm docs/V2_RELEASE_TEST_PLAN.md
git rm -r SESSION_NOTES/

# Add to .gitignore
echo "# Internal documentation (moved to aget-aget)" >> .gitignore
echo "DAY_*.md" >> .gitignore
echo "*_TEST_PLAN.md" >> .gitignore
echo "*_STATUS.md" >> .gitignore
echo "SESSION_NOTES/" >> .gitignore

# Commit changes
git add .
git commit -m "chore: Migrate internal docs to private aget-aget repo

- Moved test plans and results
- Moved session notes
- Added .gitignore entries for internal docs
- See INTERNAL_DOCS_MIGRATION_PLAN.md for details"

EOF

echo ""
if [ "$DRY_RUN" == "--dry-run" ]; then
    echo -e "${YELLOW}This was a dry run. To execute the migration, run:${NC}"
    echo "  ./scripts/migrate_internal_docs.sh --execute"
else
    echo -e "${GREEN}Migration complete!${NC}"
    echo "Please review the changes and run the cleanup commands above."
fi

echo ""
echo "Summary:"
echo "- Files to migrate: 10 documents + SESSION_NOTES/"
echo "- Target repo: $TARGET_REPO"
echo "- Mode: $DRY_RUN"