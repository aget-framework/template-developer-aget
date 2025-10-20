# Privacy Considerations for AGET Templates

**Created**: 2025-09-28
**Critical**: This document records privacy requirements for AGET releases

## Key Privacy Rules

### 1. No Private Agent Names in Public Templates
- Never include `my-*` prefixed agents in public documentation
- These are personal/private implementations
- Use generic examples like `example-agent` or `your-project-name`

### 2. No Personal Workspace Information
- Don't expose personal directory structures
- Don't include actual GitHub usernames in examples (use placeholders)
- Don't reference specific private projects

### 3. README Content Rules

#### ✅ GOOD Examples (Generic):
```markdown
- **example-analytics-agent** - Analytics and reporting
- **your-project-name** - Your project description
- **sample-tool-aget** - Tool automation example
```

#### ❌ BAD Examples (Exposes Private Info):
```markdown
- **my-AGET-aget** - Gabor's private agent
- **my-CCB-aget** - Personal implementation
- **/Users/gabormelli/github/...** - Personal paths
```

## Template README Guidelines

1. Use placeholder names in examples
2. Use generic project descriptions
3. Never reference actual private agent names
4. Keep examples focused on public, shareable patterns

## Privacy Checklist for Releases

- [ ] No `my-*` agent names in documentation
- [ ] No personal file paths
- [ ] No private project references
- [ ] No personal GitHub usernames (except in LICENSE)
- [ ] No internal company/personal project details

## Lesson Learned

During v2.1 preparation, we almost exposed 9 private agent names in the workspace README. This was caught during review but highlights the need for privacy consciousness when creating public templates from private workspaces.

---
*Remember: Templates are public. Keep private details private.*