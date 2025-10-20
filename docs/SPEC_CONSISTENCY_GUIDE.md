# Spec-to-Code Consistency Guide

**Template**: template-developer-aget v2.7.0
**Pattern**: `.aget/patterns/analysis/spec_consistency.py`
**Purpose**: Detect gaps and drifts between specification and implementation

---

## Overview

Spec-to-code consistency checking compares formal specifications against actual code to identify:
- **Coverage**: What percentage of spec is implemented
- **Gaps**: Missing capabilities (not implemented yet)
- **Drift**: Implementation diverges from spec (scope expansion/reduction)
- **Over-Implementation**: Features in code not mentioned in spec

**Collaboration**: Works with `template-spec-engineer-aget` specs (EARS format, YAML)

**Output**: Coverage metrics + prioritized recommendations

---

## Usage

### Basic Consistency Check
```bash
# Check spec against implementation
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/APP_SPEC_v1.0.yaml \
  --repo ~/github/my-app

# Specify spec format
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/requirements.md \
  --spec-format markdown \
  --repo ~/github/my-app

# Filter by capability priority
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/APP_SPEC_v1.0.yaml \
  --repo ~/github/my-app \
  --priority high
```

### Interactive Use
```
User: "Compare specs/APP_SPEC_v1.0.yaml against ~/github/my-app"

Advisor:
1. Parses specification (32 capabilities)
2. Maps capabilities to code
3. Detects coverage: 85% (27/32 implemented)
4. Identifies gaps: 5 missing capabilities
5. Detects drift: 1 scope expansion (OAuth added)
6. Reports over-implementation: 2 features not in spec
7. Recommends next steps (prioritized)
```

---

## Output Format

### Report Structure
```
Spec-to-Code Consistency Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Specification: specs/APP_SPEC_v1.0.yaml (32 capabilities)
Implementation: ~/github/my-app

Coverage: 85% (27/32 implemented)

Missing Capabilities:
❌ CAP-015: Password reset functionality (high priority)
❌ CAP-022: Email notifications (partial - 60% done)
❌ CAP-028: Audit logging (medium priority)

Implementation Drift:
⚠️  CAP-010: Login allows OAuth (spec: username/password only)
   Question: Is OAuth intended? Update spec or remove feature?

Over-Implementation:
⚠️  Social media sharing (sharing.py)
   Not mentioned in spec - document or remove

Recommendations:
1. Implement CAP-015 (password reset) - high priority
2. Complete CAP-022 (email notifications) - 60% done
3. Clarify CAP-010 with spec engineer (OAuth scope)
```

### JSON Output
```json
{
  "status": "success",
  "spec_version": "v1.0.0",
  "coverage": {
    "total_capabilities": 32,
    "implemented": 27,
    "partial": 1,
    "missing": 4,
    "percentage": 84.4
  },
  "missing_capabilities": [
    {
      "id": "CAP-015",
      "name": "Password reset functionality",
      "priority": "high",
      "rationale": "Required for user account recovery"
    }
  ],
  "implementation_drift": [
    {
      "capability_id": "CAP-010",
      "drift_type": "scope_expansion",
      "spec_says": "Username/password authentication",
      "implementation_has": "Username/password + OAuth",
      "question": "Is OAuth intended? Update spec or remove?"
    }
  ],
  "over_implementation": [...],
  "recommendations": [...]
}
```

---

## Specification Formats

### YAML Format (Preferred)

**Structure**:
```yaml
spec:
  id: SPEC-MY-APP
  version: v1.0.0

capabilities:
  CAP-001:
    statement: "The SYSTEM shall provide user login with username and password"
    type: ubiquitous
    priority: high

  CAP-002:
    statement: "WHEN user clicks reset password, the SYSTEM shall send reset link"
    type: event-driven
    priority: high

  CAP-003:
    statement: "IF user is admin, the SYSTEM shall display admin panel"
    type: conditional
    priority: medium
```

**EARS Patterns** (5 types):
- **Ubiquitous**: `The SYSTEM shall...`
- **Event-driven**: `WHEN <trigger>, the SYSTEM shall...`
- **State-driven**: `WHILE <state>, the SYSTEM shall...`
- **Optional**: `WHERE <feature enabled>, the SYSTEM shall...`
- **Conditional**: `IF <condition>, the SYSTEM shall...`

**Collaboration**: Created by `template-spec-engineer-aget`

---

### Markdown Format

**Structure**:
```markdown
# App Requirements v1.0

## Authentication (High Priority)
- [ ] CAP-001: User login with username/password
- [ ] CAP-002: Password reset functionality
- [x] CAP-003: Session token generation

## API Endpoints (Medium Priority)
- [x] CAP-004: GET /users/:id (retrieve user profile)
- [ ] CAP-005: POST /users (create user)
```

**Parsing**: Extracts capabilities from checkboxes and headings

---

### Plain Text (Basic)

**Structure**:
```
Requirements v1.0

1. [HIGH] User login (username/password)
2. [HIGH] Password reset via email
3. [MED] User profile API endpoint
4. [LOW] Social media integration
```

---

## Consistency Analysis

