# Template Developer AGET

> **Code Analysis Advisor Template** - Pre-configured agent for code quality, standards compliance, debugging assistance, and specification consistency analysis

Transform your codebase into insights with an AI advisor specialized in code analysis. Provides expert recommendations on code quality, standards compliance, debugging strategies, and spec-to-code consistency - without modifying your code.

**Current Version**: v2.9.0

**Template Type**: Developer (Code Analysis Advisor)

---

## What This Is

**An advisory agent for code analysis** - Analyzes code quality, checks standards compliance, assists with debugging, and validates spec consistency. Provides recommendations and insights without executing changes.

**Mental Model**:
```
Your Code → Analysis Request → AI Advisor → Runs Pattern Analysis → Recommends Improvements
```

Your advisor analyzes code metrics, detects issues, ranks hypotheses, and recommends fixes - but never modifies files or executes commands.

---

## Quick Start (5 Minutes)

### 1. Clone and Configure

```bash
# Create your code analysis advisor instance
git clone https://github.com/aget-framework/template-developer-aget.git my-code-advisor-aget
cd my-code-advisor-aget

# Update agent identity
# Edit .aget/version.json and set:
#   "agent_name": "my-code-advisor-aget"
#   "domain": "code-analysis"
```

### 2. Verify Installation

```bash
# Run contract tests
python3 -m pytest tests/ -v

# Expected: 21/21 tests passing
```

### 3. Run Example

```bash
# Try code quality analysis example
cd examples/code_quality_analysis
python3 run_analysis.py

# See analysis of sample code with quality issues
```

---

## Key Capabilities

### 1. Code Quality Analysis

Analyzes code complexity, maintainability, technical debt, and code smells.

**Metrics**:
- Cyclomatic complexity (decision point counting)
- Maintainability index (0-100 scale)
- Technical debt detection (TODO/FIXME/HACK)
- Code smell detection (long methods, high complexity, nested conditionals)
- Overall quality rating (0-10)

**Example**:
```python
from patterns.analysis.code_quality import analyze

result = analyze({
    "repo_path": "./src",
    "language": "python"
})

print(f"Overall Quality: {result['overall_quality']}/10")
print(f"Complexity: {result['metrics']['complexity']['avg_cyclomatic']}")
print(f"Maintainability: {result['metrics']['maintainability']['index']}/100")
```

### 2. Standards Compliance Checking

Checks code against coding standards with configurable precedence.

**Standards Precedence**:
1. **Repo-specific** (`.coding-standards.md` in repo root)
2. **Agent-level** (custom standards in `.aget/`)
3. **Built-in** (PEP-8 for Python, ESLint for JavaScript, gofmt for Go)

**Example**:
```python
from patterns.analysis.standards_check import analyze

result = analyze({
    "repo_path": "./src",
    "language": "python",
    "standards": "auto"  # Use precedence order
})

print(f"Compliance Rating: {result['compliance_rating']}/10")
print(f"Standards Applied: {result['standards_applied']}")
```

### 3. Debugging Assistance

Analyzes errors and provides ranked root cause hypotheses with fix strategies.

**Error Patterns Recognized**:
- null_pointer_exception (AttributeError with 'NoneType')
- missing_dict_key (KeyError)
- list_index_out_of_range (IndexError)
- calling_non_function (TypeError "not callable")
- async_await_missing (RuntimeError "coroutine never awaited")
- And more...

**Example**:
```python
from patterns.analysis.debug_assist import analyze

result = analyze({
    "error_type": "AttributeError",
    "error_message": "'NoneType' object has no attribute 'split'",
    "code_context": {
        "file": "app.py",
        "line": 22,
        "code_snippet": "email_parts = user.email.split('@')"
    }
})

print(f"Error Pattern: {result['error_pattern']}")
for hypothesis in result['root_cause_hypotheses']:
    print(f"{hypothesis['rank']}. {hypothesis['cause']} ({hypothesis['confidence']})")
```

### 4. Specification Consistency

Compares code implementation against formal specifications to detect gaps and drift.

