# Coding Standards Checking Example

Demonstrates the `standards_check.py` pattern for checking code against coding standards.

## Files

- `sample_code.py` - Sample Python code with PEP-8 violations
- `run_check.py` - Script that runs standards compliance check

## Usage

```bash
cd examples/standards_checking
python3 run_check.py
```

## Expected Output

The check identifies PEP-8 violations:

1. **E501** (Line too long): Lines exceeding 79 characters
2. **E722** (Bare except clause): `except:` without exception type
3. **W293** (Blank line contains whitespace): Whitespace on empty lines

## Standards Precedence

The pattern applies standards in this order:

1. **Repo-specific** (`.coding-standards.md` in repository root)
2. **Agent-level** (custom standards in `.aget/standards/`)
3. **Built-in** (PEP-8 for Python, ESLint for JavaScript, gofmt for Go)

## Customization

Create `.coding-standards.md` in your repository:

```markdown
# Coding Standards

Max line length: 120

Rules:
- Use descriptive variable names (>3 characters)
- Document all public functions
- Handle exceptions explicitly (no bare except)
```

The pattern will detect and parse this file automatically.

## Learning Points

- Built-in standards knowledge for multiple languages
- Precedence order allows repo-specific overrides
- Compliance rating (0-10) based on violations per 1000 lines
- Recommendations prioritize high-impact fixes