### Coverage Calculation
```
Coverage % = (Implemented / Total) × 100

Where:
  Implemented = Count of capabilities found in code
  Total = Total capabilities in spec
```

**Example**:
- Total: 32 capabilities
- Implemented: 27 capabilities
- Coverage: (27 / 32) × 100 = **84.4%**

**Interpretation**:
- **90-100%**: Excellent (ready for release)
- **70-89%**: Good (minor gaps)
- **50-69%**: Fair (significant gaps)
- **<50%**: Poor (early development)

---

### Gap Detection

**Types of Gaps**:

#### 1. Missing Capability
```yaml
# Spec says:
CAP-015:
  statement: "The SYSTEM shall provide password reset"

# Code: No implementation found

# Classification: MISSING
# Priority: High (required feature)
# Recommendation: Implement before release
```

#### 2. Partial Implementation
```yaml
# Spec says:
CAP-022:
  statement: "The SYSTEM shall send email notifications on important events"

# Code: Email sending exists, but only for registration (not all events)

# Classification: PARTIAL (60% complete)
# Recommendation: Complete remaining notification types
```

---

### Drift Detection

**Types of Drift**:

#### 1. Scope Expansion (Most Common)
```yaml
# Spec says:
CAP-010:
  statement: "The SYSTEM shall provide user login with username and password"

# Code implements:
- Username/password login ✅
- OAuth login ⚠️  (not in spec)
- SSO login ⚠️  (not in spec)

# Classification: SCOPE EXPANSION
# Question: Is OAuth/SSO intended feature or scope creep?
# Action: Clarify with spec engineer → Update spec OR remove code
```

#### 2. Scope Reduction (Less Common)
```yaml
# Spec says:
CAP-030:
  statement: "The SYSTEM shall export reports to PDF, Excel, and CSV"

# Code implements:
- PDF export ✅
- CSV export ✅
- Excel export ❌ (missing)

# Classification: SCOPE REDUCTION (partial)
# Recommendation: Complete Excel export per spec
```

---

### Over-Implementation Detection

**Definition**: Features in code **not mentioned** in spec

**Example**:
```python
# Code: src/sharing.py
def share_to_facebook(post_id):
    """Social media sharing - not in spec"""
    pass

# Spec: No CAP-XXX mentions social media

# Classification: OVER-IMPLEMENTATION
# Questions:
  - Is this required but undocumented? (Add to spec)
  - Is this experimental? (Document or remove)
  - Is this scope creep? (Remove if out of scope)
```

**Action**:
1. **Consult stakeholders**: Is feature needed?
2. **If yes**: Add to spec (create CAP-XXX)
3. **If no**: Remove code to prevent maintenance burden

---

## Capability Mapping

### How Mapping Works

**Step 1**: Extract keywords from capability statement
```yaml
CAP-015:
  statement: "The SYSTEM shall provide password reset functionality"

# Keywords: password, reset, functionality
```

**Step 2**: Search codebase for keywords
```bash
# Search for implementation
grep -ri "password.*reset" src/
grep -ri "reset.*password" src/

# Potential matches:
# src/auth.py:42: def reset_password(user_id):
# src/api/auth.py:108: @app.route('/reset-password')
```

**Step 3**: Calculate confidence
```
Confidence = (Keyword matches + Code proximity + Type hints) / 3

High confidence (>0.7): Strong evidence of implementation
Medium confidence (0.4-0.7): Possible implementation, needs review
Low confidence (<0.4): Likely not implemented
```

**Step 4**: Classify status
- **Implemented**: High confidence match found
- **Partial**: Some keywords match, incomplete implementation
- **Missing**: Low confidence, no clear implementation

---

## Workflow Examples

### Example 1: Pre-Release Gap Analysis

**Scenario**: Check if app is ready for v1.0 release

```bash
# 1. Run consistency check
cd ~/github/my-app
python3 ~/github/template-developer-aget/.aget/patterns/analysis/spec_consistency.py \
  --spec specs/v1.0_SPEC.yaml \
  --repo . \
  --priority high

# 2. Review results
# Coverage: 85% (27/32)
# Missing (high priority): CAP-015 (password reset), CAP-028 (audit logging)

# 3. Decision
# Option A: Implement missing high-priority features
# Option B: Defer to v1.1, release with 85% coverage

# 4. Document decision
# If deferring: Update spec priority CAP-028 → low, target v1.1
```

---

### Example 2: Spec Drift Clarification

**Scenario**: Found OAuth in code, but spec only mentions username/password

```bash
# 1. Detect drift
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/v1.0_SPEC.yaml \
  --repo .

# Output:
# Drift: CAP-010 - Implementation has OAuth (not in spec)

# 2. Investigate history
git log --all --grep="OAuth" --oneline
# Found: "Add OAuth login (requested by stakeholder)"

# 3. Consult spec engineer
User: "CAP-010 drift - OAuth was stakeholder request. Update spec?"

Spec Engineer: "Yes, OAuth is approved. I'll add CAP-010a."

# 4. Spec updated
# CAP-010a: "The SYSTEM shall provide OAuth login (Google, GitHub)"

# 5. Re-run check
# Coverage: 88% ✅ (drift resolved)
```

