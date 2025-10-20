# AGET Branching Strategy (GitFlow-Lite)

## Branch Structure

### Primary Branches
- **main** - Stable, production-ready code (current: v2.1.0)
- **develop** - Integration branch for next release (current: v2.2.0-dev)

### Supporting Branches
- **release/vX.Y.Z** - Release candidates before merging to main
- **feature/name** - Individual feature development
- **hotfix/issue** - Critical fixes to main

## Current State (as of 2025-09-28)

```
main (v2.1.0) ← Users clone this by default
  ↑
develop (v2.2.0-dev) ← Active development
```

## Version Tags

- `v2.1.0` - Current stable release on main
- `v2.0.0` - Previous stable release
- `v2.2.0-dev` - Next version in development

## For Users

### Getting Stable Version (Default)
```bash
git clone https://github.com/aget-framework/aget-worker-template.git
# You get main branch (stable)
```

### Getting Development Version
```bash
git clone -b develop https://github.com/aget-framework/aget-worker-template.git
# You get latest development features
```

### Getting Specific Version
```bash
git clone https://github.com/aget-framework/aget-worker-template.git
cd aget-worker-template
git checkout v2.0.0-stable  # or any tag
```

## For Contributors

### Working on New Features
```bash
git checkout develop
git checkout -b feature/my-feature
# Make changes
git push origin feature/my-feature
# Create PR to develop branch
```

### Release Process
1. Features merged to develop
2. Create release/vX.Y.Z from develop
3. Test and fix bugs in release branch
4. Merge to main and tag
5. Merge back to develop

## Local Directory Strategy

For agents needing stable references:
```
~/github/
├── aget-worker-template/         # Working copy (any branch)
├── aget-template-v2.1.0/         # Frozen at v2.1.0
└── aget-template-v2.2.0-dev/     # Tracks develop branch
```

## Key Principles

1. **main is always stable** - Safe for production use
2. **develop is next** - Features for next release
3. **Tags are immutable** - Version references never change
4. **Clear communication** - Branch names indicate stability

---
*GitFlow-Lite adopted 2025-09-28 for clearer version management*