**Spec Format Support**:
- **YAML** (with capabilities or EARS requirements)
- **Markdown** (CAP-XXX or REQ-XXX identifiers)
- **Plain text** (numbered or bulleted lists)

**Example**:
```python
from patterns.analysis.spec_consistency import analyze

result = analyze({
    "spec_path": "./spec.yaml",
    "repo_path": "./src",
    "language": "python"
})

print(f"Coverage: {result['coverage']['percentage']}%")
print(f"Gaps: {len(result['gaps'])} missing capabilities")
```

### 5. Multi-Repository Scanning

Discovers and analyzes multiple repositories for consistency and shared patterns.

**Discovery Modes**:
- **Auto-scan**: Automatically discover git repositories in base path
- **Configured**: Use explicit include/exclude lists from `.aget/config/repos.yaml`

**Example**:
```python
from patterns.analysis.multi_repo_scan import analyze

result = analyze({
    "scan_mode": "auto",
    "base_path": "~/github",
    "analysis_type": "consistency"
})

print(f"Discovered: {result['repos_discovered']} repositories")
```

---

## Examples

All examples are runnable and validated. Each includes:
- Sample code/specification demonstrating the pattern
- Runnable script using pattern's `analyze()` function
- README with usage instructions and learning points

### Run Examples

```bash
# Validate all examples
./scripts/validate_examples.sh

# Or run individually
cd examples/code_quality_analysis && python3 run_analysis.py
cd examples/standards_checking && python3 run_check.py
cd examples/debugging_assistance && python3 run_debug.py
cd examples/spec_consistency && python3 run_check.py
```

**Example Scenarios**:
- **code_quality_analysis**: Analyzes code with high complexity and technical debt
- **standards_checking**: Detects PEP-8 violations (E501, E722, W293)
- **debugging_assistance**: Analyzes TypeError from None subscript
- **spec_consistency**: Detects 60% gap between spec and implementation

---

## Pattern Usage

All patterns follow a common interface:

```python
def analyze(input_data: dict) -> dict:
    """
    Args:
        input_data: Analysis parameters (pattern-specific)

    Returns:
        dict: Analysis results with status, metrics, recommendations
    """
```

### Pattern Locations

```
.aget/patterns/analysis/
├── code_quality.py          # Code quality metrics
├── standards_check.py       # Standards compliance
├── debug_assist.py          # Error analysis
├── spec_consistency.py      # Spec-to-code validation
├── multi_repo_scan.py       # Multi-repo discovery
└── __init__.py              # Common interface
```

### Import Patterns

```python
import sys
import os

# Add .aget to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.aget'))

from patterns.analysis.code_quality import analyze
from patterns.analysis.standards_check import analyze
# ... etc
```

---

## Contract Testing

The template includes 21 contract tests (10 inherited from advisor template + 11 developer-specific).

**Run Tests**:
```bash
# Run all contract tests
python3 -m pytest tests/ -v

# Run developer-specific tests only
python3 -m pytest tests/test_developer_contract.py -v

# Expected: 21/21 passing
```

**Test Coverage**:
- Multi-repo discovery (auto-scan, configured mode, exclusions)
- Standards precedence (repo-specific, agent-level, built-in)
- Code analysis capabilities (quality, standards, debug, spec)
- Advisory enforcement (no write operations outside .aget/)

---

## Documentation

Comprehensive guides for each pattern:

- **docs/CODE_QUALITY_GUIDE.md** - Metrics, thresholds, interpretation
- **docs/STANDARDS_CHECKING_GUIDE.md** - Precedence, customization, built-in standards
- **docs/DEBUG_ASSISTANCE_GUIDE.md** - Error patterns, hypothesis ranking, investigation paths
- **docs/SPEC_CONSISTENCY_GUIDE.md** - Spec formats, gap detection, EARS patterns
- **docs/MULTI_REPO_CONFIGURATION.md** - Discovery modes, consistency analysis

---

## Customization

### Add Custom Standards

Create `.coding-standards.md` in your repository:

```markdown
# Coding Standards

Max line length: 120

Rules:
- Use descriptive variable names (>3 characters)
- Document all public functions
- Handle exceptions explicitly (no bare except)
```

