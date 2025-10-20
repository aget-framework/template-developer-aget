# Public vs Private Repository Guidelines

## Quick Reference

### ✅ Belongs in aget-cli-agent-template (PUBLIC)
- Installation instructions
- User guides and tutorials
- API documentation
- Template documentation
- Pattern explanations
- Troubleshooting guides
- Contributing guidelines
- License and security info
- Changelog for releases

### ❌ Does NOT Belong in aget-cli-agent-template
- Test migration reports (DAY_X_STATUS.md)
- Internal test plans
- Session notes
- Hours tracking
- Internal project names (spotify-aget, llm-judge-aget)
- Development schedules
- Team discussions
- Bug reproduction steps
- Performance benchmarks from testing

### 🔒 Belongs in aget-aget (PRIVATE)
- Test documentation
- Migration tracking
- Internal roadmaps
- Session notes
- Development logs
- Test project management
- Cross-project coordination
- Internal tooling
- Pre-release testing

## Decision Tree

```
Is this document...
├── For end users? → PUBLIC (aget-cli-agent-template)
├── About using AGET? → PUBLIC
├── About installing AGET? → PUBLIC
├── API/Pattern reference? → PUBLIC
└── About our development?
    ├── Test results? → PRIVATE (aget-aget)
    ├── Internal planning? → PRIVATE
    ├── Session notes? → PRIVATE
    └── Bug investigations? → PRIVATE
```

## Examples

### PUBLIC Example: README.md
```markdown
# AGET: CLI Agent Template

AGET helps you make any codebase AI-agent ready in <60 seconds.

## Installation
curl -sSL https://... | bash

## Quick Start
aget init --template agent
```

### PRIVATE Example: Test Report
```markdown
# Day 2 Migration Test

Tested spotify-aget with advanced template...
Found bug in session_protocol.py line 67...
Hours spent: 4.5
```

## File Patterns

### Always PUBLIC
- README.md
- LICENSE
- CHANGELOG.md
- docs/*.md (user guides)
- examples/*.py
- templates/*

### Always PRIVATE
- DAY_*_*.md
- *_TEST_*.md
- SESSION_NOTES/*
- *_STATUS.md
- *migration-report*
- test-results/*

### Context-Dependent
- ROADMAP.md → Public version (features) vs Private version (hours/deadlines)
- Issues → Public (bugs/features) vs Private (security/planning)
- Benchmarks → Public (performance guarantees) vs Private (test results)

## Pre-Release Checklist

Before making repository public:

1. **Audit all .md files**
   ```bash
   find . -name "*.md" -exec grep -l "spotify-aget\|llm-judge-aget\|hour\|Day [0-9]" {} \;
   ```

2. **Check for internal references**
   ```bash
   grep -r "internal\|private\|TODO\|FIXME\|XXX" --include="*.md"
   ```

3. **Verify no session notes**
   ```bash
   [ -d "SESSION_NOTES" ] && echo "WARNING: Session notes still present"
   ```

4. **Clean test artifacts**
   ```bash
   find . -name "*test-report*" -o -name "*migration-report*"
   ```

## Migration Command

Quick migration to aget-aget:
```bash
# In aget-cli-agent-template
./scripts/move_internal_to_private.sh

# Verify cleanup
./scripts/verify_public_ready.sh
```

## Maintaining Separation

### When Committing
Ask yourself:
- Would a user need this?
- Does this expose internal process?
- Is this about using or developing AGET?

### When Documenting
- User task → aget-cli-agent-template
- Development task → aget-aget
- Test result → aget-aget
- Feature explanation → aget-cli-agent-template

### When Testing
- Test code → aget-cli-agent-template
- Test results → aget-aget
- Test plans → aget-aget
- Test examples → aget-cli-agent-template

---
*This separation ensures users see a clean, professional framework*
*while we maintain detailed development history privately*