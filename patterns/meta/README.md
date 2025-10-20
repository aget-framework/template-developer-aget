# Meta Patterns

Patterns for managing repositories that contain multiple AGET-enabled projects.

## Available Patterns

### project_scanner.py
Scans all sub-projects to determine AGET migration status.

**Usage**:
```bash
python patterns/meta/project_scanner.py
python patterns/meta/project_scanner.py --json
python patterns/meta/project_scanner.py --quiet
```

**Exit Codes**:
- 0: All projects migrated
- 1: Partial migration
- 2: No projects migrated
- 3: Error

### bulk_operations.py (Planned)
Apply operations across multiple sub-projects.

**Planned Features**:
- Update all AGENTS.md files
- Run tests across all projects
- Generate consolidated reports
- Synchronize pattern versions

### pattern_federation.py (Planned)
Share patterns across multiple projects.

**Planned Features**:
- Extract common patterns
- Create shared pattern library
- Manage pattern dependencies
- Version synchronization

## Meta-Repository Structure

A typical meta-repository with AGET should have:

```
meta-repo/
├── .aget/
│   ├── version.json        # Meta-repo AGET version
│   └── projects.json       # Registry of sub-projects
├── AGENTS.md               # Meta-level agent config
├── patterns/
│   ├── meta/              # Meta-repository patterns
│   └── shared/            # Patterns shared by sub-projects
└── projects/
    ├── project-1/         # AGET-enabled project
    ├── project-2/         # AGET-enabled project
    └── legacy-project/    # Not yet migrated
```

## Implementation Status

| Pattern | Status | Priority |
|---------|--------|----------|
| project_scanner.py | ✅ Implemented | High |
| bulk_operations.py | 📋 Planned | Medium |
| pattern_federation.py | 📋 Planned | Low |
| version_matrix.py | 📋 Planned | Low |

---
*Part of EP-4: Meta Patterns proposal*