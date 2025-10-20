# AGET Distributed Architecture

## Overview

AGET follows a **distributed laboratory model** where the public framework enables multiple private implementations. This architecture separates universal framework code from experimental and proprietary patterns.

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│            PUBLIC LAYER (Open Source)            │
│                                                  │
│         aget-cli-agent-template (MIT)           │
│      Framework, Protocol, Universal Patterns    │
└──────────────────┬──────────────────────────────┘
                   │ Fork & Customize
     ┌─────────────┼─────────────┬─────────────┐
     ▼             ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Lab A   │  │ Lab B   │  │ Lab C   │  │Reference│
│CorpAGET│  │TeamAGET │  │MyAGET   │  │aget-aget│
│(private)│  │(private)│  │(private)│  │(private)│
└─────────┘  └─────────┘  └─────────┘  └─────────┘
     ▲             ▲             ▲             ▲
     └─────────────┴─────────────┴─────────────┘
              Optional Contribution Back
```

## Component Responsibilities

### Public Framework (aget-cli-agent-template)
**Purpose**: Universal framework and protocol definition

**Contains**:
- Core AGET implementation (`aget/` module)
- Universal patterns (`patterns/`)
- Standard templates (`templates/`)
- Framework tests (`tests/`)
- Public documentation

**Does NOT Contain**:
- Experimental code
- Company-specific patterns
- Opinionated workflows
- Private documentation

### Private Laboratories (Multiple Instances)
**Purpose**: Experimentation and customization

**Examples**:
- `aget-aget` - Reference lab (Gabor Melli's)
- `corp-aget` - Enterprise patterns
- `team-aget` - Team-specific workflows
- `my-aget` - Personal experiments

**Contains**:
- Experimental patterns
- Custom workflows
- Private documentation
- Failed experiments (learning)
- Proprietary enhancements

## Data Flow Patterns

### 1. Universal Pattern Discovery
```
Private Lab                Public Framework
Experiment → Validate → PR → Review → Merge → Available to All
```

### 2. Framework Bug Fix
```
Private Lab                     Public Framework
Discover Bug → Fix & Test → PR → Fast Track Merge
```

### 3. Private Pattern Development
```
Private Lab Only
Develop → Test → Use Internally → Keep Private
```

## Core Components

### 1. Configuration Layer

#### AGENT.md
- Universal agent configuration file
- Contains all natural language triggers
- Works with any CLI coding agent (Claude Code, Cursor, Aider, etc.)
- CLAUDE.md exists as symlink for backward compatibility

#### Makefile
- Provides command shortcuts (`make wake`, `make wind-down`)
- Template-specific targets
- Fallback for agents that don't read AGENT.md

### 2. Protocol Layer

#### Session Protocol (`scripts/aget_session_protocol.py`)
**Purpose**: Manage development sessions with state persistence

**Key Features**:
- **SessionState Class**: Persistent JSON state management
- **Wake Command**: Initialize session, show project status
- **Wind Down**: Commit changes, save session notes, run tests
- **Sign Off**: Quick commit and push
- **Status Command**: Show current session info

**State Management**:
```python
{
    "last_wake": "ISO timestamp",
    "last_wind_down": "ISO timestamp",
    "session_count": 42,
    "total_commits": 156,
    "current_session": {
        "start_time": "ISO timestamp",
        "tasks_completed": [],
        "files_modified": [],
        "tests_run": 3
    }
}
```

#### Housekeeping Protocol (`scripts/aget_housekeeping_protocol.py`)
**Purpose**: Maintain codebase cleanliness

**Commands**:
- `documentation-check`: Analyze docs quality (A-F grade)
- `housekeeping`: Light cleanup (caches, temp files)
- `spring-clean`: Deep cleanup with archiving
- `sanity-check`: Emergency diagnostics

### 3. Template System

#### Installer (`installer/install.py`)
**Purpose**: Install patterns into target projects

**Template Levels**:
1. **Minimal**: Basic session management only
2. **Standard**: Adds housekeeping protocols
3. **Advanced**: Adds CI/CD, testing patterns

**Key Methods**:
- `install()`: Main installation process
- `customize_file()`: Replace template variables
- `create_symlink()`: CLAUDE.md backward compatibility
- `merge_files()`: Smart Makefile merging

### 4. Pattern Organization

```
patterns/
├── session/          # Session management patterns
├── housekeeping/     # Cleanup and maintenance
├── documentation/    # Doc generation and checking
├── recovery/         # Error recovery patterns
├── state/           # State persistence (Phase 2)
├── rules/           # Safety boundaries (Phase 3)
├── hooks/           # Event hooks (Phase 3)
└── identity/        # Agent personality (Phase 3)
```

### 5. Session Notes Organization

```
SESSION_NOTES/
├── YYYY-MM-DD/      # Daily directories
│   ├── session_HHMM.md
│   └── session_HHMM.md
├── archive/         # Sessions >30 days old
│   └── YYYY-MM-DD/
└── .session_state.json
```

## Design Principles

### 1. Progressive Disclosure
- Start simple (minimal template)
- Add complexity only when needed
- Each pattern is self-contained

### 2. Dogfooding
- Repository uses its own patterns
- Tests use the actual protocols
- Documentation generated by patterns

### 3. Universal Compatibility
- AGENT.md works with any CLI agent
- Python 3.8+ (widely available)
- No exotic dependencies

### 4. Safety First
- Dry-run by default for destructive operations
- State persistence prevents data loss
- Git integration for rollback capability

## Data Flow

### Wake Up Flow
```
User: "wake up"
  ↓
