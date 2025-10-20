# ARCH-001: Self-Contained Project Architecture

**Date**: 2025-09-27
**Status**: Accepted
**Deciders**: Gabor Melli, my-AGET-aget
**Category**: Core Architecture
**Confidence**: Very High
**Supersedes**: Implicit dependency assumptions

## Context

Discovery of systemic path dependency issues revealed that AGET projects were referencing parent directory resources using relative paths. When `smart_reader.py` was referenced but didn't exist locally, sessions failed with 8-10 tool calls instead of 2-3.

Investigation revealed:
- Scripts copied from parent assumed parent file structure
- No pattern synchronization mechanism existed
- Changes in parent repositories could break child projects
- Documentation referenced non-existent local files

This violates AGET's core promise of reliable, predictable agent behavior.

## Decision

**Every AGET project MUST be completely self-contained with no runtime dependencies on external directories.**

### Three Pillars

1. **Self-Contained Islands**
   - Each AGET contains ALL files it needs to operate
   - No runtime references to parent/sibling directories
   - Complete portability - project can be moved/zipped/shared

2. **Intentional Upgrades**
   - Pattern/script updates require explicit action
   - Version tracking in `.aget/dependencies.json`
   - AGET can request: "I need pattern X updated"
   - No automatic inheritance of changes

3. **Fail-Fast on Missing**
   - Missing dependencies halt execution immediately
   - Clear error messages identify what's missing
   - No silent degradation or fallbacks

## Implementation

### Required Components

```
my-aget/
├── .aget/
│   └── dependencies.json    # Manifest of all dependencies
├── patterns/                # Local copies of all patterns
│   ├── documentation/
│   │   └── smart_reader.py  # Copied, not referenced
│   └── meta/
│       └── project_scanner.py
├── scripts/
│   ├── install_pattern.py   # Copies patterns locally
│   └── verify_dependencies.py
└── ARCH-001-SELF-CONTAINED.md
```

### Dependency Manifest Structure

```json
{
  "architecture": "self-contained",
  "upgrade_policy": "intentional",
  "failure_mode": "fail-fast",
  "required_patterns": [
    {
      "name": "documentation/smart_reader.py",
      "version": "1.0.0",
      "status": "installed",
      "installed_from": "source_path",
      "installed_date": "ISO-8601"
    }
  ]
}
```

## Compatibility Analysis

### Aligns With

- **ADR-001 (Scope Boundaries)**: Self-containment keeps AGET focused on conversation layer
- **ADR-004 (Three-Tier Degradation)**: Each tier operates within self-contained boundaries
- **ADR-006 (Repo Separation)**: Single repo recommendation supports self-containment
- **ADR-007 (Test Requirements)**: Self-contained projects are easier to test in isolation

### Enhances

- **ADR-003 (V2 Charter)**: Reliability commitment strengthened by eliminating external dependencies
- **ADR-005 (Gate-Based Releases)**: Each gate validates self-containment
- **ADR-008 (Quality Agent)**: Can verify self-containment as quality check

### No Conflicts Identified

This architecture decision strengthens existing ADRs without contradiction.

## Consequences

### Positive
- ✅ **Complete independence** - No external failure modes
- ✅ **Predictable behavior** - What you see is what runs
- ✅ **Version control** - Every dependency tracked
- ✅ **Portable** - Entire project moveable as unit
- ✅ **Testable** - No hidden dependencies
- ✅ **Reliable** - Matches ADR-004's reliability goals

### Negative
- ❌ **Storage overhead** - Patterns duplicated across projects
- ❌ **Update burden** - Manual propagation required
- ❌ **Potential drift** - Projects may diverge over time

### Mitigations
1. **Pattern registry** - Central catalog of available patterns
2. **Update tooling** - `install_pattern.py` simplifies updates
3. **Version tracking** - Clear versioning prevents confusion
4. **aget-AGET-aget** - Meta-agent manages updates across projects

## Validation

A project is self-contained when:
- [ ] No code references parent directories (`../` or `/Users/`)
- [ ] All patterns exist in local `patterns/` directory
- [ ] Dependencies.json lists all external sources
- [ ] `verify_dependencies.py` passes
- [ ] Project works when copied to new location
- [ ] Wake protocol uses local resources first

## Migration Path

For existing projects:
1. Run `python3 scripts/install_pattern.py` to copy dependencies
2. Update path references to use local files
3. Test in isolated environment
4. Commit with message: "arch: Implement self-contained architecture (ARCH-001)"

## Decision Trace

- **Problem**: Path dependency failures (8-10 tools vs 2-3)
- **Analysis**: 5-why revealed no synchronization mechanism
- **Options**: Shared libraries vs self-contained vs hybrid
- **Choice**: Self-contained for maximum reliability
- **Validation**: Session now uses 3 tools with local patterns

## References

- DISC-2025-09-27-path-dependency-issue.md
- DEC-2025-09-27-self-contained-architecture.md
- Session efficiency improved 70% after implementation

---
*Architecture decisions shape the fundamental structure of AGET projects*