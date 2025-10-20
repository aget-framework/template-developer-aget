# Migration Guide: AGET v1 to v2

This guide helps you migrate from AGET v1 (script-based) to v2 (pattern-based).

## What's New in v2

### Major Changes
- **Pattern-based architecture** - Reusable patterns instead of monolithic scripts
- **Include architecture** - Separate AGENTS.md from project files
- **Enhanced CLI** - `aget init`, `aget apply`, `aget extract` commands
- **Evolution tracking** - Built-in decision and discovery tracking

### Breaking Changes
- Scripts moved from root to `scripts/` directory
- CLAUDE.md renamed to AGENTS.md (symlink provided for compatibility)
- Pattern structure requires `apply_pattern()` function

## Migration Paths

### Option 1: Fresh Install (Recommended)
Best for projects that can start clean.

```bash
# Backup existing configuration
cp CLAUDE.md CLAUDE.md.backup

# Install v2
python3 -m aget init --template agent --with-patterns

# Your old CLAUDE.md is preserved as symlink
```

### Option 2: In-Place Migration
For projects that need gradual transition.

```bash
# Run migration tool
python3 -m aget migrate .

# This will:
# - Convert CLAUDE.md to AGENTS.md
# - Move scripts to scripts/ directory
# - Add v2 patterns while keeping v1 scripts
```

### Option 3: Manual Migration
For customized setups.

1. Create AGENTS.md from CLAUDE.md
2. Move scripts to scripts/ directory
3. Add .aget/version.json
4. Apply patterns selectively

## Compatibility Features

### Backward Compatibility
- **CLAUDE.md symlink** - Old references continue working
- **v1 scripts** - Still functional alongside v2 patterns
- **Gradual adoption** - Use v2 patterns as needed

### Tool Compatibility
All AI tools continue working:
- Claude Code ✅
- Cursor ✅
- Aider ✅
- Windsurf ✅

## Step-by-Step Migration

### 1. Assess Current State
```bash
python3 scripts/validate_patterns.py
```

### 2. Backup Current Setup
```bash
cp -r . ../backup-$(date +%Y%m%d)
```

### 3. Install AGET v2
```bash
git clone https://github.com/gmelli/aget-cli-agent-template.git
cd aget-cli-agent-template
python3 -m aget init /path/to/project --template agent
```

### 4. Verify Migration
```bash
# Test core patterns
python3 scripts/aget_session_protocol.py wake
python3 scripts/aget_session_protocol.py wind-down
```

### 5. Clean Up (Optional)
```bash
# Remove v1 artifacts
python3 -m aget apply housekeeping/migration_cleanup
```

## Common Issues

### Issue: Scripts not found
**Solution**: Check scripts are in scripts/ directory, not root

### Issue: Patterns not loading
**Solution**: Ensure patterns have `apply_pattern()` function

### Issue: CLAUDE.md not recognized
**Solution**: AGENTS.md should exist with CLAUDE.md as symlink

## Feature Comparison

| Feature | v1 | v2 |
|---------|----|----|
| Setup time | 5-10 minutes | <60 seconds |
| Pattern reuse | Copy-paste | `aget apply` |
| Evolution tracking | Manual | Automatic |
| Multi-project | Difficult | `aget init` |
| Extraction | Manual | `aget extract` |

## Getting Help

- **Issues**: https://github.com/gmelli/aget-cli-agent-template/issues
- **Docs**: See docs/ directory
- **Validation**: Run `python3 scripts/validate_patterns.py`

## Timeline

- **v1 Support**: Continues through 2025
- **v2 Stable**: October 7, 2025
- **Migration Period**: 3 months recommended

---

*AGET v2: Making CLI agents better collaborators*