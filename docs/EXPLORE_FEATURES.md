# AGET Enhancement Proposals

This document tracks enhancement proposals for the AGET framework based on real-world migration experiences.

## Status: Active Proposals

### EP-1: Discovery Mechanism
**Status**: Proposed
**Priority**: High
**Category**: Migration Tools

Auto-detect existing patterns in codebases during migration.

**Features**:
- Scan for existing automation scripts
- Detect common trigger phrases
- Identify pattern-like structures
- Map script dependencies

**Example**:
```bash
aget discover --scan .
# Output: Found potential patterns in scripts/, docs/
```

### EP-2: Migration Assistant
**Status**: Proposed
**Priority**: High
**Category**: Migration Tools

Interactive wizard for step-by-step migrations.

**Features**:
- Backup creation and checkpoints
- Migration order suggestions
- Phase validation
- Rollback capabilities
- Migration reports

### EP-3: Compatibility Layers
**Status**: Proposed
**Priority**: Medium
**Category**: Migration Tools

Support for legacy script wrapping during transitions.

**Features**:
- Auto-generate wrapper scripts
- Maintain backward compatibility
- Gradual deprecation support
- Usage tracking

### EP-4: Meta Patterns
**Status**: Implemented (Partial)
**Priority**: Medium
**Category**: Patterns

Manage multiple projects within meta-repositories.

**Implementation**: See `patterns/meta/project_scanner.py`

**Features**:
- Project discovery and scanning ✅
- Bulk operations (planned)
- Cross-project pattern sharing (planned)
- Differential AGET versions (planned)

### EP-5: Pattern Versioning
**Status**: Proposed
**Priority**: Low
**Category**: Core Framework

Track pattern evolution across migrations.

**Features**:
- Version tracking per pattern
- Breaking change documentation
- Incremental migration support
- Independent rollback capability

### EP-6: AGET Version Tracking
**Status**: Implemented
**Priority**: High
**Category**: Core Framework

Track AGET version in repositories.

**Implementation**: `.aget/version.json` and AGENTS.md headers

### EP-7: Project Scanner Pattern
**Status**: Implemented
**Priority**: High
**Category**: Meta Patterns

Scan multi-project repositories for AGET status.

**Implementation**: `patterns/meta/project_scanner.py`

### EP-8: Testing Infrastructure
**Status**: Implemented (Partial)
**Priority**: High
**Category**: Quality Assurance

Standardized testing for AGET components.

**Features**:
- Unit tests ✅
- Integration tests ✅
- Coverage reporting (planned)
- CI/CD integration (planned)

### EP-9: CLI Enhancement Arguments
**Status**: Proposed
**Priority**: Medium
**Category**: User Experience

Common CLI arguments across all patterns.

**Standard Arguments**:
- `--quiet/-q` for minimal output
- `--verbose/-v` for debug info
- `--json` for machine-readable output
- `--dry-run` for safe preview
- `--no-save` to skip persistence

### EP-10: Pattern Documentation Standards
**Status**: Proposed
**Priority**: Medium
**Category**: Documentation

Consistent documentation for all patterns.

**Requirements**:
- Docstrings with exit codes
- Usage examples
- CLI argument docs
- Test coverage requirements
- Integration points

### EP-11: Migration Artifact Cleanup Pattern
**Status**: Proposed
**Priority**: High
**Category**: Housekeeping

Automated cleanup of migration leftovers.

**Target Artifacts**:
- Backup files (*.backup, *.original)
- Orphaned session files
- Deprecated configurations
- Old scripts

**Implementation Ideas**:
- `patterns/housekeeping/migration_cleanup.py`
- `.aget/backups/` directory management
- Artifact detection patterns

### EP-12: Directory Organization Standards
**Status**: Proposed
**Priority**: High
**Category**: Standards

Standard directory structure for AGET projects.

**Structure**:
```
.aget/
├── backups/    # Migration and version backups
├── cache/      # Temporary caches
├── logs/       # Operation logs
└── state/      # State files
```

## Implementation Priority

1. **Immediate** (Already in progress):
   - EP-4: Meta Patterns (partial)
   - EP-6: Version Tracking
   - EP-7: Project Scanner
   - EP-8: Testing Infrastructure (partial)

2. **Next Phase**:
   - EP-1: Discovery Mechanism
   - EP-2: Migration Assistant
   - EP-11: Migration Cleanup
   - EP-12: Directory Standards

3. **Future**:
   - EP-3: Compatibility Layers
   - EP-5: Pattern Versioning
   - EP-9: CLI Standards
   - EP-10: Documentation Standards

### EP-13: Data Management Patterns
**Status**: Proposed
**Priority**: High
**Category**: Infrastructure Patterns

Standardized patterns for database consolidation and management.

**Features**:
- Unified database schema patterns
- Thread-safe connection pooling
- Automatic migration support
- Backward compatibility adapters
- Operation context tracking

**Example Implementation**: See UNIFIED_TRACKING_SPECS_FOR_AGET.md

**Benefits**:
- Reduce database proliferation
- Simplify backup/recovery
- Enable cross-domain reporting
- Maintain backward compatibility

### EP-14: Architectural Decision Records (ADR) Pattern
**Status**: Implemented
**Priority**: High
**Category**: Documentation Patterns

Industry-standard ADR pattern for documenting architectural decisions.

**Features**:
- Michael Nygard template format
- Status lifecycle management
- CLI agent awareness integration
- Review process guidelines
- Cross-reference support

**Implementation**: patterns/adr/

**Benefits**:
- Prevents repeated rejected proposals
- Documents rationale for constraints
- Creates institutional memory for agents
- Improves decision transparency
- Based on AWS/Microsoft best practices

## Contributing

To propose a new enhancement:
1. Add to this document with EP-{number}
2. Include: Status, Priority, Category
3. Describe the need and use case
4. Provide implementation ideas
5. Submit PR to aget-cli-agent-template

---
*Last Updated: 2025-09-22*
*Based on: Real-world AGET migration experiences*