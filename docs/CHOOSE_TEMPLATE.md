# Scaffolding System Documentation

## Overview

The AGET scaffolding system provides template-based project initialization with predefined directory structures optimized for different use cases. This feature was added in Gate 3 to address learnings from the llm-manager-aget project.

## Template Options

### Minimal Template
**Use Case**: Basic agent configuration with minimal overhead
**Command**: `aget init --template minimal`

Creates:
- `.aget/` - Framework metadata
- `.aget/evolution/` - Decision tracking
- `AGENTS.md` - Agent configuration
- `CLAUDE.md` - Backward compatibility symlink

### Standard Template (Default)
**Use Case**: General-purpose development with private workspace
**Command**: `aget init` or `aget init --template standard`

Creates everything from Minimal plus:
- `workspace/` - Private development area
- `data/` - Persistent data storage

### Agent Template
**Use Case**: Autonomous agent development
**Command**: `aget init --template agent`

Creates:
- `.aget/` with `checkpoints/` for state management
- `src/` - Agent source code
- `workspace/` - Private exploration area
- `products/` - Public products
- `data/` - Persistent storage
- `docs/` - Documentation
- `tests/` - Test suite

### Tool Template
**Use Case**: Public tool/library development
**Command**: `aget init --template tool`

Creates:
- `.aget/` for framework metadata
- `src/` - Tool source code
- `products/` - Public distribution
- `docs/` - Documentation
- `tests/` - Test suite

Note: No `workspace/` since tools focus on public products

### Hybrid Template
**Use Case**: Combined agent and tool development
**Command**: `aget init --template hybrid`

Creates everything from Agent template plus:
- `examples/` - Usage examples and demos

## Directory Structure

### Core Directories

#### `.aget/`
Framework metadata and state management
- `version.json` - Template and version information
- `evolution/` - Decision and discovery tracking
- `checkpoints/` - Agent state snapshots (agent/hybrid templates)

#### `workspace/`
Private exploration and development area
- Internal tools and scripts
- Work-in-progress code
- Experimental features
- Not intended for public use

#### `products/`
Public products ready for distribution
- Standalone tools
- Extracted utilities
- Published packages
- Documentation

#### `src/`
Main source code
- Agent implementation
- Tool functionality
- Core logic

## Vocabulary Evolution

The scaffolding system uses renamed directories to avoid case-sensitivity issues:

| Original | New | Purpose |
|----------|-----|---------|
| `outputs/` | `workspace/` | Private exploration |
| `Outputs/` | `products/` | Public products |

This change ensures compatibility across all filesystems (macOS, Windows, Linux).

## Usage Examples

### Creating a New Agent Project

```bash
# Initialize with agent template
aget init --template agent my-agent

# Navigate to project
cd my-agent

# View created structure
ls -la
```

### Creating a Tool Library

```bash
# Initialize with tool template
aget init --template tool my-tool

# No workspace directory - focus on public products
ls products/
```

### Upgrading from Default to Agent

```bash
# Start with standard template
aget init my-project

# Later, manually add missing directories
mkdir src tests docs products
```

## Template-Specific Features

### Gitignore Patterns

Each template adds appropriate `.gitignore` patterns:

**All templates**:
- `.aget/backups/`
- `.aget/cache/`
- `.session_state.json`
- Python artifacts (`__pycache__/`, `*.pyc`)

**Agent/Hybrid templates** also add:
- `workspace/.tmp/`
- `workspace/*.log`

### README Files

The scaffolding system automatically creates README.md files in key directories:

- **workspace/README.md** - Explains private nature
- **products/README.md** - Describes public purpose
- **src/README.md** - Source code organization
- **.aget/evolution/README.md** - Evolution tracking guide
- **tests/README.md** - Testing instructions
- **docs/README.md** - Documentation structure

### Version Tracking

The `.aget/version.json` file tracks:
```json
{
  "aget_version": "2.0.0-alpha",
  "created": "2025-09-24",
  "template": "agent",
  "tier": "basic"
}
```

## Implementation Details

### Tier System

The scaffolding works with the three-tier degradation pattern:

1. **Basic Tier**: Creates directories and AGENTS.md
2. **Git Tier**: Adds .gitignore configuration
3. **GitHub Tier**: Adds issue templates

### Cross-Platform Compatibility

- Uses `Path` objects for filesystem operations
- Handles both Unix and Windows paths
- Creates symlinks where supported, fallback to redirect files
- Case-insensitive filesystem safe (workspace/products naming)

## Testing

The scaffolding system includes comprehensive tests:

```bash
# Run scaffolding tests
python3 -m pytest tests/test_scaffolding.py -v
```

Tests verify:
- All templates create expected directories
- README files are properly placed
- AGENTS.md contains correct template information
- Version tracking includes template type
- Invalid templates are rejected
- Default template is 'standard'

## Future Enhancements

Planned improvements for the scaffolding system:

1. **Custom Templates**: User-defined template configurations
2. **Template Inheritance**: Extend existing templates
3. **Post-Init Hooks**: Run commands after scaffolding
4. **Remote Templates**: Pull templates from GitHub
5. **Interactive Mode**: Wizard for template selection

## Migration from v1

For projects using v1 patterns:

1. The old `outputs/` directory maps to `workspace/`
2. The old `Outputs/` directory maps to `products/`
3. Use `aget migrate` (coming soon) for automated migration

## Troubleshooting

### "AGENTS.md already exists"

Use `--force` to overwrite:
```bash
aget init --template agent --force
```

### Missing Directories

Verify template created all directories:
```bash
ls -la
```

If missing, create manually or re-run with different template.

### Case Sensitivity Issues

The rename from outputs/Outputs to workspace/products specifically addresses this issue on macOS and Windows.

## See Also

- [QUICK_START.md](QUICK_START.md) - Getting started guide
- [PATTERNS_EXPLAINED.md](PATTERNS_EXPLAINED.md) - Understanding patterns
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migrating from v1