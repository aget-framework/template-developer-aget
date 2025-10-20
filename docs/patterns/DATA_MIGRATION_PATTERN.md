# Data Migration Pattern

**Pattern Type**: Organizational
**Source**: Proven in production
**Risk Level**: Low (incremental, reversible)

## Pattern: Centralize Agent Data in ./data Directory

### Problem
Agent cognitive data (musings, sessions, state) scattered across project root creates:
- Cluttered repository structure
- Difficult .gitignore management
- Hard to separate public code from private data
- Complex backup strategies

### Solution
Migrate all agent data to a centralized `./data` directory with clear subdirectories.

## Implementation Steps

### 1. Create Structure
```bash
mkdir -p data/{captures,sessions,state}
mkdir -p data/captures/journal_v2
```

### 2. Migration Script Pattern
```python
#!/usr/bin/env python3
"""Migrate with backward compatibility"""

def migrate_incremental():
    # 1. Copy to new location
    # 2. Update scripts to check both locations
    # 3. Verify everything works
    # 4. Delete old locations only after confirmation
```

### 3. Backward Compatibility Pattern
```python
# In scripts, check both locations
def get_data_path(filename):
    new_path = Path(f"data/state/{filename}")
    old_path = Path(filename)

    # Prefer new location, fall back to old
    if new_path.exists():
        return new_path
    elif old_path.exists():
        return old_path
    else:
        # Create in new location
        return new_path
```

### 4. Verification Pattern
```python
def verify_migration():
    checks = []

    # Check structure exists
    checks.append(Path("data/captures").exists())
    checks.append(Path("data/sessions").exists())
    checks.append(Path("data/state").exists())

    # Check data accessible
    checks.append(can_read_json("data/state/moments.json"))

    # Check scripts work
    checks.append(test_capture_command())

    return all(checks)
```

### 5. Health Check Pattern
Create comprehensive health check:
```python
def health_check():
    results = {
        "data_structure": check_directories(),
        "json_validity": validate_json_files(),
        "script_function": test_scripts(),
        "git_status": check_git_clean(),
        "old_locations": verify_cleaned_up()
    }
    return results
```

## Final Structure

```
project/
├── .aget/                 # AGET metadata (unchanged)
├── AGENTS.md              # AGET config (unchanged)
├── data/                  # Centralized agent data
│   ├── captures/
│   │   └── journal_v2/   # Timestamped captures
│   ├── sessions/
│   │   ├── .session_state.json
│   │   └── SESSION_*.md
│   └── state/
│       └── moments.json  # Agent state
├── scripts/              # Agent scripts
└── src/                  # Project code
```

## Checkpoint Strategy

Based on production experience:

1. **Before Migration**: Commit current state
2. **After Structure Creation**: Checkpoint "structure ready"
3. **After Script Updates**: Checkpoint "scripts migrated"
4. **After Verification**: Checkpoint "migration verified"
5. **After Cleanup**: Final commit "migration complete"

## Benefits Observed

- ✅ Clean repository root
- ✅ Easy to .gitignore entire data/ if needed
- ✅ Simple to separate into project-data/ later
- ✅ Clear boundary between code and cognitive data
- ✅ Improved backup/restore operations

## Compatibility

- **AGET v2**: Fully compatible (AGET only requires .aget/ and AGENTS.md)
- **Rollback**: Git revert to any checkpoint
- **Future**: Ready for multi-repo pattern if needed

## Migration Command (Future AGET)

```bash
# Potential future AGET command
aget migrate --to-data-dir
```

## Key Insight

> "Checkpoints should be part of sprint planning - saves from missing the moment"

This led to explicit checkpoint planning in sprint templates, ensuring incremental progress is captured and reversible.

---

*Pattern extracted from production usage*