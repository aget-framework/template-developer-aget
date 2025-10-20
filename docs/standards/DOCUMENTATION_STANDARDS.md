# Documentation Standards

## Naming Convention: User-Goal ALL-CAPS

All documentation files must follow this pattern:

### Core Principle
**"Documentation files must complete the sentence: 'I want to...'"**

### Format
- ALL-CAPS with underscores: `VERB_OBJECT.md`
- Start with action verb when possible
- Focus on user goals, not technical concepts

### Examples
```
GET_STARTED.md         # "I want to get started"
WRITE_PATTERNS.md      # "I want to write patterns"
FIX_PROBLEMS.md        # "I want to fix problems"
USE_COMMANDS.md        # "I want to use commands"
CHOOSE_TEMPLATE.md     # "I want to choose a template"
CONTRIBUTE_PATTERNS.md # "I want to contribute patterns"
UNDERSTAND_AGET.md     # "I want to understand AGET"
```

### Why ALL-CAPS?
1. **Visual hierarchy** - Documentation stands out from code
2. **Authority** - These are THE official docs
3. **Unix tradition** - Follows README, LICENSE, CHANGELOG convention
4. **Instant recognition** - Users know these are guides, not code

### Anti-patterns to Avoid
```
❌ scaffolding.md         # lowercase lacks presence
❌ SCAFFOLDING.md        # noun-focused, not user-goal
❌ AGET_SCAFFOLDING.md   # prefix redundant in docs/
❌ HowToScaffold.md      # camelCase inconsistent
```

### Special Files
These standard files keep their conventional names:
- `README.md` - Directory overview
- `MISSION.md` - Project mission statement
- `LICENSE.md` - Legal information
- `CHANGELOG.md` - Version history

## Enforcement

The pattern validator (in aget-aget) checks documentation naming:
```python
def validates_doc_name(filename):
    # Must be ALL_CAPS
    # Should start with verb
    # Should complete "I want to..."
```

## Migration

When renaming docs, update all references:
1. In README.md links
2. In other docs cross-references
3. In pattern outputs
4. In test fixtures

---
*Standard established: 2025-09-25*
*Part of AGET v2.0 quality standards*