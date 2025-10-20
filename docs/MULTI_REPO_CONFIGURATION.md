# Multi-Repository Configuration Guide

**Template**: template-developer-aget v2.7.0
**Pattern**: `.aget/patterns/analysis/multi_repo_scan.py`
**Purpose**: Analyze code patterns across multiple repositories

---

## Overview

Multi-repository analysis enables:
- **Pattern Recognition**: Identify shared frameworks, libraries, conventions
- **Consistency Checking**: Detect inconsistencies across related projects
- **Duplicate Detection**: Find similar code that could be extracted to shared library
- **Architecture Validation**: Verify microservices follow organization standards

**Discovery Modes**:
- **Zero-Config**: Auto-scan `~/github/` (no setup required)
- **Configured**: Explicit include/exclude lists (fine-grained control)
- **Hybrid**: Auto-scan with exclusions (balanced approach)

---

## Discovery Mechanisms

### Zero-Config Mode (Auto-Scan)

**How it works**: Automatically discovers all git repositories in `~/github/`

**No configuration needed** - just run analysis:
```bash
# Discover and analyze all repos in ~/github/
python3 .aget/patterns/analysis/multi_repo_scan.py --mode auto
```

**Auto-Scan Algorithm**:
```bash
# Discover repos
ls ~/github/ | while read dir; do
  if [ -d ~/github/$dir/.git ]; then
    echo "$dir"
  fi
done | grep -v "vendor\|archive\|node_modules"
```

**Default Exclusions**:
- `vendor/` - Third-party dependencies
- `archive/` - Archived projects
- `node_modules/` - NPM packages
- `*-archive/` - Archived directories

**Use Case**: Quick analysis across all your projects without configuration overhead

---

### Configured Mode (Explicit Control)

**How it works**: Use `.aget/config/repos.yaml` for precise control

**Configuration File**: `.aget/config/repos.yaml`
```yaml
repos:
  include:
    - ~/github/api-service
    - ~/github/web-service
    - ~/github/worker-service
    - ~/github/microservice-*  # Wildcard supported

  exclude:
    - ~/github/vendor/*
    - ~/github/archive/*
    - ~/github/*/node_modules
    - ~/github/experimental-*

  auto_scan:
    enabled: false  # Disable auto-scan, use include list only
    path: ~/github
```

**Usage**:
```bash
# Use configured repos (reads .aget/config/repos.yaml)
python3 .aget/patterns/analysis/multi_repo_scan.py --mode configured
```

**Use Case**: Analyzing specific subset of repositories (e.g., only production microservices)

---

### Hybrid Mode (Balanced)

**How it works**: Auto-scan with custom exclusions

**Configuration**: `.aget/config/repos.yaml`
```yaml
repos:
  include: []  # Empty = auto-scan

  exclude:
    - ~/github/my-private-project
    - ~/github/client-*  # Exclude client work
    - ~/github/archive/*

  auto_scan:
    enabled: true  # Fallback to auto-scan
    path: ~/github
```

**Behavior**:
1. If `include` list is **empty** → Auto-scan `~/github/`
2. Apply `exclude` filters to discovered repos
3. Return filtered list

**Use Case**: Most common approach - scan everything except specific exclusions

---

## Configuration Examples

### Example 1: Microservices Analysis

**Goal**: Analyze consistency across 8 microservices

```yaml
# .aget/config/repos.yaml
repos:
  include:
    - ~/github/api-gateway
    - ~/github/auth-service
    - ~/github/user-service
    - ~/github/order-service
    - ~/github/payment-service
    - ~/github/notification-service
    - ~/github/analytics-service
    - ~/github/admin-service

  exclude: []

  auto_scan:
    enabled: false

  analysis_focus:
    - framework_consistency  # Same Flask version?
    - database_consistency   # Same PostgreSQL version?
    - logging_consistency    # Same logging format?
    - testing_consistency    # All using pytest?
```

**Run Analysis**:
```bash
python3 .aget/patterns/analysis/multi_repo_scan.py \
  --mode configured \
  --analysis-type consistency
```

---

### Example 2: Client Projects (Exclude Confidential)

**Goal**: Analyze personal projects only, exclude client work

```yaml
# .aget/config/repos.yaml
repos:
  include: []  # Auto-scan

  exclude:
    - ~/github/client-acme-*
    - ~/github/client-contoso-*
    - ~/github/confidential-*
    - ~/github/work-*

  auto_scan:
    enabled: true
    path: ~/github

  sensitivity:
    level: personal  # Skip confidential repos
```

---

### Example 3: Python Projects Only

**Goal**: Analyze only Python repositories

