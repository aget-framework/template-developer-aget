# AGET Template Family Comparison Matrix

**Version**: 1.0
**Last Updated**: 2025-10-10
**Purpose**: Guide users to the correct template for their use case

---

## Template Family Overview

The AGET framework provides **three specialized templates** for different agent roles:

| Template | Primary Use | Instance Type | Action Capability | Target Users |
|----------|-------------|---------------|-------------------|--------------|
| **template-worker-aget** | General-purpose work | Configurable (`aget` or `AGET`) | Configurable | Individual contributors, analysts, developers |
| **template-supervisor-aget** | Fleet coordination | Fixed (`AGET`) | Yes (manages agents) | Fleet managers, coordinators |
| **template-advisor-aget** | Advisory guidance | Fixed (`aget`) | No (read-only) | Domain experts, consultants, coaches |

---

## Detailed Capability Comparison

### Core Capabilities

| Capability | Worker | Supervisor | Advisor |
|------------|--------|------------|---------|
| **File Read** | ✅ Yes | ✅ Yes | ✅ Yes |
| **File Write** | ⚙️ Configurable | ✅ Yes | ❌ No (enforced) |
| **File Edit** | ⚙️ Configurable | ✅ Yes | ❌ No (enforced) |
| **Command Execution** | ⚙️ Configurable | ✅ Yes | ⚠️ Read-only only |
| **Analysis & Search** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Web Fetch** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Recommendations** | ⚙️ Optional | ⚙️ Optional | ✅ Primary purpose |

**Legend**:
- ✅ Yes = Always available
- ❌ No = Never available (enforced)
- ⚙️ Configurable = User chooses via configuration
- ⚠️ Limited = Available with restrictions

---

### Specialized Features

| Feature | Worker | Supervisor | Advisor |
|---------|--------|------------|---------|
| **Persona Differentiation** | ❌ No | ❌ No | ✅ Yes (5 personas) |
| **Multi-Agent Coordination** | ❌ No | ✅ Yes | ❌ No |
| **Agent Lifecycle Management** | ❌ No | ✅ Yes | ❌ No |
| **Confidence Levels in Output** | ⚙️ Optional | ⚙️ Optional | ✅ Required |
| **Assumption Documentation** | ⚙️ Optional | ⚙️ Optional | ✅ Required |
| **Trade-off Analysis** | ⚙️ Optional | ⚙️ Optional | ✅ Primary pattern |
| **Role Boundary Enforcement** | ❌ No | ❌ No | ✅ Yes (4 layers) |
| **Advisory Protocols (L114)** | ❌ No | ❌ No | ✅ Yes (built-in) |

---

### Configuration & Validation

| Aspect | Worker | Supervisor | Advisor |
|--------|--------|------------|---------|
| **Minimum Contract Tests** | 7 tests | 7 tests | 16 tests |
| **Instance Type Flexibility** | ✅ Can be `aget` or `AGET` | ❌ Must be `AGET` | ❌ Must be `aget` |
| **Persona Field** | ❌ Not used | ❌ Not used | ✅ Required |
| **Advisory Capabilities Section** | ❌ Not present | ❌ Not present | ✅ Required |
| **Role Enforcement Tests** | ❌ No | ❌ No | ✅ Yes (7 tests) |
| **Wake Protocol Validation** | ⚙️ Basic (3 tests) | ⚙️ Basic (3 tests) | ✅ Enhanced (6 tests) |

---

## When to Use Each Template

### Use **template-worker-aget** when:

✅ **You need flexibility**
- Want to switch between read-only and action-taking modes
- Need different capability profiles for different tasks
- Building general-purpose agent for varied work

✅ **You're building domain-specific tools**
- Data analysis agents (Spotify, financial data, logs)
- Code generation and modification agents
- Deployment and automation agents
- Research and documentation agents

✅ **You want standard agent capabilities**
- Standard wake/wind-down protocols
- Session management
- Learning evolution tracking
- No specialized communication styles needed

**Examples**:
- `my-spotify-analyst-aget` - Read-only data analysis
- `my-github-AGET` - GitHub PR creation and management
- `my-code-generator-AGET` - Scaffold and modify code
- `my-deployment-AGET` - Deploy to production environments

---

### Use **template-supervisor-aget** when:

✅ **You're coordinating multiple agents**
- Managing fleet of 5+ agents
- Orchestrating multi-agent workflows
- Enforcing cross-agent standards

✅ **You need lifecycle management**
- Creating and configuring new agents
- Migrating agents across versions
- Deploying patterns to agent fleet

✅ **You're doing framework R&D**
- Developing new AGET patterns
- Creating specifications (EARS format)
- Building shared learning repository

✅ **You have oversight responsibility**
- Reviewing agent work for quality
- Enforcing process protocols
- Coordinating releases

**Examples**:
- `my-supervisor-AGET` - Fleet coordinator managing 10 agents
- `team-lead-AGET` - Coordinating project team's agents
- `platform-manager-AGET` - Managing shared agent infrastructure

**Note**: Supervisor template currently **private** until patterns stabilize (expected v2.6+)

---

### Use **template-advisor-aget** when:

✅ **You want advisory-only mode**
- Never modify systems (compliance requirement)
- Always provide recommendations, never execute
- Read-only enforcement through contract tests

