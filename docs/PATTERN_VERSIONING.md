# Pattern Versioning System

**Version:** 1.0.0
**Status:** Active (v2.3+)
**Last Updated:** 2025-10-02

---

## Overview

The Pattern Versioning System provides semantic versioning for all patterns in the AGET ecosystem. This prevents breaking changes from disrupting multi-agent collaboration and enables safe pattern evolution.

## Why Pattern Versioning?

**Problem:** Before v2.3, patterns had no version tracking. When patterns changed:
- AGETs broke silently when incompatible patterns were deployed
- No way to track breaking changes
- Multi-agent collaboration impossible (AGETs might use incompatible patterns)
- Pattern dependencies not validated

**Solution:** Semantic versioning with:
- Central version registry
- Automated version bumping
- Dependency checking
- Migration templates
- Breaking change tracking

## Components

### 1. Version Registry (`.aget/patterns/versions.yaml`)

Central registry tracking all pattern versions across ecosystem.

**Schema:**
```yaml
metadata:
  registry_version: "1.0.0"
  last_updated: "2025-10-02"
  total_patterns: 24

patterns:
  pattern_name:
    version: "1.0.0"
    category: "routing"
    file: "routing/pattern.py"
    description: "What it does"
    added: "2025-09-27"
    last_modified: "2025-09-27"
    breaking_changes: []

dependencies:
  pattern_name:
    requires:
      - dependency: "^1.0.0"
```

### 2. Version Bump Tool (`.aget/tools/bump_pattern.py`)

CLI tool for incrementing pattern versions.

**Usage:**
```bash
# List all patterns
python3 .aget/tools/bump_pattern.py --list

# Show pattern info
python3 .aget/tools/bump_pattern.py github/create_issue --show

# Bump versions
python3 .aget/tools/bump_pattern.py github/create_issue --patch
python3 .aget/tools/bump_pattern.py github/create_issue --minor
python3 .aget/tools/bump_pattern.py github/create_issue --major \
  --breaking-change "Changed API signature"
```

### 3. Compatibility Checker (`.aget/tools/check_pattern_compatibility.py`)

Validates pattern dependencies and detects conflicts.

**Usage:**
```bash
# Check all patterns
python3 .aget/tools/check_pattern_compatibility.py

# Strict mode (warnings = errors)
python3 .aget/tools/check_pattern_compatibility.py --strict
```

### 4. Migration Template (`.aget/patterns/MIGRATION_TEMPLATE.md`)

Scaffolding for pattern migration guides.

## Semantic Versioning Rules

Pattern versions follow semantic versioning: `MAJOR.MINOR.PATCH`

### MAJOR Version (Breaking Changes)

Increment when making incompatible changes:
- Changing function signatures
- Removing features
- Changing behavior that breaks existing usage
- Renaming files or modules

**Example:** `1.2.3` → `2.0.0`

**Requires:**
- `--breaking-change` description
- Migration guide
- Coordination with all AGETs using the pattern

### MINOR Version (New Features)

Increment when adding backward-compatible features:
- New optional parameters
- New capabilities
- Performance improvements
- Enhanced functionality (old functionality still works)

**Example:** `1.2.3` → `1.3.0`

**Requires:**
- Documentation update
- No migration needed

### PATCH Version (Bug Fixes)

Increment when making backward-compatible fixes:
- Bug fixes
- Documentation fixes
- Internal refactoring (no API change)
- Security patches

**Example:** `1.2.3` → `1.2.4`

**Requires:**
- Minimal documentation
- No migration needed

## Version Dependency Format

Dependencies use caret (`^`) notation:

```yaml
dependencies:
  routing/route_engine:
    requires:
      - routing/agent_registry: "^1.0.0"
```

**Caret Range (`^1.2.3`):**
- Allows: `>=1.2.3` and `<2.0.0`
- Rationale: MINOR and PATCH are backward compatible, MAJOR is not
- Example: `^1.2.3` matches `1.2.3`, `1.2.4`, `1.5.0` but NOT `2.0.0`