Agent reads AGENT.md
  ↓
Executes: python3 scripts/aget_session_protocol.py wake
  ↓
SessionState.start_session()
  ↓
Show: Directory, Git status, Patterns, Tests
  ↓
organize_session_notes()
  ↓
"Ready for tasks"
```

### Wind Down Flow
```
User: "wind down"
  ↓
Check uncommitted changes
  ↓
Git commit if needed
  ↓
Run tests
  ↓
Create session note in SESSION_NOTES/YYYY-MM-DD/
  ↓
SessionState.end_session()
  ↓
Archive old sessions
  ↓
"Session preserved"
```

## Extension Points

### Adding New Patterns
1. Create pattern in `patterns/<category>/<name>.py`
2. Add tests in `tests/test_<name>.py`
3. Update installer to include pattern
4. Document in pattern's README.md

### Custom Triggers
Edit AGENT.md to add project-specific commands:
```markdown
### Deploy to Production
When user says "deploy", execute:
- Run: `./scripts/deploy.sh`
```

### State Extensions
Extend SessionState class to track custom metrics:
```python
state['custom_metrics'] = {
    'deploys': 0,
    'reviews': 0,
    'refactors': 0
}
```

## Security Considerations

### Sensitive Data
- Never commit .session_state.json (gitignored)
- Session notes sanitize file paths
- No credentials in templates

### Command Injection
- All subprocess calls use arrays when possible
- User input never directly inserted into commands
- Git messages properly quoted

## Performance

### Optimizations
- Lazy imports where possible
- Session state cached in memory
- Pattern detection uses glob efficiently
- Archive runs only when needed

### Scalability
- Handles 1000s of session notes
- Patterns load on-demand
- Templates cached after first read

## Testing Strategy

### Unit Tests
- Each protocol function tested
- State persistence verified
- Template installation mocked

### Integration Tests
- Full wake/wind-down cycle
- Git operations verified
- File organization tested

### Coverage Goals
- Core protocols: >80%
- Installer: >80%
- Patterns: >70%

## Future Architecture (Phases 2-5)

### Phase 2: State Management
- Dedicated state/ pattern
- Context preservation across sessions
- Task tracking integration

### Phase 3: Advanced Patterns
- Rules engine for safety boundaries
- Hook system for custom events
- Identity patterns for agent personality

### Phase 4: Template Variants
- Project type detection
- Framework-specific templates
- Enterprise multi-repo support

### Phase 5: Production Features
- Telemetry and analytics
- Performance monitoring
- Update notifications

## Dependencies

### Required
- Python 3.8+
- Git

### Optional
- PyYAML (for config files)
- pytest (for running tests)
- Make (for Makefile commands)

## File Structure

```
cli-agent-template/
├── AGENT.md              # Universal config
├── CLAUDE.md            # Symlink to AGENT.md
├── ARCHITECTURE.md      # This file
├── README.md            # User documentation
├── Makefile             # Command shortcuts
├── installer/           # Installation system
│   ├── install.py
│   └── status.py
├── patterns/            # Reusable patterns
│   └── */
├── scripts/             # Protocol implementations
│   ├── session_protocol.py
│   └── housekeeping_protocol.py
├── templates/           # Template variants
│   ├── minimal/
│   ├── standard/
│   └── advanced/
├── tests/               # Test suite
│   └── test_*.py
└── SESSION_NOTES/       # Session storage
    └── YYYY-MM-DD/
```

## Conventions

### Naming
- Patterns: lowercase with underscores
- Templates: lowercase single word
- Commands: hyphenated (wind-down, sign-off)
- Session notes: session_YYYYMMDD_HHMM.md

### Versioning
- Semantic versioning (MAJOR.MINOR.PATCH)
- Each pattern has independent version
- Templates versioned with main package

### Git Commits
- Type prefixes: feat, fix, docs, test, chore
- Session commits: "session: Wind down at TIMESTAMP"
- Sign-off commits: "chore: Quick sign off at TIMESTAMP"

---

This architecture enables any codebase to become agent-ready while maintaining simplicity, safety, and extensibility.