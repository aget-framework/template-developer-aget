# Code Quality Analysis Guide

**Template**: template-developer-aget v2.7.0
**Pattern**: `.aget/patterns/analysis/code_quality.py`
**Purpose**: Comprehensive code quality assessment with actionable metrics

---

## Overview

Code quality analysis assesses your codebase across multiple dimensions:
- **Complexity**: Cyclomatic complexity, cognitive complexity
- **Maintainability**: Maintainability index (0-100 scale)
- **Technical Debt**: TODO/FIXME comments, age tracking
- **Code Smells**: Long methods, duplicate code, nested conditionals

**Output**: Quantitative rating (0-10) + prioritized recommendations

---

## Usage

### Basic Analysis
```bash
# Analyze single repository
python3 .aget/patterns/analysis/code_quality.py ~/github/my-project

# Specify language (auto-detected by default)
python3 .aget/patterns/analysis/code_quality.py ~/github/my-project --language python

# Filter metrics
python3 .aget/patterns/analysis/code_quality.py ~/github/my-project \
  --metrics complexity,maintainability
```

### Interactive Use
Wake up the advisor and request analysis:
```
User: "Assess code quality for ~/github/my-app"

Advisor: [Runs code_quality.py, presents formatted report]
```

---

## Output Format

### Report Structure
```
Code Quality Report: ~/github/my-app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Quality: 7/10

Metrics:
- Complexity: Medium (avg cyclomatic: 8)
- Maintainability: Good (maintainability index: 72)
- Test Coverage: Low (detected: 45%)
- Documentation: Medium (60% of public functions)

Issues:
🔴 High Complexity: auth.py::login() (cyclomatic: 18)
🟡 Technical Debt: 5 TODO comments unresolved
🟡 Code Smell: Long method process_data() (150 lines)

Recommendations:
1. Refactor auth.py::login() - extract validation logic
2. Address TODOs in utils.py (2 years old)
3. Split process_data() into smaller, focused methods
```

### JSON Output
```json
{
  "status": "success",
  "overall_quality": 7.0,
  "metrics": {
    "complexity": {
      "avg_cyclomatic": 8.2,
      "max_cyclomatic": 18,
      "high_complexity_functions": [
        {"file": "auth.py", "function": "login", "complexity": 18}
      ]
    },
    "maintainability": {
      "index": 72,
      "status": "good"
    },
    "technical_debt": {
      "todo_count": 5,
      "fixme_count": 2,
      "oldest_todo": "2023-01-15",
      "items": [...]
    },
    "code_smells": [...]
  },
  "recommendations": [...]
}
```

---

## Metrics Explained

### 1. Complexity (Cyclomatic)

**What it measures**: Number of independent paths through code

**Thresholds**:
- **1-10**: Simple, easy to test (✅ Good)
- **11-20**: Moderate, needs attention (⚠️ Warning)
- **21+**: High, difficult to maintain (🔴 Critical)

**Example**:
```python
# Complexity: 1 (simple)
def add(a, b):
    return a + b

# Complexity: 6 (moderate - 5 if statements + 1 base)
def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        return a + b + c + d + e
    return 0
```

**Fix Strategy**: Extract nested logic into separate functions

---

### 2. Maintainability Index

**What it measures**: How easy code is to maintain (0-100 scale)

**Formula**:
```
MI = max(0, 171 - 5.2*ln(V) - 0.23*G - 16.2*ln(LOC))

Where:
  V = Halstead Volume (complexity of operators/operands)
  G = Cyclomatic Complexity
  LOC = Lines of Code
```

**Ratings**:
- **85-100**: Excellent (green zone)
- **65-84**: Good (acceptable)
- **50-64**: Fair (needs improvement)
- **0-49**: Poor (refactor urgently)

**Improvement Tips**:
- Reduce function length (lower LOC)
- Simplify logic (lower G)
- Use clear variable names (lower V)

---

### 3. Technical Debt

**What it measures**: Unresolved TODO/FIXME/HACK comments

**Detection Patterns**:
```python
# TODO: Refactor this function
# FIXME: Handle edge case
# HACK: Temporary workaround
# XXX: This is broken
```

**Metrics**:
- Total count (all types)
- Oldest item (age in days)
- Breakdown by type

**Prioritization**:
- 🔴 **>2 years old**: Delete or implement immediately
- 🟡 **>6 months**: Review for relevance
- ⚪ **<6 months**: Monitor

---

### 4. Code Smells

**Common Smells Detected**:

#### Long Method (>50 lines)
```python
# Bad: 150-line method
def process_data(data):
    # ... 150 lines of logic ...
    pass

# Good: Extracted smaller methods
def process_data(data):
    validated = validate_data(data)
    transformed = transform_data(validated)
    return save_data(transformed)
```

#### Nested Conditionals (depth >3)
```python
# Bad: Deeply nested
if a:
    if b:
        if c:
            if d:
                return True

# Good: Early returns
if not a:
    return False
if not b:
    return False
if not c:
    return False
return d
```

