# Next Session Plan - Gate 3 Migration Tools

**Created**: 2025-09-24
**Target**: Gate 3 - Migration Tools (v1→v2)
**Estimated Duration**: 8-10 hours

## Key Learning from Gate 2
**Always explore before building** - Much of the infrastructure already existed, just needed wiring. This saved time but could have saved more with better discovery.

## Gate 3 Incremental Plan

### Phase 0: Discovery & Audit (20 min) - ALWAYS FIRST
```bash
# Search for existing migration code
grep -r "migrate\|migration\|upgrade\|v1.*v2" --include="*.py"
find . -name "*migrat*" -o -name "*upgrade*"

# Check backup infrastructure
ls -la aget/config/commands/rollback.py
ls -la .aget/backups/

# Identify v1 patterns
find . -name "session_protocol.py"
```

### Phase 1: Complete Gate 2 - Validate Command (30 min)
- Create `aget/config/commands/validate.py`
- Check AGENTS.md syntax and structure
- Verify pattern references are valid
- Add tests

### Phase 2: Migration Assessment Tool (45 min)
- Create `aget/migration/assessor.py`
- Detect v1 file patterns
- Calculate risk score
- Generate compatibility report

### Phase 3: Backup System Enhancement (30 min)
- Enhance backup for migration scenarios
- Full project snapshot capability
- Restore verification

### Phase 4: Compatibility Checker (30 min)
- Python version requirements
- Breaking change detection
- Dependency analysis

### Phase 5: Migration Planner (30 min)
- Generate step-by-step plans
- Multiple strategy options
- Time estimates

### Phase 6: Core Migration Engine (60 min)
- CLAUDE.md → AGENTS.md conversion
- Directory structure updates
- Pattern transformation

### Phase 7: Custom Script Porter (45 min)
- Convert v1 scripts to v2 patterns
- Preserve customizations
- Generate tests

### Phase 8: Configuration Merger (30 min)
- Intelligent config merging
- Conflict resolution
- Data preservation

### Phase 9: Validation & Testing (45 min)
- Post-migration verification
- Feature parity checks
- Comprehensive test suite

### Phase 10: Documentation & Polish (30 min)
- Migration guide
- Example migrations
- Error recovery

## Success Criteria for Gate 3

- [ ] Migration completes in <60 seconds
- [ ] Zero data loss during migration
- [ ] All v1 functionality preserved
- [ ] Rollback works 100% reliably
- [ ] 5+ successful test migrations
- [ ] <2 second command performance

## New Development Principles

1. **Discovery First**
   - Always audit before implementing
   - Check for existing solutions
   - Document what actually exists

2. **Test-Driven Discovery**
   - Write test for desired functionality
   - Run test to find existing implementations
   - Only build if truly needed

3. **Progressive Enhancement**
   - Enhance existing code where possible
   - Build new only when necessary
   - Wire components together

## Commands for Next Wake

```bash
# Wake up
python3 scripts/aget_session_protocol.py wake

# Read this plan
cat .aget/evolution/2025-09-24-next-session-plan.md

# Start discovery audit
grep -r "migrate" --include="*.py" | head -20

# Check Gate 2 status
python3 -m pytest tests/test_gate2_features.py -v
```

## Risk Mitigation

- **If migration code exists**: Reduce implementation phases, focus on enhancement
- **If starting from scratch**: May need full 10 hours
- **If complex customizations found**: Add buffer time for edge cases

## Notes for Next Agent

- Gate 2 is 7/8 complete (validate command pending)
- All pattern commands working (apply, list)
- 8 patterns available and functional
- Tests comprehensive and passing
- Performance excellent (<0.5s for all operations)

---
*Ready for Gate 3 implementation with discovery-first approach*