```yaml
# .aget/config/repos.yaml
repos:
  include: []  # Auto-scan

  exclude:
    - ~/github/*/node_modules
    - ~/github/vendor

  auto_scan:
    enabled: true
    path: ~/github

  filters:
    language: python  # Only analyze Python repos
    min_files: 5      # Skip toy projects (<5 files)
```

---

## Analysis Types

### 1. Consistency Analysis

**Purpose**: Check if related repositories follow same patterns

**Example Output**:
```
Consistency Analysis: 8 repositories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shared Patterns (Consistent):
✅ Framework: Flask 2.0 (8/8 repos)
✅ Database: PostgreSQL 14 (8/8 repos)
✅ Python Version: 3.11 (8/8 repos)

Inconsistencies:
⚠️  ORM Usage:
   - SQLAlchemy: api-gateway, user-service, order-service
   - Raw SQL: auth-service, payment-service, notification-service
   - Django ORM: analytics-service, admin-service
   Recommendation: Standardize on SQLAlchemy (most used)

⚠️  Testing Framework:
   - pytest: api-gateway, user-service, order-service (3/8)
   - unittest: auth-service, payment-service (2/8)
   - None: notification-service, analytics-service, admin-service (3/8)
   Recommendation: Add pytest to all services

⚠️  Logging:
   - Structured JSON: api-gateway
   - Python logging: user-service, auth-service, order-service
   - print() statements: payment-service, notification-service, analytics-service, admin-service
   Recommendation: Migrate all to structured JSON logging
```

**Actionable Recommendations**:
1. High Priority: Standardize ORM (SQLAlchemy)
2. High Priority: Add pytest to 5 services
3. Medium Priority: Migrate to structured logging

---

### 2. Pattern Recognition

**Purpose**: Identify architectural patterns used across repos

**Example Output**:
```
Pattern Recognition: 15 repositories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Detected Patterns:
📦 Framework: Flask (10), Django (3), FastAPI (2)
📦 Database: PostgreSQL (8), MySQL (4), MongoDB (3)
📦 Testing: pytest (7), unittest (4), none (4)
📦 CI/CD: GitHub Actions (12), Jenkins (2), none (1)
📦 Documentation: Sphinx (5), MkDocs (3), none (7)

Architecture Patterns:
🏗️  Monolith: 3 repos
🏗️  Microservices: 8 repos
🏗️  Serverless: 2 repos
🏗️  Hybrid: 2 repos
```

---

### 3. Duplicate Code Detection

**Purpose**: Find similar code blocks that could be extracted to shared library

**Example Output**:
```
Duplicate Code Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duplicates Found: 5

🔴 High Similarity (>90%):
   - api-gateway/src/db.py vs user-service/src/db.py (95% similar)
     Code: Database connection initialization (32 lines)
     Recommendation: Extract to shared library (common-db-utils)

🟡 Medium Similarity (80-90%):
   - auth-service/src/jwt.py vs api-gateway/src/auth.py (85% similar)
     Code: JWT token validation (48 lines)
     Recommendation: Consider shared auth library

   - order-service/src/email.py vs notification-service/src/mailer.py (82% similar)
     Code: Email sending logic (56 lines)
     Recommendation: Extract to shared notification library

Potential Savings:
- Code reduction: ~200 lines
- Maintenance: Single source of truth for DB/auth/email logic
```

---

## Workflow Examples

### Example 1: Microservices Consistency Check

**Scenario**: Check if all microservices use same logging format

```bash
# 1. Run consistency analysis
python3 .aget/patterns/analysis/multi_repo_scan.py \
  --mode configured \
  --analysis-type consistency

# 2. Review report
# Inconsistency: 3 different logging approaches
# - api-service: Structured JSON ✅
# - web-service: print() statements ❌
# - worker-service: Python logging module ⚠️

# 3. Standardize
# Target: Structured JSON logging for all services

# 4. Update repos
cd ~/github/web-service
# [Implement structured logging]

cd ~/github/worker-service
# [Migrate to structured logging]

# 5. Re-run analysis
# Result: All 3 services now use structured JSON ✅
```

---

### Example 2: Find Duplicate Database Code

**Scenario**: Extract shared database logic to library

```bash
# 1. Run duplicate detection
python3 .aget/patterns/analysis/multi_repo_scan.py \
  --mode auto \
  --analysis-type duplicates

# 2. Review findings
# Duplicate: Database connection code (95% similar)
# Repos: api-gateway, user-service, order-service

# 3. Create shared library
mkdir -p ~/github/shared-db-utils
# [Extract common DB code]

# 4. Update microservices
cd ~/github/api-gateway
pip install ../shared-db-utils
# [Replace local code with library]

# 5. Verify
python3 .aget/patterns/analysis/multi_repo_scan.py \
  --mode auto \
  --analysis-type duplicates

# Result: Duplicate reduced from 95% to 15% ✅
```

---

### Example 3: Architecture Compliance Validation

