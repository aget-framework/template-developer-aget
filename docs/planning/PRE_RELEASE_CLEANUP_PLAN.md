# Pre-Release Documentation Cleanup Plan

**STATUS**: ✅ COMPLETED on 2025-09-25

## Overview
Internal development documentation has been successfully migrated to the private aget-aget meta-repository. This cleanup ensures users only see relevant documentation in the public repository.

## Repository Responsibilities

### aget-cli-agent-template (PUBLIC)
**Purpose**: The AGET framework users install
**Audience**: Developers using AGET
**Content**: Only user-facing documentation and code

### aget-aget (PRIVATE)
**Purpose**: Meta-repository for managing all aget projects
**Audience**: AGET maintainers only
**Content**: Internal development, test plans, migration tracking

## Files Moved (aget-cli-agent-template → aget-aget) ✅

### Phase 1: Test Documentation (COMPLETED)
- ✅ DAY_1_STATUS.md → testing/v2_release/DAY_01_RESULTS.md
- ✅ DAY_1_TEST_PLAN.md → testing/v2_release/DAY_01_TEST_PLAN.md
- ✅ DAY_2_STATUS.md → testing/v2_release/DAY_02_RESULTS.md
- ✅ DAY_2_TEST_PLAN.md → testing/v2_release/DAY_02_TEST_PLAN.md
- ✅ DAY_3_PREVIEW.md → testing/v2_release/DAY_03_PREVIEW.md
- ✅ V2_INCREMENTAL_TEST_PLAN.md → testing/plans/V2_INCREMENTAL_PLAN.md
- ✅ MIGRATION_TEST_MATRIX.md → testing/v2_release/TEST_MATRIX.md
- ✅ TRANSITION_TEST_SUITE.md → testing/protocols/TRANSITION_SUITE.md
- ✅ CURSOR_TEST_PROTOCOL.md → testing/protocols/CURSOR_TESTING_PROTOCOL.md
- ✅ docs/V2_RELEASE_TEST_PLAN.md → testing/plans/V2_RELEASE_PLAN.md

### Phase 2: Session Notes (COMPLETED)
- ✅ SESSION_NOTES/ → sessions/ (all historical notes migrated)

### Phase 3: Internal Sections (LOW PRIORITY)
Remove from public docs:
- References to spotify-aget, llm-judge-aget test projects
- Hours tracking in ROADMAP_v2.md
- Internal deadlines and commitments
- Test migration specifics

## Files to Keep (User-Facing)

### Core Documentation
```bash
README.md                    # Main user guide
CHANGELOG.md                 # User-visible changes
LICENSE                      # Legal requirement
CONTRIBUTING.md              # How to contribute
SECURITY.md                  # Security policy
```

### User Guides
```bash
docs/
├── GET_STARTED.md          # Quick start guide
├── MIGRATE_TO_V2.md        # Migration guide
├── UNDERSTAND_AGET.md      # Concepts
├── USE_COMMANDS.md         # Command reference
├── CHOOSE_TEMPLATE.md      # Template selection
└── TROUBLESHOOTING.md      # Common issues
```

### Technical Docs (Keep)
```bash
ARCHITECTURE.md              # System design
docs/PATTERNS.md            # Pattern documentation
docs/API.md                 # API reference
```

## Migration Script

```bash
#!/bin/bash
# move_to_aget_aget.sh

# Create target directory in aget-aget
AGET_AGET_DIR="~/github/aget-aget"
TARGET_DIR="$AGET_AGET_DIR/aget-cli-agent-template-dev"

mkdir -p $TARGET_DIR

# Move test documentation
mv DAY_*.md $TARGET_DIR/
mv V2_INCREMENTAL_TEST_PLAN.md $TARGET_DIR/
mv MIGRATION_TEST_MATRIX.md $TARGET_DIR/
mv TRANSITION_TEST_SUITE.md $TARGET_DIR/
mv SCRIPT_FIX_REPORT.md $TARGET_DIR/

# Move session notes
mv SESSION_NOTES $TARGET_DIR/

# Move internal test plan
mv docs/V2_RELEASE_TEST_PLAN.md $TARGET_DIR/

# Create public version of critical docs
cat > docs/RELEASE_PLAN.md << 'EOF'
# AGET v2.0 Release Plan

## Release Date
October 7, 2025

## What's New
- Pattern-based architecture
- Enhanced CLI commands
- Multiple template types
- Session management improvements

## Migration Guide
See [MIGRATE_TO_V2.md](MIGRATE_TO_V2.md)

## Breaking Changes
None - fully backward compatible

## Support
Report issues at: https://github.com/gmelli/aget-cli-agent-template/issues
EOF

echo "Files moved to $TARGET_DIR"
echo "Remember to commit in both repos"
```

## Cleanup Checklist

### Before Release (Oct 5-6)
- [ ] Run migration script
- [ ] Verify public repo has only user docs
- [ ] Update README with clean examples
- [ ] Remove internal project references
- [ ] Clean git history if needed
- [ ] Test fresh clone experience

### Public Repo Should Answer
- How do I install AGET?
- How do I use AGET?
- What templates are available?
- How do I migrate from v1?
- Where do I report issues?

### Public Repo Should NOT Contain
- Our test project names
- Daily status reports
- Internal planning documents
- Hour tracking
- Test migration results
- Session notes

## Validation Test

```bash
# Clone fresh copy as a user would
cd /tmp
git clone https://github.com/gmelli/aget-cli-agent-template.git
cd aget-cli-agent-template

# Should only see user-relevant files
ls *.md
# Expected: README.md, CHANGELOG.md, LICENSE, etc.
# NOT: DAY_1_STATUS.md, MIGRATION_TEST_MATRIX.md, etc.

# Docs should be user-focused
ls docs/*.md
# Expected: GET_STARTED.md, MIGRATE_TO_V2.md, etc.
# NOT: V2_RELEASE_TEST_PLAN.md
```

## Timeline

### Sept 26-30: Continue Testing
- Keep test docs in aget-cli-agent-template for now
- Continue documenting in current location

### Oct 1-4: Documentation Polish
- Create final user documentation
- Polish README and guides

### Oct 5-6: Pre-Release Cleanup
- **CRITICAL**: Run migration script
- Move all internal docs to aget-aget
- Clean public repo
- Validate user experience

### Oct 7: Release
- Public repo contains only user-facing content
- Internal development continues in aget-aget

## Why This Matters

1. **User Experience**: Users shouldn't see our internal development chaos
2. **Professionalism**: Clean, focused documentation looks professional
3. **Maintenance**: Separation makes both repos easier to maintain
4. **Security**: No accidental exposure of internal information
5. **Clarity**: Users find what they need without distraction

## Migration Verification

After moving files, verify:

```bash
# In aget-cli-agent-template (PUBLIC)
find . -name "*DAY_*" -o -name "*TEST_PLAN*" -o -name "*STATUS.md"
# Should return: No results

# In aget-aget (PRIVATE)
ls aget-cli-agent-template-dev/
# Should contain: All test docs, session notes, internal plans
```

---
*Created: September 25, 2025*
*Critical for: October 7, 2025 release*
*Status: MUST COMPLETE before going public*