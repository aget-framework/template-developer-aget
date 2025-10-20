# File Ownership Model (AGET)

## Overview
The AGET (Agent Template) architecture uses a clear file ownership model to separate template-managed files from user customizations.

## Core AGET Files (Template-Owned)
These files are managed by the CLI Agent Template and should not be modified directly by users:

### Protocol Scripts
- `scripts/aget_session_protocol.py` - Session management (wake/wind-down/sign-off)
- `scripts/aget_housekeeping_protocol.py` - Cleanup and maintenance protocols
- `scripts/install_verify.py` - Installation verification
- `scripts/security_check.py` - Security scanning

### Templates
- `templates/minimal/` - Minimal template files
- `templates/standard/` - Standard template files
- `templates/advanced/` - Advanced template files

### Core Documentation
- `docs/FILE_OWNERSHIP.md` - This file
- `docs/WRITE_PATTERNS.md` - Pattern documentation
- `docs/GET_STARTED.md` - Getting started guide

## User Files (Project-Owned)
These files belong to the user's project and can be freely customized:

### Configuration
- `AGENTS.md` - User sections between template markers
- `CLAUDE.md` - If not a symlink, user-owned
- Custom scripts in `scripts/` (without aget_ prefix)

### Project Files
- `README.md` - Project documentation
- `.env` - Environment variables
- Custom configuration files
- All application code

## Update Strategy
When updating AGET templates:

1. **Template-owned files**: Can be safely overwritten
2. **User-owned files**: Must preserve user modifications
3. **Hybrid files** (like AGENTS.md): Use section markers to protect user content

## Section Markers
AGET uses section markers to manage updates in hybrid files:

```markdown
<!-- BEGIN AGET:section-name v1.0 -->
Template-managed content here
<!-- END AGET:section-name -->

User content here (preserved during updates)
```

## Migration Path
When migrating from old naming to AGET:

1. Old script names become symlinks to aget_ versions
2. User references are gradually updated
3. Full deprecation after transition period