## Workflows

### Workflow 1: Bug Fix (PATCH)

```bash
# 1. Fix the bug in pattern code
vim .aget/patterns/github/create_issue.py

# 2. Bump patch version
python3 .aget/tools/bump_pattern.py github/create_issue --patch
# Output: ✅ Bumped github/create_issue: v1.0.0 → v1.0.1

# 3. Check compatibility
python3 .aget/tools/check_pattern_compatibility.py
# Output: ✅ PASS: All compatibility checks passed

# 4. Commit
git add .aget/patterns/github/create_issue.py .aget/patterns/versions.yaml
git commit -m "fix(github/create_issue): Fix edge case in issue creation (v1.0.1)"

# 5. Deploy (automatic - no migration needed)
```

### Workflow 2: New Feature (MINOR)

```bash
# 1. Add new feature to pattern code
vim .aget/patterns/github/create_issue.py

# 2. Bump minor version
python3 .aget/tools/bump_pattern.py github/create_issue --minor
# Output: ✅ Bumped github/create_issue: v1.0.1 → v1.1.0

# 3. Check compatibility
python3 .aget/tools/check_pattern_compatibility.py

# 4. Update documentation
vim docs/patterns/github_create_issue.md

# 5. Commit
git add .aget/patterns/github/create_issue.py .aget/patterns/versions.yaml docs/
git commit -m "feat(github/create_issue): Add --priority flag (v1.1.0)"

# 6. Deploy (automatic - backward compatible)
```

### Workflow 3: Breaking Change (MAJOR)

```bash
# 1. Make breaking change to pattern code
vim .aget/patterns/github/create_issue.py

# 2. Create migration guide
cp .aget/patterns/MIGRATION_TEMPLATE.md \
   .aget/patterns/migrations/github_create_issue_v1_to_v2.md
vim .aget/patterns/migrations/github_create_issue_v1_to_v2.md

# 3. Bump major version with breaking change description
python3 .aget/tools/bump_pattern.py github/create_issue --major \
  --breaking-change "Changed --body parameter to --description"
# Output: ✅ Bumped github/create_issue: v1.1.0 → v2.0.0
#         Breaking change: Changed --body parameter to --description

# 4. Check compatibility (will show breaking change warning)
python3 .aget/tools/check_pattern_compatibility.py

# 5. Commit
git add .aget/patterns/github/create_issue.py \
        .aget/patterns/versions.yaml \
        .aget/patterns/migrations/
git commit -m "feat(github/create_issue)!: Change --body to --description (v2.0.0)

BREAKING CHANGE: --body parameter renamed to --description
See migration guide: .aget/patterns/migrations/github_create_issue_v1_to_v2.md"

# 6. Coordinate deployment (requires migration)
# - Notify all AGETs using this pattern
# - Schedule migration window
# - Follow migration guide
```

## Pattern Lifecycle

```
[New Pattern]
     ↓
v1.0.0 (Initial Release)
     ↓
v1.0.1 (Bug fixes - PATCH)
     ↓
v1.1.0 (New features - MINOR)
     ↓
v1.2.0 (More features - MINOR)
     ↓
v2.0.0 (Breaking change - MAJOR)
     ↓
v2.1.0 (New features - MINOR)
     ↓
[Deprecated] → [Removed in v3.0.0]
```

## Multi-AGET Compatibility

**Scenario:** Coordinator uses `routing/route_engine` v1.5.0, which requires `routing/agent_registry` ^1.0.0

**Compatible:**
- agent_registry v1.0.0 ✅
- agent_registry v1.2.0 ✅ (backward compatible minor bump)
- agent_registry v1.9.9 ✅ (backward compatible)

**Incompatible:**
- agent_registry v0.9.0 ❌ (too old)
- agent_registry v2.0.0 ❌ (breaking change)

