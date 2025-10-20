# Coding Standards Checking Guide

**Template**: template-developer-aget v2.7.0
**Pattern**: `.aget/patterns/analysis/standards_check.py`
**Purpose**: Verify code compliance against coding standards (built-in + custom)

---

## Overview

Standards checking validates your code against established guidelines:
- **Built-in Standards**: PEP-8 (Python), ESLint (JavaScript), gofmt (Go)
- **Custom Standards**: Agent-level or repository-specific rules
- **Precedence Order**: Repo-specific → Agent-level → Built-in

**Output**: Compliance rating (0-10) + violation details + fix examples

---

## Standards Precedence

**Priority Order** (most specific to least):

### 1. Repository-Specific Standards (Highest Priority)
**Location**: `{repo}/.coding-standards.md`

**Use Case**: Project-specific conventions (team style, architecture rules)

**Example**:
```markdown
<!-- ~/github/my-project/.coding-standards.md -->
# My Project Coding Standards

## Python
- Max line length: 100 (not 79 - we use wider monitors)
- Docstrings: Google style (not NumPy)
- Imports: absolute only (no relative imports)

## Naming
- API endpoints: snake_case (get_user, not getUser)
- Database tables: plural (users, not user)
```

---

### 2. Agent-Level Custom Standards
**Location**: `.aget/standards/{language}.md`

**Use Case**: Personal/organizational standards applied to all your repos

**Example**:
```markdown
<!-- .aget/standards/python.md -->
# Python Standards (Agent-Level)

## Error Handling
- Never use bare `except:` (use `except Exception:`)
- Always log exceptions with context

## Testing
- Every public function must have docstring
- Test coverage minimum: 80%
```

---

### 3. Built-In Standards (Fallback)
**Languages Supported**:
- **Python**: PEP-8, PEP-257 (docstrings)
- **JavaScript/TypeScript**: ESLint recommended config
- **Go**: gofmt formatting + Effective Go patterns

**Used When**: No custom standards configured

---

## Usage

### Basic Standards Check
```bash
# Auto-detect language and standards
python3 .aget/patterns/analysis/standards_check.py ~/github/my-project

# Specify standard explicitly
python3 .aget/patterns/analysis/standards_check.py ~/github/my-project \
  --standard pep8

# Use custom standards file
python3 .aget/patterns/analysis/standards_check.py ~/github/my-project \
  --custom-standards .aget/standards/python.md
```

### Interactive Use
```
User: "Check ~/github/my-app against coding standards"

Advisor:
1. Checks for repo-specific standards (~/github/my-app/.coding-standards.md)
2. Falls back to agent-level (.aget/standards/python.md)
3. Falls back to built-in (PEP-8)
4. Analyzes code against standards
5. Reports violations with severity and fix examples
```

---

## Output Format

### Report Structure
```
Standards Compliance Report: ~/github/my-app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Standard: PEP-8 (Python)
Compliance: 6/10 (18 violations)

Violations:
🔴 E501: Line too long (>79 chars) - 8 files
🟡 E722: Bare except clause - 4 instances
🟡 F841: Unused variable - 6 instances

Fix Examples:
E501 (line too long):
  ❌ result = some_very_long_function_name(argument1, argument2, argument3, argument4)
  ✅ result = some_very_long_function_name(
         argument1, argument2,
         argument3, argument4
      )

E722 (bare except):
  ❌ except:
  ✅ except Exception as e:
      logger.error(f"Error: {e}")

Recommendations:
1. Fix 8 E501 violations (line too long) - high priority
2. Replace 4 bare except clauses - high priority
3. Remove 6 unused variables - medium priority
```

### JSON Output
```json
{
  "status": "success",
  "compliance_rating": 6.5,
  "standards_applied": "PEP-8 (built-in)",
  "violations": [
    {
      "code": "E501",
      "severity": "error",
      "file": "app.py",
      "line": 42,
      "message": "Line too long (95 > 79 characters)",
      "fix_example": "Break line at 79 chars:\n  result = func(\n      arg1, arg2\n  )"
    }
  ],
  "violation_summary": {
    "error": 5,
    "warning": 12,
    "total": 17
  },
  "recommendations": [...]
}
```

---

## Built-In Standards Reference

### Python (PEP-8)

**Common Violations**:

