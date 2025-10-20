# [PROJECT NAME] Business Rules

> The policies and logic that govern your system's behavior

## Getting Started
<!-- Start with the rules you're certain about -->

### BR-001: [Most Important Rule]
**Rule**: <!-- What must always be true? -->
**Rationale**: <!-- Why does this rule exist? -->
**Example**: <!-- Show a specific case -->
**Exceptions**: <!-- When doesn't this apply? -->

---

## Rule Categories
<!-- Organize rules as you discover them -->

### Data Validation Rules
<!-- What makes data valid or invalid? -->

#### BR-___: [Data Constraint]
**Rule**: <!-- e.g., "Email addresses must be unique" -->
**Implementation**: <!-- Where is this enforced? -->
**Error Handling**: <!-- What happens when violated? -->

### Business Logic Rules
<!-- Domain-specific policies -->

#### BR-___: [Business Policy]
**Rule**: <!-- e.g., "Orders over $100 get free shipping" -->
**Conditions**: <!-- When does this apply? -->
**Source**: <!-- Business requirement, regulation, etc. -->

### Security Rules
<!-- What must be protected? -->

#### BR-___: [Security Constraint]
**Rule**: <!-- e.g., "Passwords must be hashed, never stored plain" -->
**Enforcement**: <!-- How is this guaranteed? -->
**Audit**: <!-- How do we verify compliance? -->

### Performance Rules
<!-- Response time, throughput, resource limits -->

#### BR-___: [Performance Constraint]
**Rule**: <!-- e.g., "API responses must be under 200ms" -->
**Measurement**: <!-- How do we measure? -->
**Optimization**: <!-- How do we achieve this? -->

### Integration Rules
<!-- How external systems are handled -->

#### BR-___: [Integration Policy]
**Rule**: <!-- e.g., "Retry failed API calls 3 times" -->
**Systems**: <!-- Which integrations? -->
**Fallback**: <!-- What if it still fails? -->

---

## Discovery Checklist

### Look for Rules in:
- [ ] **Validation functions** - What's being checked?
- [ ] **Constants/Config** - Magic numbers, thresholds
- [ ] **Comments** - Often explain why
- [ ] **Error messages** - Reveal constraints
- [ ] **Test cases** - Show expected behavior
- [ ] **Database constraints** - Unique, not null, foreign keys
- [ ] **API documentation** - Rate limits, formats
- [ ] **Conditional logic** - If/then patterns

### Common Rule Patterns:
- **Boundaries**: Min/max values, length limits
- **Formats**: Email, phone, date patterns
- **States**: Valid transitions, workflows
- **Permissions**: Who can do what
- **Time**: Expiration, deadlines, schedules
- **Calculations**: Formulas, algorithms
- **Defaults**: What happens if not specified

---

## Rule Conflicts
<!-- Document when rules contradict -->

| Rule 1 | Rule 2 | Resolution |
|--------|--------|------------|
| <!-- Rule --> | <!-- Conflicting rule --> | <!-- How to resolve --> |

---

## Compliance & Standards
<!-- External requirements -->

### Regulatory
- <!-- GDPR, HIPAA, PCI, etc. -->

### Industry Standards
- <!-- ISO, RFC, etc. -->

### Company Policies
- <!-- Internal standards -->

---

## Notes
<!-- Track your understanding as it evolves -->

**Discovered Rules**:
- <!-- Rules found in code but not documented -->

**Uncertain Rules**:
- <!-- Rules you think exist but need confirmation -->

**Missing Rules**:
- <!-- Places where rules should exist but don't -->

---

*Template Version: 1.0*
*Last Updated: [DATE]*
*Confidence Level: [LOW/MEDIUM/HIGH]*