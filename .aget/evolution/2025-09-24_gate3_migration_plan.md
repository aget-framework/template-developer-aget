# Gate 3: Migration Tools - Enhanced Implementation Plan
*Created: 2025-09-24*
*Status: Active*
*Estimated Time: 8-10 hours*

## Core Principle: Discovery Before Building

```python
def should_implement(feature):
    """Core development principle for Gate 3"""
    existing = search_codebase(feature)
    if existing and working:
        return "wire_it"
    elif existing and broken:
        return "fix_it"
    else:
        return "build_it"
```

## Phase 0: Discovery & Audit (20 min)

### Objective
Understand existing migration infrastructure before building

### Tasks
1. **Search for existing migration code:**
   ```bash
   grep -r "migrate\|migration\|upgrade\|v1.*v2" --include="*.py"
   find . -name "*migrat*" -o -name "*upgrade*"
   ```

2. **Check backup/rollback infrastructure:**
   - Review `aget/config/commands/rollback.py`
   - Check `.aget/backups/` handling
   - Look for version tracking in `.aget/version.json`

3. **Identify v1 pattern files:**
   - List all v1 template files (`session_protocol.py`, etc.)
   - Check CLAUDE.md vs AGENTS.md handling

4. **Document findings:**
   - Create `.aget/evolution/migration-audit.md`

### Success Criteria
Clear map of what exists vs what's needed

### Checkpoint
```bash
git commit -m "docs: migration infrastructure audit"
```

---

## Phase 1: Complete Gate 2 - Validate Command (30 min)

### Objective
Finish Gate 2 requirement before moving to Gate 3

### Tasks
1. **Create `aget/config/commands/validate.py`:**
   - Check AGENTS.md syntax
   - Verify required sections exist
   - Validate pattern references are valid
   - Check for conflicting patterns

2. **Wire to ConfigModule**

3. **Add tests to `test_gate2_features.py`**

4. **Test validation on good and bad configs**

### Success Criteria
`aget validate` prevents broken configs

### Checkpoint
```bash
git commit -m "feat: implement aget validate command"
```

---

## Phase 2: Migration Assessment Tool (45 min)

### Objective
Analyze v1 projects and assess complexity

### Tasks
1. **Create `aget/migration/assessor.py`:**
   - Detect v1 file patterns
   - Identify customizations vs standard
   - Calculate risk score (0-100)
   - Generate compatibility report

2. **Create `aget/config/commands/check.py`:**
   - Wire to assessor
   - Format output nicely
   - Support JSON output with `--json` flag

3. **Test on:**
   - Standard v1 project
   - Heavily customized v1 project
   - Non-AGET project

### Success Criteria
Accurate assessment of 3 project types

### Checkpoint
```bash
git commit -m "feat: migration assessment tool"
```

---

## Phase 3: Backup System Enhancement (30 min)

### Objective
Robust backup before migration

### Tasks
1. **Enhance `aget/migration/backup.py`:**
   - Full project snapshot to `.aget/migration_backup/`
   - Manifest with checksums
   - Compression option
   - Version tagging

2. **Add to rollback command:**
   - `aget rollback --list-migrations`
   - `aget rollback --from-migration <id>`

3. **Test backup/restore cycle:**
   - Backup → modify → restore
   - Verify file integrity

### Success Criteria
100% restoration accuracy

### Checkpoint
```bash
git commit -m "feat: enhanced backup for migration"
```

---

## Phase 4: Compatibility Checker (30 min)

### Objective
Identify breaking changes before migration

### Tasks
1. **Create `aget/migration/compatibility.py`:**
   - Python version check (≥3.8)
   - Check for conflicting files
   - Identify import dependencies
   - Detect custom script patterns

2. **Generate report:**
   - Breaking changes list
   - Required manual interventions
   - Risk assessment by component

3. **Test with edge cases:**
   - Python 3.7 project
   - Conflicting file names
   - Complex customizations

### Success Criteria
No false negatives on breaking changes

### Checkpoint
```bash
git commit -m "feat: migration compatibility checker"
```

---

## Phase 5: Migration Planner (30 min)

### Objective
Generate step-by-step migration plan

### Tasks
1. **Create `aget/migration/planner.py`:**
   - Analyze assessment + compatibility
   - Generate ordered steps
   - Identify rollback points
   - Estimate time required

2. **Output formats:**
   - Human-readable plan
   - Machine-executable JSON
   - Markdown report

3. **Plan variations:**
   - Minimal (preserve everything)
   - Standard (update to v2 patterns)
   - Clean (remove deprecated)

### Success Criteria
Clear, actionable plans

### Checkpoint
```bash
git commit -m "feat: migration planner"
```

---

## Phase 6: Core Migration Engine (60 min)

### Objective
Execute the actual migration

### Tasks
1. **Create `aget/migration/migrator.py`:**
   - Read migration plan
   - Execute transformations:
     - CLAUDE.md → AGENTS.md
     - scripts/ → patterns/
     - Add outputs/, data/ dirs
   - Preserve customizations
   - Track progress

2. **Create `aget/config/commands/migrate.py`:**
   - Dry-run mode by default
   - Confirmation prompts
   - Progress bar
   - Detailed logging