✅ **You need persona differentiation**
- **Teacher** - Educational content, structured learning
- **Mentor** - Career guidance, reflective questions
- **Consultant** - Trade-off analysis, formal recommendations
- **Guru** - Best practices, authoritative expertise
- **Coach** - Performance feedback, incremental improvement

✅ **You want built-in advisory protocols**
- Requirements Before Solutions (L114)
- Confidence levels in all recommendations
- Explicit assumption documentation
- Role boundary enforcement

✅ **You're building for governance**
- Architecture review boards
- Security advisory agents
- Code review agents (critique only)
- Decision support systems

**Examples**:
- `my-architecture-advisor-aget` (consultant persona) - System design guidance
- `my-security-advisor-aget` (guru persona) - Security best practices
- `my-code-review-coach-aget` (coach persona) - Code quality feedback
- `my-career-mentor-aget` (mentor persona) - Professional development

---

## Migration Between Templates

### Can I Convert Between Templates?

| From | To | Difficulty | Notes |
|------|-----|-----------|-------|
| Worker → Advisor | ⚠️ Medium | Requires validation of read-only compliance, add persona config, expand tests to 16 |
| Worker → Supervisor | ⚠️ Medium | Requires multi-agent patterns, coordination protocols, fleet context |
| Advisor → Worker | ⚠️ Medium | **One-way door**: Removes read-only enforcement, requires architecture review |
| Advisor → Supervisor | ❌ Discouraged | Conflates advisory and execution roles (see D11 terminology) |
| Supervisor → Worker | ❌ Discouraged | Loses coordination capabilities, better to create separate agent |
| Supervisor → Advisor | ❌ Discouraged | Supervisors need action capability for agent management |

**Recommendation**: Start with the right template. Template conversions require significant rework and risk configuration drift.

---

## Decision Tree

```
Do you need to modify files or execute commands with side effects?
├─ YES → Continue below
│   └─ Are you managing 5+ other agents?
│       ├─ YES → Use template-supervisor-aget
│       └─ NO → Use template-worker-aget
│
└─ NO (read-only only) → Continue below
    └─ Do you need persona-based communication styles?
        ├─ YES → Use template-advisor-aget
        └─ NO → Use template-worker-aget (configure as read-only)
```

---

## Quick Reference Table

| Your Need | Recommended Template | Key Reason |
|-----------|---------------------|------------|
| Flexible capability (switch modes) | Worker | Configurable instance_type |
| Data analysis (read-only) | Worker or Advisor | Worker if no persona needed, Advisor for guidance style |
| Code generation/modification | Worker | Needs write capabilities |
| GitHub automation | Worker | Needs action capabilities (PRs, merges) |
| Architecture guidance | **Advisor** | Built-in trade-off analysis, consultant persona |
| Code review feedback | **Advisor** | Critique protocols, coach persona |
| Career mentorship | **Advisor** | Reflective questions, mentor persona |
| Teaching concepts | **Advisor** | Structured learning, teacher persona |
| Security guidance | **Advisor** | Best practices, guru persona |
| Fleet coordination | **Supervisor** | Multi-agent orchestration |
| Pattern deployment | **Supervisor** | Framework R&D capabilities |
| Release management | **Supervisor** | Lifecycle and coordination |

---

## Template Maturity Status

| Template | Status | Public Availability | Stability |
|----------|--------|---------------------|-----------|
| **template-worker-aget** | ✅ Stable | Public (aget-framework/template-worker-aget) | v2.5.0 |
| **template-supervisor-aget** | 🚧 Stabilizing | Private (gmelli/template-supervisor-aget) | v2.5.0 |
| **template-advisor-aget** | ✅ Stable | Public (aget-framework/template-advisor-aget) | v2.5.0 |

**Expected Public Release**:
- Worker: ✅ Already public
- Advisor: ✅ Public with v2.5.0
- Supervisor: 🔜 Expected v2.6.0+ (patterns stabilizing)

---

## Getting Started

### Clone the Right Template

```bash
# Worker template (flexible capability)
git clone https://github.com/aget-framework/template-worker-aget.git my-{purpose}-{AGET|aget}

# Advisor template (read-only + persona)
git clone https://github.com/aget-framework/template-advisor-aget.git my-{domain}-advisor-aget

# Supervisor template (fleet coordination) - Private until v2.6+
# Contact framework maintainer for access
```

### Next Steps

1. **Configure identity** - Edit `.aget/version.json`
2. **Run contract tests** - Validate: `python3 -m pytest tests/ -v`
3. **Customize documentation** - Update `AGENTS.md` with domain context
4. **Deploy** - Create GitHub repository (optional)

**Detailed guides**:
- Worker: See `template-worker-aget/docs/GET_STARTED.md`
- Advisor: See `template-advisor-aget/.aget/docs/CREATING_ADVISOR_AGENTS.md`
- Supervisor: Documentation pending v2.6 public release

---

## Support

**Questions about which template to use?**
- File issue: [aget-aget hub](https://github.com/gmelli/aget-aget/issues) with `[template-selection]` prefix
- Review: This comparison matrix
- Check: Template README.md files for feature details

**Template-specific questions**:
- Worker: `[worker-template]` prefix
- Advisor: `[advisor-template]` prefix
- Supervisor: `[supervisor-template]` prefix

---

*Template Family v2.5.0 | Framework: aget-framework | Updated: 2025-10-10*
