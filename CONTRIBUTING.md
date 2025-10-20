# Contributing to Template Developer AGET

Thank you for your interest in contributing to the Template Developer AGET! This guide will help you get started.

---

## Development Setup

### Prerequisites

- Python 3.8+
- pytest for testing
- git for version control

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/aget-framework/template-developer-aget.git
cd template-developer-aget

# Install development dependencies (if needed)
pip install pytest pyyaml

# Run tests to verify setup
python3 -m pytest tests/ -v
```

---

## Project Structure

```
template-developer-aget/
├── .aget/
│   ├── patterns/analysis/      # Analysis patterns
│   │   ├── code_quality.py
│   │   ├── standards_check.py
│   │   ├── debug_assist.py
│   │   ├── spec_consistency.py
│   │   └── multi_repo_scan.py
│   └── version.json            # Agent identity
├── examples/                    # Example workflows
│   ├── code_quality_analysis/
│   ├── standards_checking/
│   ├── debugging_assistance/
│   └── spec_consistency/
├── tests/                       # Contract tests
│   ├── test_advisor_contract.py    # Inherited tests
│   └── test_developer_contract.py  # Developer-specific tests
├── scripts/
│   └── validate_examples.sh     # Example validation
├── docs/                        # Pattern guides
├── AGENTS.md                    # Agent configuration
├── README.md                    # Main documentation
└── CONTRIBUTING.md              # This file
```

---

## Adding New Patterns

### 1. Create Pattern File

Add your pattern to `.aget/patterns/analysis/`:

```python
#!/usr/bin/env python3
"""Your Pattern Name

Description of what this pattern does.

Part of template-developer-aget v2.7.0.
"""

def analyze(input_data: dict) -> dict:
    """Analyze using your pattern.

    Args:
        input_data: Analysis parameters
            - param1: description
            - param2: description

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - [pattern-specific fields]
    """
    # Implementation here
    return {
        "status": "success",
        # ... pattern-specific results
    }

if __name__ == "__main__":
    # Example usage
    result = analyze({
        "param1": "value1"
    })
    print(result)
```

### 2. Add Contract Tests

Add tests to `tests/test_developer_contract.py`:

```python
def test_your_pattern_interface():
    """Verify your pattern implements common interface."""
    from patterns.analysis.your_pattern import analyze

    result = analyze({"param1": "test"})

    assert "status" in result
    assert result["status"] in ["success", "error"]
    # ... additional assertions
```

### 3. Create Example

Add example workflow to `examples/your_pattern/`:

```
examples/your_pattern/
├── sample_input.py         # Sample code/data
├── run_analysis.py         # Pattern usage script
└── README.md               # Usage guide
```

### 4. Update Validation Script

Add your example to `scripts/validate_examples.sh`:

```bash
# Validate your_pattern example
run_example "your_pattern" "run_analysis.py"
```

### 5. Document the Pattern

Create guide in `docs/YOUR_PATTERN_GUIDE.md`:

```markdown
# Your Pattern Guide

## Overview

Description of pattern capabilities.

## Usage

Example code showing how to use the pattern.

## Parameters

- param1: description
- param2: description

## Output Format

Description of return value structure.

## Examples

Concrete usage examples.
```

---

## Testing Guidelines

### Run All Tests

```bash
# Run full test suite
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_developer_contract.py -v

# Run with coverage
python3 -m pytest tests/ --cov=.aget/patterns --cov-report=term-missing
```

### Test Requirements

- **All tests must pass** before submitting PR
- **Contract tests** validate pattern interfaces
- **Example validation** ensures examples are runnable

### Writing Tests

**Contract Test Pattern**:
```python
def test_pattern_name_interface():
    """Verify pattern implements common interface."""
    from patterns.analysis.pattern_name import analyze

    # Test basic interface
    result = analyze(minimal_valid_input)
    assert "status" in result

    # Test error handling
    result = analyze(invalid_input)
    assert result["status"] == "error"