**Scenario**: Verify all new microservices follow organizational standards

```bash
# 1. Define organizational standards
cat > ~/github/template-developer-aget/.aget/standards/microservice.yaml <<EOF
microservice_standards:
  required:
    - framework: Flask 2.0+
    - database: PostgreSQL 14+
    - testing: pytest
    - ci: GitHub Actions
    - logging: structured JSON
    - documentation: README.md with API docs
EOF

# 2. Scan repositories
python3 .aget/patterns/analysis/multi_repo_scan.py \
  --mode configured \
  --analysis-type compliance \
  --standard .aget/standards/microservice.yaml

# 3. Review compliance report
# api-service: 6/6 ✅ Fully compliant
# web-service: 4/6 ⚠️  Missing: testing, documentation
# worker-service: 3/6 ❌ Missing: testing, documentation, structured logging

# 4. Remediate non-compliant services
# [Add pytest, docs, structured logging to web-service and worker-service]

# 5. Re-validate
# All services: 6/6 ✅
```

---

## Advanced Configuration

### Wildcard Patterns

**Include with wildcards**:
```yaml
repos:
  include:
    - ~/github/microservice-*      # All microservices
    - ~/github/lib-*                # All libraries
    - ~/github/tool-*               # All tools
```

---

### Language Filtering

**Analyze only specific languages**:
```yaml
repos:
  include: []  # Auto-scan

  filters:
    languages:
      - python
      - javascript
    exclude_languages:
      - go  # Skip Go projects
```

---

### Minimum Size Filtering

**Skip toy projects**:
```yaml
repos:
  include: []  # Auto-scan

  filters:
    min_files: 10        # Skip repos with <10 files
    min_commits: 5       # Skip repos with <5 commits
    exclude_forks: true  # Skip forked repos
```

---

## Integration Workflows

### Interactive Advisory Session
```
User: "Analyze all my microservices for logging consistency"

Advisor:
1. Discovers: api-service, web-service, worker-service (3 repos)
2. Analyzes logging patterns in each
3. Reports:
   - api-service: Structured JSON logging ✅
   - web-service: print() statements ❌
   - worker-service: Python logging module ⚠️
4. Recommends: Standardize on structured logging across all services
5. Provides migration guide for web-service and worker-service
```

---

### CI/CD Pipeline (Multi-Repo Validation)
```yaml
# .github/workflows/multi_repo_check.yml
name: Multi-Repo Consistency Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday

jobs:
  consistency-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code Analyzer
        uses: actions/checkout@v3
        with:
          repository: aget-framework/template-developer-aget
          path: analyzer

      - name: Clone All Microservices
        run: |
          for repo in api-service web-service worker-service; do
            git clone https://github.com/myorg/$repo
          done

      - name: Run Consistency Analysis
        run: |
          python3 analyzer/.aget/patterns/analysis/multi_repo_scan.py \
            --mode configured \
            --analysis-type consistency \
            --format json > consistency_report.json

      - name: Check for Inconsistencies
        run: |
          inconsistencies=$(jq '.inconsistencies | length' consistency_report.json)
          if [ "$inconsistencies" -gt 0 ]; then
            echo "Found $inconsistencies inconsistencies"
            jq '.inconsistencies' consistency_report.json
            exit 1
          fi
```

---

## Troubleshooting

### "No repositories found"
**Cause**: Auto-scan path incorrect or all repos excluded

**Fix**: Check configuration
```bash
# Verify repos exist
ls -la ~/github/

# Check config
cat .aget/config/repos.yaml

# Test auto-scan manually
ls ~/github/ | while read dir; do
  if [ -d ~/github/$dir/.git ]; then
    echo "Found: $dir"
  fi
done
```

---

### "Analysis shows 0 inconsistencies (but there are)"
**Cause**: Pattern detection too lenient

**Fix**: Adjust sensitivity
```yaml
repos:
  analysis_config:
    similarity_threshold: 0.8  # Stricter (default: 0.9)
    min_pattern_occurrences: 2  # Report if appears in 2+ repos
```

---

### "Performance slow (>5 min for 10 repos)"
**Cause**: Deep analysis on large codebases

**Fix**: Use caching and filtering
```yaml
repos:
  performance:
    cache_enabled: true
    cache_ttl: 3600  # 1 hour
    max_file_size: 1000000  # Skip files >1MB
    exclude_patterns:
      - "*/test_*"  # Skip test files for faster scan
```

---

## Related Guides

- **Code Quality**: `docs/CODE_QUALITY_GUIDE.md`
- **Standards Checking**: `docs/STANDARDS_CHECKING_GUIDE.md`
- **Pattern Library**: `.aget/patterns/analysis/multi_repo_scan.py`

---

*Generated for template-developer-aget v2.7.0*
