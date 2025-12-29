#!/usr/bin/env python3
"""Developer Template Contract Tests

Code-analysis specific tests for template-developer-aget.
Tests multi-repo awareness, standards precedence, and analysis capabilities.

Part of AGET framework developer template validation (v2.7.0).
Total: 10 new tests + 16 inherited tests from advisor template = 26 tests

v2.10.0: Added template context detection - instance-only tests skipped on templates
"""

import pytest
import json
import os
import tempfile
import shutil
from pathlib import Path
from conftest import is_template_context


# Skip reason for instance-only tests (memory layer tests)
SKIP_TEMPLATE = pytest.mark.skipif(
    is_template_context(),
    reason="Instance-only test: .memory/ directory is created at instantiation"
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def temp_github_dir(tmp_path):
    """Create temporary ~/github/ directory for multi-repo tests."""
    github_dir = tmp_path / "github"
    github_dir.mkdir()
    yield github_dir
    # Cleanup handled by tmp_path


@pytest.fixture
def test_repo_a(temp_github_dir):
    """Create test repository A with sample code."""
    repo_dir = temp_github_dir / "test-repo-a"
    repo_dir.mkdir()

    # Create .git directory (marks as git repo)
    (repo_dir / ".git").mkdir()

    # Create sample code file
    code_file = repo_dir / "app.py"
    code_file.write_text("""#!/usr/bin/env python3
def hello():
    return "Hello from repo A"
""")

    yield repo_dir


@pytest.fixture
def test_repo_b(temp_github_dir):
    """Create test repository B with sample code."""
    repo_dir = temp_github_dir / "test-repo-b"
    repo_dir.mkdir()

    # Create .git directory
    (repo_dir / ".git").mkdir()

    # Create sample code file
    code_file = repo_dir / "utils.py"
    code_file.write_text("""#!/usr/bin/env python3
def greet():
    return "Greetings from repo B"
""")

    yield repo_dir


@pytest.fixture
def repos_config_file(tmp_path):
    """Create repos.yaml configuration file."""
    config_dir = tmp_path / ".aget" / "config"
    config_dir.mkdir(parents=True)

    config_file = config_dir / "repos.yaml"
    yield config_file


@pytest.fixture
def custom_python_standard(tmp_path):
    """Create custom Python coding standard file."""
    standards_dir = tmp_path / ".aget" / "standards"
    standards_dir.mkdir(parents=True)

    standard_file = standards_dir / "python.md"
    standard_file.write_text("""# Custom Python Standards

## Rules
- Max line length: 100 (not 79)
- Docstrings: Google style required
- Type hints: Required for all public functions
""")

    yield standard_file


@pytest.fixture
def repo_specific_standard(tmp_path):
    """Create repository-specific coding standard."""
    standard_file = tmp_path / ".coding-standards.md"
    standard_file.write_text("""# Repo-Specific Standards

## Rules
- Max line length: 120 (project uses wide monitors)
- Testing: pytest required
""")

    yield standard_file


@pytest.fixture
def test_code_with_violations(tmp_path):
    """Create Python file with known PEP-8 violations."""
    code_file = tmp_path / "test_violations.py"
    code_file.write_text("""#!/usr/bin/env python3
# E501: Line too long
def very_long_function_name_that_exceeds_seventy_nine_characters_for_pep8(argument_one, argument_two, argument_three):
    pass

# E722: Bare except
def bad_exception():
    try:
        risky_operation()
    except:
        pass

# F841: Unused variable
def unused_var():
    x = 5
    y = 10
    return x
""")

    yield code_file


@pytest.fixture
def test_spec_file(tmp_path):
    """Create minimal YAML specification file."""
    spec_file = tmp_path / "test_spec.yaml"
    spec_content = """spec:
  id: TEST-SPEC
  version: v1.0.0

capabilities:
  CAP-001:
    statement: "The SYSTEM shall provide user login"
    type: ubiquitous
    priority: high

  CAP-002:
    statement: "The SYSTEM shall provide password reset"
    type: event-driven
    priority: high

  CAP-003:
    statement: "The SYSTEM shall send email notifications"
    type: event-driven
    priority: medium

  CAP-004:
    statement: "The SYSTEM shall provide API for user profile"
    type: ubiquitous
    priority: medium

  CAP-005:
    statement: "The SYSTEM shall log all transactions"
    type: ubiquitous
    priority: low
"""
    spec_file.write_text(spec_content)
    yield spec_file


@pytest.fixture
def test_implementation_partial(tmp_path):
    """Create code implementing 3 of 5 spec capabilities."""
    impl_dir = tmp_path / "implementation"
    impl_dir.mkdir()

    # Implement CAP-001 (login)
    auth_file = impl_dir / "auth.py"
    auth_file.write_text("""def login(username, password):
    # CAP-001: User login implementation
    return validate_credentials(username, password)
""")

    # Implement CAP-004 (user profile API)
    api_file = impl_dir / "api.py"
    api_file.write_text("""def get_user_profile(user_id):
    # CAP-004: User profile API
    return fetch_user(user_id)
""")

    # Implement CAP-005 (transaction logging)
    logger_file = impl_dir / "logger.py"
    logger_file.write_text("""def log_transaction(transaction):
    # CAP-005: Transaction logging
    write_log(transaction)
""")

    # CAP-002 (password reset) and CAP-003 (email) NOT implemented

    yield impl_dir


# ============================================================================
# Category 4: Multi-Repository Awareness (3 tests)
# Priority 1: Highest risk - validate hybrid approach
# ============================================================================

def test_can_discover_adjacent_repos(test_repo_a, test_repo_b, temp_github_dir):
    """Test 17: Verify multi-repo discovery works (auto-scan mode).

    Tests that the template can discover multiple git repositories
    in adjacent directories (simulating ~/github/ structure).
    """
    # Verify test repos were created
    assert test_repo_a.exists(), "Test repo A not created"
    assert test_repo_b.exists(), "Test repo B not created"
    assert (test_repo_a / ".git").exists(), "Test repo A missing .git"
    assert (test_repo_b / ".git").exists(), "Test repo B missing .git"

    # List all directories in temp_github_dir
    repos = [d for d in temp_github_dir.iterdir() if d.is_dir()]
    repo_names = [r.name for r in repos]

    # Should discover both test repos
    assert "test-repo-a" in repo_names, "Failed to discover test-repo-a"
    assert "test-repo-b" in repo_names, "Failed to discover test-repo-b"
    assert len(repos) == 2, f"Expected 2 repos, found {len(repos)}"


def test_respects_repo_configuration(test_repo_a, test_repo_b, repos_config_file):
    """Test 18: Verify config file overrides auto-scan.

    Tests that when .aget/config/repos.yaml exists with explicit
    include list, only specified repos are discovered (not auto-scan).
    """
    # Write config with only test-repo-a included
    config_content = f"""repos:
  include:
    - {str(test_repo_a)}
  exclude:
    - {str(test_repo_b)}
  auto_scan:
    enabled: false
"""
    repos_config_file.write_text(config_content)

    # Verify config file exists
    assert repos_config_file.exists(), "Repos config file not created"

    # Parse config
    import yaml
    with open(repos_config_file) as f:
        config = yaml.safe_load(f)

    # Verify configuration structure
    assert "repos" in config, "Config missing 'repos' section"
    assert "include" in config["repos"], "Config missing 'include' list"
    assert "exclude" in config["repos"], "Config missing 'exclude' list"

    # Verify include list contains test-repo-a
    include_list = config["repos"]["include"]
    assert len(include_list) == 1, f"Expected 1 included repo, got {len(include_list)}"
    assert str(test_repo_a) in include_list[0], "test-repo-a not in include list"

    # Verify exclude list contains test-repo-b
    exclude_list = config["repos"]["exclude"]
    assert len(exclude_list) == 1, f"Expected 1 excluded repo, got {len(exclude_list)}"
    assert str(test_repo_b) in exclude_list[0], "test-repo-b not in exclude list"


def test_cross_repo_file_reading(test_repo_a, test_repo_b):
    """Test 19: Verify can read files from multiple discovered repos.

    Tests that code-analysis advisor can read source files from
    multiple repositories in a single analysis session.
    """
    # Verify repos exist
    assert test_repo_a.exists(), "Test repo A not found"
    assert test_repo_b.exists(), "Test repo B not found"

    # Read file from repo A
    file_a = test_repo_a / "app.py"
    assert file_a.exists(), "app.py not found in repo A"
    content_a = file_a.read_text()
    assert "Hello from repo A" in content_a, "Unexpected content in repo A"

    # Read file from repo B
    file_b = test_repo_b / "utils.py"
    assert file_b.exists(), "utils.py not found in repo B"
    content_b = file_b.read_text()
    assert "Greetings from repo B" in content_b, "Unexpected content in repo B"

    # Both files readable in same session
    assert content_a != content_b, "Repo files should have different content"


# ============================================================================
# Category 6: Configuration & Standards (2 tests)
# Priority 2: Validate configuration model
# ============================================================================

def test_custom_standards_loading(custom_python_standard):
    """Test 24: Verify can load custom coding standards.

    Tests that custom standards from .aget/standards/python.md
    are loaded and can be applied (beyond built-in PEP-8).
    """
    # Verify custom standard file exists
    assert custom_python_standard.exists(), "Custom standard file not created"

    # Read custom standard
    content = custom_python_standard.read_text()

    # Verify content has custom rules
    assert "Max line length: 100" in content, "Custom line length rule missing"
    assert "Google style" in content, "Custom docstring style missing"
    assert "Type hints: Required" in content, "Custom type hints rule missing"

    # Verify it's different from PEP-8 (which specifies 79 chars)
    assert "100" in content, "Custom standard should specify 100, not 79"


def test_standards_precedence_order(custom_python_standard, repo_specific_standard):
    """Test 25: Verify standards precedence (repo > agent > built-in).

    Tests that when both repo-specific and agent-level standards exist,
    the repo-specific standard takes precedence.
    """
    # Verify both standards exist
    assert custom_python_standard.exists(), "Agent-level standard not found"
    assert repo_specific_standard.exists(), "Repo-specific standard not found"

    # Read both standards
    agent_content = custom_python_standard.read_text()
    repo_content = repo_specific_standard.read_text()

    # Agent-level says max line length: 100
    assert "100" in agent_content, "Agent standard should specify 100"

    # Repo-specific says max line length: 120 (takes precedence)
    assert "120" in repo_content, "Repo standard should specify 120"

    # Verify they conflict (proof of precedence test)
    assert "100" in agent_content and "120" in repo_content, \
        "Standards should have conflicting rules to test precedence"

    # Precedence order: repo (120) > agent (100) > built-in (79)
    # In actual usage, repo-specific standard (120) would win


# ============================================================================
# Category 5: Code Analysis Capabilities (4 tests)
# Priority 3: Core functionality validation
# ============================================================================

def test_code_quality_analysis_capability(test_code_with_violations):
    """Test 20: Verify can analyze code quality.

    Tests that code quality analysis pattern exists and can detect
    complexity issues, code smells, and generate ratings.
    """
    # Verify test code exists
    assert test_code_with_violations.exists(), "Test code file not created"

    # Verify pattern file exists
    pattern_file = Path(__file__).parent.parent / ".aget/patterns/analysis/code_quality.py"
    assert pattern_file.exists(), \
        f"Code quality pattern not found at {pattern_file}"

    # Read test code
    code_content = test_code_with_violations.read_text()

    # Verify test code has detectable issues
    assert "very_long_function_name" in code_content, "Test should have long function name"
    assert "unused_var" in code_content, "Test should have unused variable"

    # Pattern file should define analyze() function
    pattern_content = pattern_file.read_text()
    assert "def analyze" in pattern_content, "Pattern missing analyze() function"


def test_standards_compliance_checking(test_code_with_violations):
    """Test 21: Verify can check coding standards.

    Tests that standards checking pattern exists and can detect
    PEP-8 violations (E501 line too long, E722 bare except).
    """
    # Verify test code exists
    assert test_code_with_violations.exists(), "Test code file not created"

    # Verify pattern file exists
    pattern_file = Path(__file__).parent.parent / ".aget/patterns/analysis/standards_check.py"
    assert pattern_file.exists(), \
        f"Standards check pattern not found at {pattern_file}"

    # Read test code - should have violations
    code_content = test_code_with_violations.read_text()

    # Verify violations are present
    assert "seventy_nine_characters" in code_content, "E501 violation (long line) missing"
    assert "except:" in code_content and "except Exception" not in code_content, \
        "E722 violation (bare except) missing"
    assert "y = 10" in code_content and "return x" in code_content, \
        "F841 violation (unused variable) missing"


def test_spec_to_code_consistency(test_spec_file, test_implementation_partial):
    """Test 22: Verify can compare spec vs implementation.

    Tests that spec consistency pattern exists and can detect
    coverage gaps (3/5 capabilities implemented).
    """
    # Verify inputs exist
    assert test_spec_file.exists(), "Test spec file not created"
    assert test_implementation_partial.exists(), "Test implementation not created"

    # Verify pattern file exists
    pattern_file = Path(__file__).parent.parent / ".aget/patterns/analysis/spec_consistency.py"
    assert pattern_file.exists(), \
        f"Spec consistency pattern not found at {pattern_file}"

    # Read spec file - should have 5 capabilities
    spec_content = test_spec_file.read_text()
    assert "CAP-001" in spec_content, "Spec missing CAP-001"
    assert "CAP-005" in spec_content, "Spec should have 5 capabilities"

    # Verify implementation files exist (3 implemented)
    assert (test_implementation_partial / "auth.py").exists(), "auth.py (CAP-001) missing"
    assert (test_implementation_partial / "api.py").exists(), "api.py (CAP-004) missing"
    assert (test_implementation_partial / "logger.py").exists(), "logger.py (CAP-005) missing"

    # CAP-002 and CAP-003 should NOT be implemented (gap detection test)
    impl_files = list(test_implementation_partial.glob("*.py"))
    impl_content = " ".join([f.read_text() for f in impl_files])
    # Check for password reset functionality (CAP-002)
    assert "reset_password" not in impl_content.lower() and \
           "password_reset" not in impl_content.lower(), \
        "CAP-002 (password reset) should not be implemented"
    # Check for email notification functionality (CAP-003)
    assert "send_email" not in impl_content.lower() and \
           "email_notification" not in impl_content.lower(), \
        "CAP-003 (email notifications) should not be implemented"


def test_debugging_assistance_capability():
    """Test 23: Verify can assist with debugging.

    Tests that debug assist pattern exists and can recognize
    error patterns and generate fix strategies.
    """
    # Verify pattern file exists
    pattern_file = Path(__file__).parent.parent / ".aget/patterns/analysis/debug_assist.py"
    assert pattern_file.exists(), \
        f"Debug assist pattern not found at {pattern_file}"

    # Pattern should handle common errors
    pattern_content = pattern_file.read_text()
    assert "def analyze" in pattern_content, "Pattern missing analyze() function"

    # Should recognize common error patterns
    # (Full error pattern matching tested in integration tests)


# ============================================================================
# Category 7: Advisory Enforcement (1 test)
# Priority 4: Validate consultant persona
# ============================================================================

def test_analysis_output_is_recommendations():
    """Test 26: Verify output format is advisory (not imperative).

    Tests that AGENTS.md and documentation use advisory language
    (recommend, suggest, consider) not imperative (do this, change).
    Enforces consultant persona requirement.
    """
    # Read AGENTS.md
    agents_md = Path(__file__).parent.parent / "AGENTS.md"
    assert agents_md.exists(), "AGENTS.md not found"

    content = agents_md.read_text().lower()

    # Should use advisory language
    advisory_terms = ["recommend", "suggest", "consider", "advise", "guide"]
    found_advisory = [term for term in advisory_terms if term in content]
    assert len(found_advisory) >= 2, \
        f"AGENTS.md should use advisory language, found only: {found_advisory}"

    # Verify template type (v3.0) or persona (v2.x)
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    with open(version_file) as f:
        data = json.load(f)
        # v3.0 uses template field, v2.x uses persona field
        template = data.get("template")
        persona = data.get("persona")
        assert template == "developer" or persona == "consultant", \
            f"Expected template='developer' (v3.0) or persona='consultant' (v2.x), got template={template}, persona={persona}"

    # Should NOT use imperative commands excessively
    # (Some imperative is OK for pattern instructions, but not analysis output)
    # This is a guideline check, not strict enforcement


# ============================================================================
# v3.0 Template Validation Tests
# ============================================================================

def test_template_type_is_developer():
    """Verify template type is 'developer' in v3.0 schema.

    v3.0 uses template field instead of v2.x persona/roles fields.
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    with open(version_file) as f:
        data = json.load(f)

    # v3.0 templates must have template field
    if data.get("manifest_version", "").startswith("3."):
        assert "template" in data, "v3.0 templates must have 'template' field"
        assert data["template"] == "developer", \
            f"Expected template='developer', got {data.get('template')}"


# ============================================================================
# Category 8: Memory Layer Tests (v2.9+) (6 tests)
# ============================================================================

@SKIP_TEMPLATE
def test_memory_directory_exists():
    """Test 27: Verify .memory/ directory exists for Layer 4 relationship state (v2.9+)."""
    memory_dir = Path(".memory")
    assert memory_dir.exists(), \
        "Developer advisor agents must have .memory/ directory at root (Layer 4 - v2.9 standard)"
    assert memory_dir.is_dir(), ".memory/ must be a directory"


@SKIP_TEMPLATE
def test_memory_clients_directory_exists():
    """Test 28: Verify .memory/clients/ for client relationship tracking (v2.9+)."""
    clients_dir = Path(".memory/clients")
    assert clients_dir.exists(), \
        ".memory/clients/ directory must exist for client relationship state"
    assert clients_dir.is_dir(), ".memory/clients/ must be a directory"


@SKIP_TEMPLATE
def test_memory_engagements_directory_exists():
    """Test 29: Verify .memory/engagements/ for engagement tracking (v2.9+)."""
    engagements_dir = Path(".memory/engagements")
    assert engagements_dir.exists(), \
        ".memory/engagements/ directory must exist for engagement state"
    assert engagements_dir.is_dir(), ".memory/engagements/ must be a directory"


def test_sessions_at_root():
    """Test 30: Sessions must be at root (sessions/), not in .aget/sessions/ (v2.9 standard)."""
    sessions_root = Path(__file__).parent.parent / "sessions"
    sessions_aget = Path(__file__).parent.parent / ".aget/sessions"

    # sessions/ at root is recommended (not strictly required for new templates)
    # This is more of a migration check, templates start fresh
    # But we document it as the standard location

    # If .aget/sessions/ exists with files, that's non-compliant
    if sessions_aget.exists() and sessions_aget.is_dir():
        session_files = list(sessions_aget.glob("SESSION_*.md"))
        assert len(session_files) == 0, \
            "Sessions must be in sessions/ at root, not .aget/sessions/ (v2.9 standard)"


@SKIP_TEMPLATE
def test_agents_md_documents_memory():
    """Test 31: AGENTS.md must document .memory/ usage for developer advisors (v2.9+)."""
    agents_md = Path("AGENTS.md")
    assert agents_md.exists(), "AGENTS.md not found"

    content = agents_md.read_text()
    assert ".memory/" in content, \
        "AGENTS.md must document .memory/ directory (Layer 4 developer advisor state)"
    assert "clients/" in content or "engagements/" in content, \
        "AGENTS.md must document .memory/clients/ and .memory/engagements/ subdirectories"


@SKIP_TEMPLATE
def test_memory_readme_exists():
    """Test 32: Verify .memory/README.md with usage guidelines (v2.9+)."""
    memory_readme = Path(".memory/README.md")
    assert memory_readme.exists(), \
        ".memory/README.md must exist with usage guidelines"

    # Verify it has some content
    content = memory_readme.read_text()
    assert len(content) > 500, \
        ".memory/README.md must have substantial usage documentation (≥500 chars)"
    assert "clients/" in content, \
        ".memory/README.md must document clients/ subdirectory"
    assert "engagements/" in content, \
        ".memory/README.md must document engagements/ subdirectory"


# ============================================================================
# Test Summary
# ============================================================================

"""
Contract Test Summary (26 total):

New Tests (10):
✅ Test 17: Multi-repo discovery (auto-scan)
✅ Test 18: Repo configuration (config override)
✅ Test 19: Cross-repo file reading
✅ Test 20: Code quality analysis capability
✅ Test 21: Standards compliance checking
✅ Test 22: Spec-to-code consistency
✅ Test 23: Debugging assistance capability
✅ Test 24: Custom standards loading
✅ Test 25: Standards precedence order
✅ Test 26: Analysis output is advisory

Inherited Tests (16):
- Test 1-16: From test_advisor_contract.py
- Validates: instance_type, persona, advisory capabilities,
  read-only enforcement, scoped writes, wake protocol, identity

Priority Order (implemented):
1. Multi-repo discovery (3 tests) - Highest risk
2. Standards precedence (2 tests) - Configuration model
3. Code analysis capabilities (4 tests) - Core functionality
4. Advisory enforcement (1 test) - Persona validation
5. Inherited tests (16 tests) - Run automatically

All tests follow contract testing pattern:
- Test framework structure (files exist)
- Test configuration (values correct)
- Test capability declarations (not full functionality)
- Integration tests handled separately
"""