#### E501: Line Too Long
```python
# ❌ Violation (95 chars)
def function_with_long_name(argument_one, argument_two, argument_three, argument_four):
    pass

# ✅ Fixed (multi-line)
def function_with_long_name(
    argument_one, argument_two,
    argument_three, argument_four
):
    pass
```

#### E722: Bare Except
```python
# ❌ Violation
try:
    risky_operation()
except:  # Catches everything, including KeyboardInterrupt
    pass

# ✅ Fixed
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
```

#### F841: Unused Variable
```python
# ❌ Violation
def calculate():
    x = 5
    y = 10  # y is never used
    return x

# ✅ Fixed
def calculate():
    x = 5
    return x
```

#### E701: Multiple Statements on One Line
```python
# ❌ Violation
def compact(): x = 1; return x

# ✅ Fixed
def compact():
    x = 1
    return x
```

#### W293: Blank Line with Whitespace
```python
# ❌ Violation
def function():
    x = 1
    ␣␣␣  # Blank line with spaces
    return x

# ✅ Fixed
def function():
    x = 1

    return x
```

**PEP-257 (Docstrings)**:
```python
# ✅ Good docstring
def add(a: int, b: int) -> int:
    """Add two numbers and return the result.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b
```

---

### JavaScript/TypeScript (ESLint)

**Common Violations**:

#### no-unused-vars
```javascript
// ❌ Violation
function calculate() {
    const x = 5;
    const y = 10;  // y is never used
    return x;
}

// ✅ Fixed
function calculate() {
    const x = 5;
    return x;
}
```

#### no-console
```javascript
// ❌ Violation (production code)
console.log('Debug info');

// ✅ Fixed
logger.info('Debug info');
```

#### eqeqeq (Require ===)
```javascript
// ❌ Violation
if (x == y) {  // Type coercion

// ✅ Fixed
if (x === y) {  // Strict equality
```

---

### Go (gofmt + Effective Go)

**Common Violations**:

#### Formatting (gofmt)
```go
// ❌ Violation (improper formatting)
func Add(a,b int)int{
return a+b
}

// ✅ Fixed (gofmt applied)
func Add(a, b int) int {
    return a + b
}
```

#### Error Handling
```go
// ❌ Violation (ignored error)
result, _ := doSomething()

// ✅ Fixed
result, err := doSomething()
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

---

## Custom Standards

### Agent-Level Standards

**Location**: `.aget/standards/{language}.md`

**Example**: Create Python standards
```bash
mkdir -p ~/github/template-developer-aget/.aget/standards

cat > ~/github/template-developer-aget/.aget/standards/python.md <<'EOF'
# Custom Python Standards (Agent-Level)