---

### Example 3: Over-Implementation Review

**Scenario**: Social media sharing found in code, not in spec

```bash
# 1. Detect over-implementation
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/v1.0_SPEC.yaml \
  --repo .

# Output:
# Over-implementation: sharing.py (social media sharing)

# 2. Consult stakeholders
User: "Social sharing not in spec. Remove?"

Stakeholder: "Not needed for v1.0. Remove to reduce scope."

# 3. Remove feature
git rm src/sharing.py
git commit -m "Remove social sharing (out of scope for v1.0)"

# 4. Re-run check
# Over-implementation: 0 ✅
```

---

## Collaboration with Spec Engineer

### Workflow: Spec Creation → Implementation → Consistency Check

**Phase 1: Spec Creation** (by `template-spec-engineer-aget`)
```yaml
# specs/v1.0_SPEC.yaml
capabilities:
  CAP-001:
    statement: "The SYSTEM shall provide user login"
    priority: high
  CAP-002:
    statement: "The SYSTEM shall provide password reset"
    priority: high
  # ... 30 more capabilities
```

**Phase 2: Implementation** (by development team)
```python
# src/auth.py
def login(username, password):  # CAP-001 ✅
    pass

# CAP-002 not implemented yet ❌
```

**Phase 3: Consistency Check** (by `template-developer-aget`)
```bash
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/v1.0_SPEC.yaml \
  --repo .

# Output:
# Coverage: 50% (16/32)
# Missing: CAP-002 (password reset), CAP-005, CAP-008, ...
```

**Phase 4: Iterative Refinement**
- Developer implements missing capabilities
- Spec engineer updates spec based on drift/over-implementation
- Code analysis advisor monitors consistency

---

## Advanced Features

### Partial Implementation Tracking
```yaml
# Spec
CAP-022:
  statement: "Send email notifications on: registration, password reset, login"

# Code
def send_registration_email():  # ✅ Implemented
    pass

# Missing: password_reset_email, login_email

# Output:
# CAP-022: PARTIAL (33% - registration only)
# Recommendation: Add password_reset_email, login_email
```

---

### Confidence Scoring
```
High Confidence (>70%):
  - Multiple keyword matches
  - Function/class names match capability
  - Tests mention capability ID

Medium Confidence (40-70%):
  - Some keyword matches
  - Similar functionality, different naming

Low Confidence (<40%):
  - Few keyword matches
  - Likely not implemented
```

---

## Integration Workflows

### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if spec coverage decreased
python3 ~/github/template-developer-aget/.aget/patterns/analysis/spec_consistency.py \
  --spec specs/v1.0_SPEC.yaml \
  --repo . \
  --format json > /tmp/coverage_new.json

old_coverage=$(jq '.coverage.percentage' .aget/analysis/spec_coverage_baseline.json)
new_coverage=$(jq '.coverage.percentage' /tmp/coverage_new.json)

if (( $(echo "$new_coverage < $old_coverage" | bc -l) )); then
    echo "⚠️  Spec coverage decreased: $old_coverage% → $new_coverage%"
    echo "Did you remove implemented features?"
    exit 1
fi
```

---

### CI/CD Pipeline
```yaml
# .github/workflows/spec_consistency.yml
- name: Spec Consistency Check
  run: |
    python3 ~/github/template-developer-aget/.aget/patterns/analysis/spec_consistency.py \
      --spec specs/v1.0_SPEC.yaml \
      --repo . \
      --format json > spec_consistency_report.json

    coverage=$(jq '.coverage.percentage' spec_consistency_report.json)
    if (( $(echo "$coverage < 80.0" | bc -l) )); then
        echo "Coverage $coverage% below 80% threshold"
        exit 1
    fi
```

---

## Troubleshooting

### "No capabilities found in spec"
**Cause**: Spec format not recognized

**Fix**: Specify format explicitly
```bash
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec requirements.md \
  --spec-format markdown \
  --repo .
```

---

### "Coverage: 0% (but features implemented)"
**Cause**: Keyword mismatch between spec and code

**Fix**: Improve spec keywords or add mapping hints
```yaml
# Add keywords field
CAP-015:
  statement: "The SYSTEM shall provide password reset"
  keywords: ["reset_password", "forgot_password", "password_recovery"]
```

---

### "Too many false positives (drift)"
**Cause**: Overly strict mapping

**Fix**: Adjust confidence threshold
```bash
python3 .aget/patterns/analysis/spec_consistency.py \
  --spec specs/v1.0_SPEC.yaml \
  --repo . \
  --confidence-threshold 0.6  # Lower = fewer false positives
```

---

## Related Guides

- **Code Quality**: `docs/CODE_QUALITY_GUIDE.md`
- **Multi-Repository**: `docs/MULTI_REPO_CONFIGURATION.md`
- **Pattern Library**: `.aget/patterns/analysis/spec_consistency.py`
- **Spec Engineer Template**: `aget-framework/template-spec-engineer-aget`

---

*Generated for template-developer-aget v2.7.0*
