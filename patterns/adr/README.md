# Architectural Decision Records (ADR) Pattern for AGET

## Overview

ADRs document significant architectural decisions, providing context that helps CLI agents understand project constraints and avoid proposing solutions that violate established principles.

Based on Michael Nygard's original format and industry best practices from Microsoft, AWS, and the broader software architecture community.

## Why ADRs Matter for CLI Agents

### Without ADRs
- Agents repeatedly propose rejected solutions
- No understanding of historical context
- Violations of unstated constraints
- Wasted effort on impossible changes

### With ADRs
- Agents check decisions before proposing
- Respect established boundaries
- Build on documented rationale
- Understand trade-offs made

## The 10 Best Practices (Industry Standard)

### 1. **Use Consistent Template**
- Follow the template in `adr_template.md`
- Include: Title, Status, Context, Decision, Consequences
- Maintain uniform structure across all ADRs

### 2. **Focus on Architecturally Significant Decisions**
Only document decisions that:
- Affect system structure
- Impact non-functional requirements
- Choose technology stacks
- Define integration approaches
- Establish security boundaries

### 3. **One Decision Per Record**
- Keep ADRs focused and atomic
- Cross-reference related decisions
- Easier review and maintenance

### 4. **Document Context Thoroughly**
Capture:
- Business drivers
- Technical constraints
- Team capabilities
- Timeline pressures
- Regulatory requirements

### 5. **Include Alternatives and Trade-offs**
For each alternative, document:
- Description
- Pros and cons
- Cost implications
- Risk assessment
- Reason for rejection

### 6. **Implement Review Process**
Before accepting ADRs:
- Stakeholder review
- Technical validation
- Security assessment
- 1-3 review cycles maximum

### 7. **Store with Codebase**
- Keep in `docs/adr/` directory
- Version control with code
- Accessible to all developers
- Synchronized with implementation

### 8. **Use Clear Status Indicators**
- **Draft**: Being written
- **Proposed**: Ready for review
- **Accepted**: Approved and active
- **Deprecated**: No longer valid
- **Superseded**: Replaced by newer ADR

### 9. **Write for Multiple Audiences**
Consider readers:
- New team members
- Current developers
- Technical architects
- Business stakeholders
- Compliance auditors

### 10. **Maintain and Evolve**
- Regular relevance reviews
- Template refinement
- Process optimization
- Tool integration
- Team training

## AGET-Specific Implementation

### Directory Structure
```
docs/adr/
├── ADR-001-AGET-SCOPE.md           # AGET's own scope decision
├── ADR-002-PROJECT-SCOPE.md        # Project-specific scope
├── ADR-003-TECH-STACK.md           # Technology choices
├── ADR-004-SECURITY.md             # Security boundaries
├── ADR-005-PERFORMANCE.md          # Performance requirements
├── adr_template.md                  # Template for new ADRs
└── README.md                        # This file
```

### Integration with AGENTS.md

Add to your AGENTS.md:

```markdown
## Architectural Decisions

### Check Decisions
When user says "check decisions" or "list ADRs":
- Run: `ls docs/adr/ADR-*.md | head -10`
- Show status and title of each ADR

### Search Decisions
When user asks "why do we..." or "what was decided about...":
- Search ADRs for relevant keywords
- Reference specific ADR numbers
- Quote decision and rationale

### Propose Change
When user says "should we change..." or "I propose...":
1. Check for conflicting ADRs
2. If conflict found, explain existing decision
3. If no conflict, offer to create new ADR

### Create ADR
When user says "document decision" or "create ADR":
- Copy adr_template.md to new file
- Sequential numbering (ADR-NNN)
- Guide through sections
```

### CLI Agent Workflow

```python
# Pattern for agents to check ADRs
def before_proposing_change(proposal):
    """Check ADRs before suggesting changes"""

    # 1. Search existing ADRs
    relevant_adrs = search_adrs(proposal.keywords)

    # 2. Check for conflicts
    for adr in relevant_adrs:
        if conflicts_with(proposal, adr):
            return f"Conflicts with {adr.title}: {adr.decision}"

    # 3. Build on existing decisions
    related = find_related_adrs(proposal)
    if related:
        proposal.add_context(f"Builds on: {related}")

    return proposal
```

## Standard ADRs for AGET Projects

### Minimal Template (3 ADRs)
1. **ADR-001**: Project Scope and Boundaries
2. **ADR-002**: Core Technology Stack
3. **ADR-003**: Security and Privacy

### Standard Template (5 ADRs)
All minimal plus:
4. **ADR-004**: Performance Requirements
5. **ADR-005**: Breaking Change Policy

### Advanced Template (8+ ADRs)
All standard plus domain-specific decisions

## Examples

### Example: AGET's Own Scope Decision
```markdown
# ADR-001: AGET Scope Boundaries

**Date**: 2025-09-22
**Status**: Accepted
**Category**: Scope

## Context
Proposal to add database consolidation patterns raised questions about AGET's mission.

## Decision
AGET remains focused on conversation layer only.

## Consequences
**Positive**: Maintains simplicity and focus
**Negative**: Some useful patterns excluded
```

### Example: Technology Choice
```markdown
# ADR-003: Python-Only Implementation

**Date**: 2025-09-22
**Status**: Accepted

## Context
Need universal scripting language for patterns.

## Decision
Use Python 3.8+ exclusively for all patterns.

## Alternatives Considered
- **Bash**: Not portable to Windows
- **JavaScript**: Requires Node.js installation
```

## Automation Support

### ADR Creation Helper
```bash
# Create new ADR
python patterns/adr/create_adr.py --title "API Rate Limiting"

# Check for conflicts
python patterns/adr/check_conflicts.py --proposal "change to PostgreSQL"

# Generate ADR index
python patterns/adr/generate_index.py > docs/adr/INDEX.md
```

## Quality Checklist

Before accepting an ADR:
- [ ] Follows standard template
- [ ] Architecturally significant
- [ ] Context fully documented
- [ ] Alternatives analyzed
- [ ] Consequences clear
- [ ] Review triggers defined
- [ ] Status accurate
- [ ] Numbered sequentially

## Common Pitfalls to Avoid

1. **Too Many ADRs**: Not every decision needs an ADR
2. **Too Few Details**: Context is crucial for future understanding
3. **Missing Alternatives**: Shows incomplete analysis
4. **No Review Triggers**: Decisions become stale
5. **Deleting ADRs**: Mark as deprecated/superseded instead

## References

- [Michael Nygard's Original ADR Article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [AWS ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs/)
- [Microsoft ADR Guidance](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [ADR GitHub Organization](https://adr.github.io)

---
*Teaching CLI agents to respect decisions through documented rationale*