## Organization Rules
- Max line length: 100 (wider than PEP-8's 79)
- Imports: Group by stdlib, third-party, local

## Error Handling
- Never use bare except (use except Exception)
- Always include error context in logs

## Documentation
- Every public function: docstring required
- Every module: module-level docstring

## Testing
- Test file naming: test_{module}.py
- Test function naming: test_{function}_{scenario}
EOF
```

**Application**: These standards apply to **all repos you analyze** (unless overridden by repo-specific standards)

---

### Repository-Specific Standards

**Location**: `{repo}/.coding-standards.md`

**Example**: Project-specific rules
```bash
cd ~/github/my-project

cat > .coding-standards.md <<'EOF'
# My Project Coding Standards

## Python Style
- Line length: 120 (we use ultrawide monitors)
- Docstrings: Google style
- Type hints: Required for all public functions

## Architecture
- No direct database access from views (use services)
- All API responses: JSON only (no XML)
- Configuration: Environment variables only (no config files)

## Naming Conventions
- API endpoints: snake_case (get_user_profile)
- Database tables: Plural (users, orders)
- Database columns: snake_case (created_at)
EOF
```

**Priority**: These **override** agent-level and built-in standards

---

## Compliance Rating Calculation

**Formula**:
```
Compliance Rating (0-10) = max(0, 10 - (violation_density / 10))

Where:
  violation_density = (total_violations / lines_checked) × 1000
```

**Example**:
- Total violations: 18
- Lines checked: 2,456
- Density: (18 / 2,456) × 1000 = 7.33
- Rating: 10 - (7.33 / 10) = **9.3/10** ✅

**Interpretation**:
- **9-10**: Excellent compliance
- **7-8**: Good compliance
- **5-6**: Needs improvement
- **0-4**: Poor compliance (urgent fixes needed)

---

## Severity Levels

### Error (🔴 High Priority)
**Violations that prevent code from working or cause bugs**:
- E501: Line too long (reduces readability significantly)
- E722: Bare except (catches KeyboardInterrupt)
- F821: Undefined name (runtime error)

**Action**: Fix immediately

---

### Warning (🟡 Medium Priority)
**Style violations that reduce maintainability**:
- F841: Unused variable (code clutter)
- W503: Line break before binary operator (style preference)

**Action**: Fix before release

---

### Info (⚪ Low Priority)
**Minor style inconsistencies**:
- W293: Blank line with whitespace
- W291: Trailing whitespace

**Action**: Fix when convenient (or auto-format)

---

## Integration Workflows

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run standards check
python3 ~/github/template-developer-aget/.aget/patterns/analysis/standards_check.py . \
  --threshold 7.0

if [ $? -ne 0 ]; then
    echo "❌ Standards compliance below threshold"
    exit 1
fi
```

### Auto-Fix with Black (Python)
```bash
# Install black formatter
pip install black

# Auto-fix PEP-8 violations
black src/

# Re-check compliance
python3 .aget/patterns/analysis/standards_check.py .
```

### CI/CD Pipeline
```yaml
# .github/workflows/standards.yml
- name: Standards Check
  run: |
    python3 ~/github/template-developer-aget/.aget/patterns/analysis/standards_check.py . \
      --format json > compliance_report.json

    rating=$(jq '.compliance_rating' compliance_report.json)
    if (( $(echo "$rating < 7.0" | bc -l) )); then
        echo "Compliance rating $rating below 7.0"
        exit 1
    fi
```

---

## Language-Specific Tooling

### Python: pycodestyle
```bash
# Install
pip install pycodestyle

# Check file
pycodestyle src/app.py

# Check directory
pycodestyle src/
```

### JavaScript: ESLint
```bash
# Install
npm install eslint --save-dev

# Initialize config
npx eslint --init

# Check files
npx eslint src/
```

### Go: gofmt + golint
```bash
# Format code (gofmt)
gofmt -w .

# Check style (golint)
go install golang.org/x/lint/golint@latest
golint ./...
```

---

## Troubleshooting

### "No standard found for {language}"
**Cause**: Language not supported by built-in standards

**Fix**: Create custom standards
```bash
cat > .aget/standards/ruby.md <<'EOF'
# Custom Ruby Standards
- Style: Follow Rubocop defaults
- Testing: RSpec required
EOF
```

---

### "Compliance rating: 0/10"
**Cause**: Excessive violations (>100 per 1000 lines)

**Fix**: Auto-format first, then check
```bash
# Python
black src/

# JavaScript
npx eslint --fix src/

# Go
gofmt -w .
```

---

### Standards conflict (repo vs agent)
**Expected**: Repo-specific standards **override** agent-level

**Verification**:
```bash
# Check which standard was applied
python3 .aget/patterns/analysis/standards_check.py . \
  --format json | jq '.standards_applied'

# Output: "Custom (repo-specific)" or "PEP-8 (built-in)"
```

---

## Example Workflow

**Scenario**: Check new project against standards

```bash
# 1. Run standards check
cd ~/github/my-new-project
python3 ~/github/template-developer-aget/.aget/patterns/analysis/standards_check.py .

# 2. Review violations
# Compliance: 5.5/10
# E501: 12 violations (line too long)
# E722: 3 violations (bare except)

# 3. Auto-fix what you can
black .  # Fixes E501, W293, etc.

# 4. Manual fixes
# Fix E722: Replace bare except with except Exception

# 5. Re-check
python3 ~/github/template-developer-aget/.aget/patterns/analysis/standards_check.py .

# 6. Verify improvement
# Compliance: 8.5/10 ✅
```

---

## Related Guides

- **Code Quality**: `docs/CODE_QUALITY_GUIDE.md`
- **Multi-Repository**: `docs/MULTI_REPO_CONFIGURATION.md`
- **Pattern Library**: `.aget/patterns/analysis/standards_check.py`

---

*Generated for template-developer-aget v2.7.0*