**Resolution:**
```bash
# Check what's wrong
python3 .aget/tools/check_pattern_compatibility.py
# Output: ❌ FAIL: routing/route_engine requires routing/agent_registry ^1.0.0 but found v2.0.0

# Option 1: Upgrade route_engine to v2.0.0 (if available)
python3 .aget/tools/bump_pattern.py routing/route_engine --show
# Check if v2.0.0+ exists that supports agent_registry v2.0.0

# Option 2: Rollback agent_registry to v1.x
git checkout HEAD~1 .aget/patterns/versions.yaml
```

## Integration with v2.3 Collaboration

Pattern versioning enables safe multi-agent collaboration:

1. **Discovery Phase:** AGETs query registry for available patterns and versions
2. **Handoff Phase:** Collaboration context includes pattern versions used
3. **Validation Phase:** Compatibility checker ensures no version conflicts
4. **Execution Phase:** AGETs use compatible pattern versions

**Example:**
```yaml
# Collaboration context
task_id: "review-pr-123"
initiator: "coordinator"
target: "github-aget"
patterns_used:
  - github/create_issue: "1.1.0"
  - github/list_issues: "1.0.0"
compatibility_check: "passed"
```

## Best Practices

### DO:
- ✅ Bump patch version for every bug fix
- ✅ Bump minor version for new features
- ✅ Bump major version for breaking changes
- ✅ Document breaking changes in migration guide
- ✅ Run compatibility checker before committing
- ✅ Coordinate major version deployments across AGETs

### DON'T:
- ❌ Skip version bumps (even for small changes)
- ❌ Make breaking changes in minor/patch versions
- ❌ Deploy major versions without migration guide
- ❌ Ignore compatibility checker failures
- ❌ Deploy to production without testing on dev branch

## Troubleshooting

### Issue: Pattern not in registry

**Error:** `ERROR: Pattern not found: github/create_issue`

**Solution:**
```bash
# List available patterns
python3 .aget/tools/bump_pattern.py --list

# Check exact pattern name (case-sensitive, category/name format)
# Correct: github/create_issue
# Wrong: github_create_issue, CreateIssue, create_issue
```

### Issue: Dependency conflict

**Error:** `routing/route_engine requires routing/agent_registry ^1.0.0 but found v2.0.0`

**Solution:**
```bash
# Option 1: Upgrade dependent pattern
# Check if route_engine has v2.x that supports agent_registry v2.0.0
python3 .aget/tools/bump_pattern.py routing/route_engine --show

# Option 2: Rollback dependency
git log .aget/patterns/versions.yaml  # Find commit before v2.0.0
git checkout <commit> .aget/patterns/versions.yaml
```

### Issue: Breaking change deployed accidentally

**Error:** AGETs break after pattern update

**Solution:**
```bash
# 1. Immediate rollback
git revert <commit>
git push origin v2.3-dev

# 2. Create hotfix
python3 .aget/tools/bump_pattern.py <pattern> --patch

# 3. Proper major version process
python3 .aget/tools/bump_pattern.py <pattern> --major \
  --breaking-change "Description of what broke"

# 4. Create migration guide
cp .aget/patterns/MIGRATION_TEMPLATE.md \
   .aget/patterns/migrations/<pattern>_v<old>_to_v<new>.md
```

## Future Enhancements (v2.4+)

- Automated migration script generation
- Pattern version compatibility matrix UI
- Cross-AGET version synchronization
- Deprecation warnings in pattern output
- Automated rollback on compatibility failure

## References

- Semantic Versioning Spec: https://semver.org/
- Pattern Registry: `.aget/patterns/versions.yaml`
- Bump Tool: `.aget/tools/bump_pattern.py`
- Compatibility Checker: `.aget/tools/check_pattern_compatibility.py`
- Migration Template: `.aget/patterns/MIGRATION_TEMPLATE.md`
- Controlled Vocabulary: `.aget/evolution/CONTROLLED_VOCABULARY.md` (v1.1.0)

---

*Pattern Versioning System - Enabling safe pattern evolution since v2.3*
