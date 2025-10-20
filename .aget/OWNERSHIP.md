# AGET File Ownership Guide

## Quick Rule
- **Files starting with `aget_`** = Framework files (DO NOT MODIFY)
- **Everything else** = Your agent's files (safe to modify)

## Directory Ownership

### Framework-Owned (Don't Modify)
- `.aget/` - All AGET framework files
- `scripts/aget_*.py` - Framework scripts
- `scripts/aget_*.sh` - Framework scripts
- `aget/` module (if present) - The AGET Python package

### Agent-Owned (Your Files)
- `src/` - Your agent's source code
- `workspace/` - Your working directory
- `products/` - Products you create
- `data/` - Your data storage
- `scripts/*.py` (without aget_ prefix) - Your custom scripts
- `patterns/` - Your custom patterns
- `tests/` - Your test suite

## Examples

### Framework Files (Don't Edit These)
```
scripts/aget_session_protocol.py
scripts/aget_housekeeping_protocol.py
scripts/aget_pre_release.sh
scripts/aget_check_permissions.py
.aget/patterns/
```

### Your Files (Safe to Edit)
```
scripts/my_release_tool.py
src/agent_logic.py
workspace/experiments/
products/release_notes.md
patterns/my_custom_pattern.py
```

## Why This Matters
This separation ensures:
1. AGET updates won't overwrite your work
2. You know which files are safe to modify
3. Clear boundaries between framework and agent code

## For Developers
When creating new scripts:
- Framework maintainers: Always use `aget_` prefix for framework scripts
- Agent developers: Never use `aget_` prefix for your scripts

---
*AGET v2.1.0 - Clear Ownership Standard*