# ADR-012: Migration Strategy and Script Inclusion

**Date**: 2025-09-28
**Status**: Accepted
**Context**: Version migration strategy for AGET framework
**Decision**: Include battle-tested migration scripts in releases

## Context

During v2.0→v2.1 migration, we successfully migrated 9 production agents but encountered several edge cases:
- Version string variations (2.0.0-alpha)
- Missing directories
- Symlink complications
- Field name inconsistencies
- Already-migrated patterns

These real-world issues provided valuable insights into migration requirements.

## Decision

We will include battle-tested migration scripts as first-class release artifacts, following this strategy:

### 1. Migration Scripts Are Release Artifacts
Every release will include:
```
scripts/migrations/
├── README.md                    # Migration guide
├── v1.0_to_v2.0.py             # Historical migrations
├── v2.0_to_v2.1.py             # Current migration
└── pre_migration_check.py      # Validation tool
```

### 2. Migration Development Pipeline
```
Development → Testing → Battle-Testing → Refinement → Release
     ↓           ↓            ↓              ↓           ↓
Create script  Test on    Real agents   Fix issues   Include
              dummies    (edge cases)               in release
```

### 3. Migration Script Requirements
Every migration script must:
- Create backups before changes
- Be idempotent (safe to run multiple times)
- Handle common edge cases
- Provide detailed reporting
- Support rollback

### 4. Version Compatibility Rules
- Direct migrations only between consecutive major/minor versions
- Patch versions (2.1.0→2.1.1) require no migration
- Skip-version migrations (2.0→2.2) must go through intermediate versions

## Consequences

### Positive
- **Reliability**: Battle-tested scripts reduce migration failures
- **Confidence**: Users can migrate knowing edge cases are handled
- **Traceability**: Migration records provide audit trail
- **Learning**: Each migration improves the next
- **Rollback**: Backup strategy allows safe experimentation

### Negative
- **Maintenance**: Migration scripts need updates for edge cases
- **Testing**: Requires testing infrastructure for migrations
- **Complexity**: More code to maintain in releases
- **Storage**: Backup directories consume disk space

### Neutral
- Migration scripts become part of version control history
- Documentation requirements increase
- Release process includes migration validation

## Implementation

### Phase 1: v2.1 Release (Current)
- [x] Include v2.0→v2.1 migration script
- [x] Document lessons learned
- [x] Create this ADR

### Phase 2: v2.2 Planning
- [ ] Create pre-migration validator
- [ ] Implement batch migration capability
- [ ] Build migration test suite

### Phase 3: Long-term
- [ ] Automated migration testing in CI/CD
- [ ] Migration compatibility matrix
- [ ] Rollback automation

## Examples

### Successful v2.0→v2.1 Migration
```bash
# Migration with automatic handling of:
python3 scripts/aget_v20_to_v21_migration.py
- Version variations (2.0.0-alpha)
- Missing directories (auto-created)
- Pattern renaming (aget_ prefix)
- Backup creation
- CLAUDE.md updates
```

### Future v2.1→v2.2 Migration
```bash
# Pre-flight check
python3 scripts/migrations/pre_migration_check.py --to 2.2

# Batch migration
python3 scripts/migrations/v2.1_to_v2.2.py --batch "my-*-aget"

# With rollback capability
python3 scripts/migrations/v2.1_to_v2.2.py --rollback
```

## Related Documents
- [MIGRATION_LESSONS_LEARNED.md](../docs/MIGRATION_LESSONS_LEARNED.md)
- [v2.1.0-RELEASE.md](../docs/v2.1.0-RELEASE.md)
- [Migration Scripts](../scripts/migrations/)

## Decision Outcome

**Accepted**: Migration scripts are now considered essential release artifacts. The v2.0→v2.1 experience proves that battle-testing on production agents reveals critical edge cases that improve migration reliability.

Future releases will follow the migration pipeline: develop → test → battle-test → refine → release.

---
*Signed off by: AGET Architecture Team*
*Review date: 2025-09-28*