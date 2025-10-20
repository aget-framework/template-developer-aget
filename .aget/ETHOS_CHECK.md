# AGET Ethos Check for Releases

## Purpose
Ensure all public-facing content aligns with humble CLI developer values.

## Pre-Release Ethos Checklist

### Language Check
- [ ] No marketing speak ("revolutionary", "game-changing", "unleash")
- [ ] No grandiose naming ("The X Release", "Project Codename")
- [ ] No flowery metaphors ("beautiful universe", "journey to excellence")
- [ ] No corporate buzzwords ("synergy", "leverage", "paradigm")

### Tone Check
- [ ] Technical and factual over emotional
- [ ] Descriptive over prescriptive
- [ ] Humble over boastful
- [ ] Functional over aspirational

### README Audit
```bash
# Quick scan for problematic phrases
grep -i "beautiful\|universe\|journey\|revolutionary\|unleash\|paradigm" README.md

# Check for superlatives
grep -i "best\|amazing\|incredible\|awesome\|perfect" README.md
```

### Commit Message Standards
- Use conventional commits (feat:, fix:, docs:, etc.)
- Describe what changed, not why it's amazing
- Keep it technical and brief

### Release Notes Format
```
## v2.1.0

### Added
- File ownership via aget_ prefix
- Migration script for v2.0 users

### Fixed
- Root directory clutter
- Privacy leaks in examples

### Changed
- Documentation moved to docs/
```

Not: "v2.1.0 - The Ownership Revolution!"

### Version Naming
- Just use version numbers: v2.1.0
- Add brief description if needed: "v2.1.0 (file ownership update)"
- Avoid: Release names, code names, thematic titles

## Quick Ethos Test

Ask yourself:
1. Would Linus Torvalds roll his eyes at this?
2. Does it sound like a UNIX man page (good) or a startup pitch (bad)?
3. Can I explain it to another developer in one sentence without adjectives?
4. Would this fit in a GNU project announcement?

## Example Transformations

❌ "Revolutionize your development workflow with our beautiful patterns"
✅ "Patterns for common development tasks"

❌ "The Ultimate CLI Agent Template Solution"
✅ "CLI agent template"

❌ "Embark on a journey to coding excellence"
✅ "Build software with AI assistance"

## Enforcement

Add to pre-release script:
```bash
# Ethos check
echo "Checking README for ethos alignment..."
if grep -qi "beautiful\|universe\|journey\|revolutionary" README.md; then
    echo "⚠️ Warning: Potentially misaligned language detected"
    echo "Run: grep -ni 'beautiful\|universe\|journey' README.md"
fi
```

## Philosophy

The best software speaks through its utility, not its marketing. Let the code quality and documentation clarity be the differentiator. Keep it simple, functional, and honest.

---
*Remember: We're toolsmiths, not poets.*