#### Duplicate Code (>80% similarity)
```
Detected across files: utils.py, helpers.py
Recommendation: Extract to shared library
```

---

## Quality Rating Calculation

**Weighted Formula**:
```
Overall Quality (0-10) =
  Complexity Score (30%) +
  Maintainability Score (40%) +
  Debt Score (20%) +
  Smells Score (10%)
```

**Component Calculations**:
```python
# Complexity: Inverse (high complexity = low score)
complexity_score = max(0, 10 - avg_cyclomatic / 2)

# Maintainability: Direct mapping
maintainability_score = maintainability_index / 10

# Debt: Inverse (high debt = low score)
debt_score = max(0, 10 - todo_count)

# Smells: Inverse (more smells = low score)
smells_score = max(0, 10 - len(code_smells))
```

**Example**:
- Avg complexity: 8 → Score: 10 - 8/2 = 6
- Maintainability: 72 → Score: 7.2
- TODOs: 3 → Score: 7
- Smells: 2 → Score: 8

**Overall**: 6×0.3 + 7.2×0.4 + 7×0.2 + 8×0.1 = **6.9/10**

---

## Language-Specific Tooling

### Python
**Tools**: `radon` (complexity, maintainability)

**Installation**:
```bash
pip install radon
```

**Direct Usage**:
```bash
# Complexity
radon cc src/ -a

# Maintainability
radon mi src/ -s
```

### JavaScript/TypeScript
**Tools**: `eslint` (complexity plugin)

**Configuration**:
```json
{
  "rules": {
    "complexity": ["warn", 10]
  }
}
```

### Go
**Tools**: `gocyclo` (complexity)

**Installation**:
```bash
go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
```

---

## Integration with Workflows

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

python3 .aget/patterns/analysis/code_quality.py . --threshold 7.0

if [ $? -ne 0 ]; then
    echo "❌ Code quality below threshold (7.0)"
    exit 1
fi
```

### CI/CD Pipeline
```yaml
# .github/workflows/quality.yml
- name: Code Quality Check
  run: |
    python3 .aget/patterns/analysis/code_quality.py . \
      --format json > quality_report.json

    score=$(jq '.overall_quality' quality_report.json)
    if (( $(echo "$score < 7.0" | bc -l) )); then
        echo "Quality score $score below threshold"
        exit 1
    fi
```

### Advisory Session
```
User: "Wind down"

Advisor:
- Runs quality analysis on current work
- Compares before/after scores
- Reports: "Quality improved from 6.5 to 7.2"
- Commits quality_report.json to .aget/analysis/
```

---

## Continuous Improvement

### Track Quality Over Time
```bash
# Store historical reports
mkdir -p .aget/analysis/quality_history/

python3 .aget/patterns/analysis/code_quality.py . \
  --format json > .aget/analysis/quality_history/$(date +%Y-%m-%d).json
```

### Trend Analysis
```bash
# Compare current vs last month
current=$(jq '.overall_quality' .aget/analysis/quality_history/$(date +%Y-%m-%d).json)
past=$(jq '.overall_quality' .aget/analysis/quality_history/$(date -d '1 month ago' +%Y-%m-%d).json)

echo "Quality trend: $past → $current"
```

---

## Example Workflow

**Scenario**: Assess quality before release

```bash
# 1. Run analysis
cd ~/github/my-app
python3 ~/github/template-developer-aget/.aget/patterns/analysis/code_quality.py .

# 2. Review report
# Overall Quality: 6.5/10
# Issues: 3 high-complexity functions, 8 TODOs

# 3. Prioritize fixes
# - auth.py::login() (complexity: 18) → Refactor first
# - utils.py TODOs (2 years old) → Delete or implement

# 4. Refactor
# [Fix high-complexity functions]

# 5. Re-run analysis
python3 ~/github/template-developer-aget/.aget/patterns/analysis/code_quality.py .

# 6. Verify improvement
# Overall Quality: 7.8/10 ✅
```

---

## Troubleshooting

### "Language not detected"
**Cause**: No recognizable source files in repository

**Fix**:
```bash
# Specify language explicitly
python3 .aget/patterns/analysis/code_quality.py . --language python
```

### "radon not found"
**Cause**: Python dependencies not installed

**Fix**:
```bash
pip install radon pycodestyle
```

### High complexity on generated code
**Cause**: Auto-generated files included in analysis

**Fix**: Exclude generated files
```bash
python3 .aget/patterns/analysis/code_quality.py . \
  --exclude "migrations/*,generated/*"
```

---

## Related Guides

- **Standards Checking**: `docs/STANDARDS_CHECKING_GUIDE.md`
- **Debugging Assistance**: `docs/DEBUG_ASSISTANCE_GUIDE.md`
- **Pattern Library**: `.aget/patterns/analysis/code_quality.py`

---

*Generated for template-developer-aget v2.7.0*
