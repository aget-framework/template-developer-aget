# Internal Documentation Migration Plan

## Overview
Migrate internal development docs from `aget-cli-agent-template` (public) to `aget-aget` (private) with improved organization.

## Phase 1: Structure Design for aget-aget

### Proposed Directory Structure
```
aget-aget/
├── testing/
│   ├── v2_release/            # Current v2.0 release testing
│   │   ├── DAY_01_RESULTS.md  # Clear test outcome docs
│   │   ├── DAY_01_TEST_PLAN.md
│   │   ├── DAY_02_RESULTS.md
│   │   ├── DAY_02_TEST_PLAN.md
│   │   ├── DAY_03_PREVIEW.md
│   │   └── TEST_MATRIX.md
│   ├── protocols/
│   │   ├── CURSOR_TESTING_PROTOCOL.md
│   │   └── TRANSITION_SUITE.md
│   └── plans/
│       ├── V2_INCREMENTAL_PLAN.md
│       └── V2_RELEASE_PLAN.md
├── sessions/                  # Renamed from SESSION_NOTES
│   ├── 2025-09/
│   │   ├── week-38/          # Optional week-based grouping
│   │   ├── week-39/
│   │   └── SUMMARY.md        # Monthly summary
│   └── archive/              # Sessions older than 30 days
├── development/
│   ├── roadmaps/
│   ├── decisions/            # Internal ADRs
│   └── metrics/              # Hours tracking, performance
└── projects/                 # Test project tracking
    ├── spotify-aget/
    ├── llm-judge-aget/
    └── test_results/
```

## Phase 2: Renaming Strategy

### Current → New Name Mapping (Preserving ALL-CAPS for Documentation)
- `DAY_1_STATUS.md` → `DAY_01_RESULTS.md` (ALL-CAPS, clearer purpose)
- `DAY_1_TEST_PLAN.md` → `DAY_01_TEST_PLAN.md` (keep TEST_PLAN clear)
- `DAY_2_STATUS.md` → `DAY_02_RESULTS.md`
- `DAY_2_TEST_PLAN.md` → `DAY_02_TEST_PLAN.md`
- `DAY_3_PREVIEW.md` → `DAY_03_PREVIEW.md` (consistent numbering)
- `MIGRATION_TEST_MATRIX.md` → `TEST_MATRIX.md` (remove redundant prefix)
- `V2_INCREMENTAL_TEST_PLAN.md` → `V2_INCREMENTAL_PLAN.md`
- `V2_RELEASE_TEST_PLAN.md` → `V2_RELEASE_PLAN.md`
- `CURSOR_TEST_PROTOCOL.md` → `CURSOR_TESTING_PROTOCOL.md`
- `TRANSITION_TEST_SUITE.md` → `TRANSITION_SUITE.md`
- `SESSION_NOTES/` → `sessions/` (lowercase directory, caps for docs within)

### Naming Conventions (Following AGET Standards)
- **Documentation files**: ALL_CAPS with underscores (visual authority)
- **Directories**: lowercase with underscores (Unix standard)
- **Code files**: lowercase with underscores (Python standard)
- **Benefits of ALL-CAPS for docs**:
  - Visual hierarchy - docs stand out from code
  - Unix tradition (README, LICENSE, CHANGELOG)
  - Instant recognition as documentation
  - Easier to spot in file listings

## Phase 3: Migration Steps

### Step 1: Prepare aget-aget structure (Day 1)
```bash
# In aget-aget repo
mkdir -p testing/{v2_release,protocols,plans}
mkdir -p sessions/{2025-09,archive}
mkdir -p development/{roadmaps,decisions,metrics}
mkdir -p projects/{spotify-aget,llm-judge-aget,test_results}
```

### Step 2: Create migration script (Day 1)
Create `scripts/migrate_internal_docs.sh` that:
1. Copies files with new names
2. Preserves git history (using git mv when possible)
3. Updates any cross-references
4. Creates redirect notes in original locations

### Step 3: Test migration (Day 2)
1. Dry-run the migration script
2. Verify all references are updated
3. Check for broken links
4. Test in a temporary branch first

### Step 4: Execute migration (Day 2-3)
```bash
# Phase A: Non-breaking moves (Day 2)
- Move test plans and results
- Move SESSION_NOTES
- Add .gitignore entries

# Phase B: Update references (Day 2)
- Update any docs that reference moved files
- Add migration notes to moved file locations

# Phase C: Final cleanup (Day 3)
- Remove migrated files from public repo
- Update PUBLIC_VS_PRIVATE_REPOS.md
- Commit with clear message
```

### Step 5: Post-migration (Day 3)
1. Verify public repo is clean
2. Update CI/CD if needed
3. Document new location in aget-aget README
4. Create "stub" references if needed

## Phase 4: Automation

### Create ongoing sync process
```python
# scripts/sync_internal_docs.py
# Automatically detect and move internal docs
# Run as pre-commit hook or GitHub Action
```

### File patterns to auto-migrate
```yaml
patterns:
  - "**/DAY_*.md"
  - "**/*_STATUS.md"
  - "**/*_TEST_*.md"
  - "**/SESSION_NOTES/**"
  - "**/*hours*.md"
```

## Benefits of This Approach

1. **Cleaner public repo**: Only user-facing documentation
2. **Better organization**: Logical grouping by purpose
3. **Improved navigation**: Week-based sessions, category-based tests
4. **Consistent naming**: Modern conventions (kebab-case)
5. **Maintainable**: Clear separation of concerns
6. **Scalable**: Room for growth in each category

## Risk Mitigation

- **Broken links**: Create redirect stubs temporarily
- **Lost history**: Use git mv to preserve history
- **Missing docs**: Keep inventory checklist
- **Team confusion**: Clear communication, migration guide

## Success Criteria

- [ ] All internal docs moved to aget-aget
- [ ] No internal references in public repo
- [ ] Clean output from `grep -r "DAY_\|STATUS\|TEST_PLAN"`
- [ ] All team members aware of new locations
- [ ] Automation in place for future docs

## Timeline

- **Day 1**: Setup structure, create scripts
- **Day 2**: Test and execute migration
- **Day 3**: Cleanup and verification
- **Ongoing**: Automated sync process

---
*This plan ensures a clean separation while improving organization*