```

---

## Code Style

### Python Style

- **PEP-8 compliance** for all code
- **Max line length**: 100 characters (relaxed from 79 for readability)
- **Docstrings**: Google style for all public functions
- **Type hints**: Use for function signatures where helpful

### Pattern Style

- **Common interface**: All patterns must implement `analyze(input_data: dict) -> dict`
- **Error handling**: Return `{"status": "error", "message": "..."}` for errors
- **No side effects**: Patterns should not modify files or execute commands
- **Deterministic**: Same input → same output (no random behavior)

### Example Code Style

```python
def analyze(input_data: dict) -> dict:
    """Pattern description.

    Args:
        input_data: Analysis parameters
            - required_param: description
            - optional_param: description (optional)

    Returns:
        dict: Analysis results
            - status: "success" | "error"
            - [other fields]: descriptions
    """
    # Extract parameters
    required = input_data.get("required_param")
    optional = input_data.get("optional_param", "default")

    # Validate inputs
    if not required:
        return {
            "status": "error",
            "message": "required_param is required"
        }

    # Perform analysis
    result = perform_analysis(required, optional)

    # Return results
    return {
        "status": "success",
        "result": result
    }
```

---

## Documentation Style

### README Files

- **Clear headings** with descriptive titles
- **Code examples** with actual runnable code
- **Expected output** when helpful
- **Learning points** explaining why, not just how

### Pattern Guides

Structure:
1. Overview (what the pattern does)
2. Usage (code example)
3. Parameters (all inputs explained)
4. Output Format (all fields explained)
5. Examples (multiple scenarios)
6. Troubleshooting (common issues)

---

## Pull Request Process

### Before Submitting

1. **Run tests**: `python3 -m pytest tests/ -v`
2. **Validate examples**: `./scripts/validate_examples.sh`
3. **Check code style**: Verify PEP-8 compliance
4. **Update documentation**: Add/update guides as needed

### PR Description Template

```markdown
## Description

Brief description of changes.

## Type of Change

- [ ] New pattern
- [ ] Bug fix
- [ ] Documentation update
- [ ] Example addition
- [ ] Test improvement

## Checklist

- [ ] All tests passing (21/21)
- [ ] Examples validated (4/4)
- [ ] Documentation updated
- [ ] Code follows PEP-8 style
- [ ] Patterns follow common interface
- [ ] No side effects (advisory-only)

## Testing

Describe how you tested the changes.
```

### Review Process

1. **Automated checks**: Tests must pass
2. **Code review**: Maintainer review for style and correctness
3. **Documentation review**: Guides are clear and helpful
4. **Example validation**: Examples are runnable and educational

---

## Pattern Design Principles

### Advisory-Only

**Patterns must not**:
- Modify files
- Execute commands with side effects
- Make network calls (except read-only fetches)
- Write to databases

**Patterns should**:
- Analyze inputs
- Return structured results
- Provide recommendations
- Be deterministic

### Minimal Configuration

**Prefer**:
- Auto-detection over configuration
- Sensible defaults over required parameters
- Built-in knowledge over external dependencies

**Example**: `standards_check.py` has built-in PEP-8 knowledge, auto-detects language, and falls back to sensible defaults.

### Composable

Patterns should:
- Work independently (not depend on other patterns)
- Use common interface (`analyze()`)
- Return structured dictionaries
- Be usable in larger workflows

---

## Getting Help

- **Questions**: Open an issue with "Question:" prefix
- **Bugs**: Open an issue with reproduction steps
- **Feature Requests**: Open an issue with "Enhancement:" prefix
- **Framework Docs**: https://github.com/aget-framework

---

## Release Process

(Maintainers only)

1. **Version bump**: Update `.aget/version.json`
2. **Changelog**: Update `README.md` version history
3. **Tag release**: `git tag v2.X.X`
4. **Push tag**: `git push origin v2.X.X`
5. **GitHub release**: Create release with notes

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Template Developer AGET! 🎉