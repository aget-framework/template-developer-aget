# Template: Developer Agent

> Build, test, and review code with purpose-built development skills

**Version**: v3.6.0 | **Archetype**: Developer | **Skills**: 3 specialized + 14 universal

---

## Why Developer?

The Developer archetype brings **software engineering expertise** to your AI coding workflow. Unlike generic coding assistants, developer agents understand:

- **Test-driven development** — Run tests, interpret results, suggest fixes
- **Code quality standards** — Lint code with project-aware configuration
- **Review discipline** — Structured PR reviews with categorized feedback

**For evaluators**: If your team needs an AI that understands the full development lifecycle — not just code generation — the Developer archetype provides specialized skills for building, testing, and maintaining quality code.

---

## Skills

Developer agents come with **3 archetype-specific skills** plus the universal AGET skills.

### Archetype Skills

| Skill | Description |
|-------|-------------|
| **aget-run-tests** | Execute test suites (pytest, jest, go test) with auto-detection. Reports pass/fail counts, captures failures with locations, suggests next steps. |
| **aget-lint-code** | Run linting with project configuration (ruff, eslint, golangci-lint). Categorizes issues by severity, identifies auto-fixable problems. |
| **aget-review-pr** | Review pull requests for quality and standards. Produces structured feedback: blocking issues, suggestions, nitpicks, and praise. |

### Universal Skills

All AGET agents include session management, knowledge capture, and health monitoring:

- `aget-wake-up` / `aget-wind-down` — Session lifecycle
- `aget-create-project` / `aget-review-project` — Project management
- `aget-record-lesson` / `aget-capture-observation` — Learning capture
- `aget-check-health` / `aget-check-kb` / `aget-check-evolution` — Health monitoring
- `aget-propose-skill` / `aget-create-skill` — Skill development
- `aget-save-state` / `aget-file-issue` — State and issue management

---

## Ontology

Developer agents use a **formal vocabulary** of 10 concepts organized into 4 clusters:

| Cluster | Concepts |
|---------|----------|
| **Code Management** | Code, Code_Change |
| **Testing** | Test, Unit_Test, Integration_Test, Test_Result |
| **Build Management** | Build, Dependency |
| **Code Review** | Pull_Request, Code_Review |

This vocabulary enables precise communication about development artifacts and processes.

See: [`ontology/ONTOLOGY_developer.yaml`](ontology/ONTOLOGY_developer.yaml)

---

## Quick Start

```bash
# 1. Clone the template
git clone https://github.com/aget-framework/template-developer-aget.git my-dev-agent
cd my-dev-agent

# 2. Configure identity
# Edit .aget/version.json:
#   "agent_name": "my-dev-agent"
#   "domain": "your-domain"

# 3. Verify setup
python3 -m pytest tests/ -v
# Expected: All tests passing
```

### Try the Skills

```bash
# In Claude Code CLI
/aget-run-tests          # Execute project tests
/aget-lint-code          # Check code quality
/aget-review-pr 42       # Review PR #42
```

---

## What Makes Developer Different

| Aspect | Generic Coding AI | Developer Agent |
|--------|-------------------|-----------------|
| **Test execution** | Basic pytest run | Framework detection, failure analysis, suggested fixes |
| **Linting** | Single tool | Project-aware configuration precedence |
| **PR review** | Line-by-line comments | Structured review with blocking/suggestion/nitpick categories |
| **Vocabulary** | Informal | Formal ontology (Code_Change, Test_Result, Pull_Request) |

---

## Framework Specification

| Attribute | Value |
|-----------|-------|
| **Framework** | [AGET v3.6.0](https://github.com/aget-framework/aget) |
| **Archetype** | Developer |
| **Skills** | 17 total (3 archetype + 14 universal) |
| **Ontology** | 10 concepts, 4 clusters |
| **License** | Apache 2.0 |

---

## Learn More

- **[AGET Framework](https://github.com/aget-framework/aget)** — Core framework documentation
- **[Archetype Guide](https://github.com/aget-framework/aget/blob/main/docs/GETTING_STARTED.md)** — All 12 archetypes explained
- **[Getting Started](https://github.com/aget-framework/aget/blob/main/docs/GETTING_STARTED.md)** — Full onboarding guide

---

## Related Archetypes

| Archetype | Best For |
|-----------|----------|
| **[Worker](https://github.com/aget-framework/template-worker-aget)** | Task execution with progress reporting |
| **[Reviewer](https://github.com/aget-framework/template-reviewer-aget)** | Quality assurance and feedback |
| **[Architect](https://github.com/aget-framework/template-architect-aget)** | System design and tradeoff analysis |

---

**AGET Framework** | Apache 2.0 | [Issues](https://github.com/aget-framework/template-developer-aget/issues)