The pattern will auto-detect and apply these standards.

### Configure Multi-Repo Scanning

Create `.aget/config/repos.yaml`:

```yaml
repos:
  include:
    - ~/projects/repo-1
    - ~/projects/repo-2
  exclude:
    - vendor
    - archive
```

---

## Template Philosophy

**Advisory-Only**: This template follows the advisor pattern - it analyzes and recommends but never modifies code. All patterns return analysis results as dictionaries, not side effects.

**Minimal Configuration**: Works out-of-the-box with built-in standards and auto-discovery. Customization is optional.

**Composable Patterns**: Each pattern is independent and focused. Combine patterns to build comprehensive analysis workflows.

**Educational**: Examples and documentation emphasize learning - showing how patterns work and why recommendations matter.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Adding new patterns
- Testing guidelines
- Code style

---

## Specification

| Attribute | Value |
|-----------|-------|
| **Governed By** | [AGET_TEMPLATE_SPEC v3.1](https://github.com/aget-framework/aget/blob/main/specs/AGET_TEMPLATE_SPEC.md) |
| **Foundation** | [WORKER_TEMPLATE_SPEC v1.0](https://github.com/aget-framework/aget/blob/main/specs/WORKER_TEMPLATE_SPEC_v1.0.yaml) |
| **Archetype** | Developer |
| **Manifest Version** | 3.0 |
| **Contract Tests** | 168 tests |

### Key Capabilities

| ID | Capability | Pattern |
|----|------------|---------|
| CAP-001 | Wake Protocol | event-driven |
| CAP-009 | Wind Down Protocol | event-driven |
| CAP-017 | File Write Operations | optional |
| CAP-DEV | Code Analysis Patterns | ubiquitous |

Validate compliance: `pytest tests/ -v`

See: [Full specification](https://github.com/aget-framework/aget/tree/main/specs)

---

## Version History

- **v3.0.0** - 5D Composition Architecture
  - Manifest v3 schema, 5D directories
  - 168 contract tests
- **v2.9.0** - Initial developer template release
  - 5 analysis patterns (quality, standards, debug, spec, multi-repo)

---

## License

**AGET Framework (This Template)**: Apache License 2.0

This template and all framework code (`.aget/` structure, patterns, protocols) are licensed under the Apache License 2.0. This ensures:

- **Patent protection** for all adopters
- **Freedom to fork**, modify, and redistribute
- **Enterprise-safe** licensing for production use

See [LICENSE](LICENSE) for full terms.

**Your Agent Instance**: Your Choice

When you create an agent from this template, **you choose the license** for your specific instance:

- Keep it Apache 2.0 (recommended for public/shared agents)
- Make it private (all rights reserved)
- Choose MIT, GPL, or any other license

**The framework is open commons. What you build with it is yours.**

### Why Apache 2.0?

AGET is production infrastructure for agent configuration and lifecycle management. Apache 2.0 provides:

1. **Patent Grant**: Contributors can't patent their contributions and sue adopters
2. **Patent Retaliation**: If someone sues for patent infringement, they lose their license
3. **Ecosystem Immunity**: The standard stays free even as it becomes valuable
4. **Enterprise Adoption**: Legal teams approve Apache 2.0 more readily than other licenses

This follows the precedent of Kubernetes, Android, Swift, and other infrastructure projects.

### Upgrading Existing Agents

If you created an agent from an earlier MIT-licensed template, no action is required. Your agent remains valid under MIT (grandfathered).

To upgrade to Apache 2.0 for patent protection benefits, see the upgrade guide in the [AGET Framework documentation](https://github.com/aget-framework).

---

## Related Templates

- **template-advisor-aget** - General-purpose advisory template with persona-based guidance
- **template-worker-aget** - Configurable action-taking agent template
- **template-supervisor-aget** - Fleet coordination and multi-agent orchestration

---

## Support

- **Issues**: https://github.com/aget-framework/template-developer-aget/issues
- **Framework**: https://github.com/aget-framework
- **Documentation**: See `docs/` directory

---

**Built with**: AGET Framework v2.9.0 | **Template Type**: Developer (Code Analysis Advisor)
