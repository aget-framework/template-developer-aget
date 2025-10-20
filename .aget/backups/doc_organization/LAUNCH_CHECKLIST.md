# AGET v2.0 Launch Checklist

**Current Status**: v2.0-alpha released (Gate 1 complete)
**Next Target**: v2.0-beta (Gate 2)

## Pre-Beta Checklist
- [ ] Pattern library working (5+ patterns)
- [ ] All 5 commands functional (not just placeholders)
- [ ] No secrets/keys in code
- [ ] LICENSE file exists (MIT)
- [ ] Core functionality tested (init, rollback, patterns)
- [ ] README updated for v2.0

## Security Check
```bash
# Run before any release
grep -r "api[_-]key\|secret\|token\|password" --include="*.py" --include="*.md" .
python3 scripts/security_check.py
```

## v2.0-beta Launch (Gate 2)
1. Complete Sprint 002 goals
2. Tag v2.0-beta
3. Share with 3-5 developers
4. Test on low-risk projects

## v2.0-rc Launch (Gate 4)
1. Migration tools ready
2. Documentation complete
3. Tag v2.0-rc
4. Broader testing group

## v2.0 Public Launch (Gate 5)
1. Full test coverage
2. Cross-platform validated
3. Tag v2.0
4. Public announcement

## Success Criteria
- Patterns installable and working
- Performance <2 seconds maintained
- No breaking changes for existing projects
- Clear migration path from v1

---
*Note: This aligns with gate-based release strategy (ADR-005)*