3. **Handle special cases:**
   - Symlink preservation
   - Git hooks
   - CI/CD files

### Success Criteria
Successful migration of test projects

### Checkpoint
```bash
git commit -m "feat: core migration engine"
```

---

## Phase 7: Custom Script Porter (45 min)

### Objective
Convert v1 scripts to v2 patterns

### Tasks
1. **Create `aget/migration/script_porter.py`:**
   - Parse v1 Python scripts
   - Extract core logic
   - Wrap in pattern template
   - Preserve custom functions

2. **Pattern generation:**
   - Create apply_pattern function
   - Add pattern metadata
   - Generate tests

3. **Handle common customizations:**
   - Custom session messages
   - Additional checks
   - Project-specific commands

### Success Criteria
80% automatic conversion rate

### Checkpoint
```bash
git commit -m "feat: v1 script to v2 pattern converter"
```

---

## Phase 8: Configuration Merger (30 min)

### Objective
Merge v1 and v2 configurations

### Tasks
1. **Create `aget/migration/config_merger.py`:**
   - Parse CLAUDE.md sections
   - Map to AGENTS.md structure
   - Preserve custom triggers
   - Handle conflicts intelligently

2. **Merge strategies:**
   - Conservative (preserve all)
   - Balanced (modernize structure)
   - Aggressive (full v2 format)

3. **Conflict resolution:**
   - Interactive mode
   - Automatic with rules
   - Generate conflict report

### Success Criteria
No data loss during merge

### Checkpoint
```bash
git commit -m "feat: configuration merger"
```

---

## Phase 9: Validation & Testing (45 min)

### Objective
Ensure migration success

### Tasks
1. **Create `aget/migration/validator.py`:**
   - Post-migration checks
   - Verify all v1 commands work
   - Test pattern execution
   - Check file permissions

2. **Create comprehensive test suite:**
   - `tests/test_migration.py`
   - Test each migration phase
   - Edge cases and failures
   - Rollback scenarios

3. **Validation report:**
   - Feature parity check
   - Performance comparison
   - Breaking changes found

### Success Criteria
All v1 functionality preserved

### Checkpoint
```bash
git commit -m "test: migration validation suite"
```

---

## Phase 10: Documentation & Polish (30 min)

### Objective
User-ready migration experience

### Tasks
1. **Create `docs/MIGRATION_GUIDE.md`:**
   - Prerequisites
   - Step-by-step instructions
   - Common issues & solutions
   - FAQ

2. **Create example migrations:**
   - `examples/migration/simple/`
   - `examples/migration/complex/`

3. **Polish user experience:**
   - Better error messages
   - Helpful hints
   - Recovery instructions

### Success Criteria
Users can self-migrate successfully

### Checkpoint
```bash
git commit -m "docs: complete migration guide"
```

---

## Development Principles

### 1. Test-Driven Discovery
- Write test for desired functionality
- Run test to see if it passes
- Only implement if test fails

### 2. Progressive Enhancement
- Start with audit
- Enhance existing where possible
- Build new only when necessary

### 3. Documentation Sync
- Update docs immediately when finding existing features
- Keep "implemented features" list current
- Track gaps explicitly

## Session Start Protocol (Enhanced)

1. [ ] Run wake protocol
2. [ ] Read last evolution entry
3. [ ] **Run discovery audit**
4. [ ] Adjust plan based on findings
5. [ ] Create todo list from adjusted plan
6. [ ] Begin implementation

## Discovery Audit Commands

```bash
# Find existing implementations
find . -type f -name "*.py" | xargs grep -l "PATTERN"

# Check for TODO/FIXME/HACK markers
grep -r "TODO\|FIXME\|HACK" --include="*.py"

# List recent changes
git log --oneline -20

# Check test coverage
python -m pytest tests/ --cov=aget
```

## Time Allocation

**Total Estimated Time**: 8-10 hours

- Discovery: 0.5 hours (20 min)
- Gate 2 Completion: 0.5 hours (30 min)
- Core Migration (Phases 2-8): 5 hours
- Testing & Validation: 1.5 hours
- Documentation: 1 hour
- Buffer: 1.5 hours

## Success Metrics

### Efficiency Metrics
- Discovery time: <20% of session
- Redundant work: <10%
- Test coverage: >80%
- Documentation accuracy: >95%

### Quality Metrics
- No duplicate implementations
- All features documented
- Tests before implementation
- Clear migration path

### User Experience Metrics
- Migration time: <2 minutes
- Zero breaking changes
- Full rollback capability
- Self-service success rate: >90%

## Risk Mitigation

1. **Complexity Risk**: Start with minimal template, evolve as needed
2. **Time Risk**: Each phase has independent value
3. **Breaking Changes**: Comprehensive backup/rollback at each step
4. **User Confusion**: Clear documentation and examples

## Next Actions

1. Begin Phase 0: Discovery & Audit
2. Document all findings before building
3. Adjust plan based on discoveries
4. Implement only what's missing

---

*This plan incorporates lessons learned from Gate 2 implementation, emphasizing discovery before building to prevent redundant work and ensure efficient development.*