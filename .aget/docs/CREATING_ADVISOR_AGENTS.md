# Creating Advisor Agents - Complete Guide

**Version**: 1.0
**Template**: template-advisor-aget v2.5.0
**Audience**: Users creating new advisor agent instances

---

## Overview

This guide walks through creating a new advisor agent from the template-advisor-aget template. Advisors are **read-only agents** that provide recommendations, analysis, and guidance without modifying systems.

**Time to complete**: 15-30 minutes
**Prerequisites**: Git, Python 3.7+, pytest, AI coding assistant (Claude Code, Cursor, etc.)

---

## When to Create an Advisor

### ✅ Use advisor template when you need:

- **Expert guidance without execution** - Recommendations, not actions
- **Persona-differentiated communication** - Teacher, mentor, consultant, guru, or coach style
- **Read-only analysis** - Code reviews, architecture assessments, learning guidance
- **Compliance scenarios** - Governance, audit, or advisory-only contexts
- **Decision support** - Trade-off analysis, option evaluation, confidence ratings

### ❌ Don't use advisor template when you need:

- **Action-taking capability** - Use template-worker-aget instead
- **File modification** - Advisors cannot edit, write, or create files
- **Command execution** - Advisors cannot execute commands with side effects
- **Flexible mode switching** - Advisors are always read-only (not configurable)

---

## Step-by-Step Creation

### Step 1: Choose Your Domain and Persona

**Domain**: What area will this advisor specialize in?
- Examples: system-architecture, career-guidance, code-quality, security-practices

**Persona**: What communication style fits your advisory approach?

| Persona | When to Use |
|---------|-------------|
| **teacher** | Educational content, explaining concepts, structured learning |
| **mentor** | Career guidance, personal development, reflective exploration |
| **consultant** | Business decisions, technical trade-offs, formal analysis |
| **guru** | Best practices, industry standards, authoritative expertise |
| **coach** | Performance improvement, skill practice, incremental feedback |

**Naming convention**:
```bash
my-{domain}-advisor-aget
```

Examples:
- `my-architecture-advisor-aget` (consultant persona)
- `my-security-advisor-aget` (guru persona)
- `my-code-review-coach-aget` (coach persona)
- `my-career-mentor-aget` (mentor persona)
- `my-python-teacher-aget` (teacher persona)

---

### Step 2: Clone the Template

```bash
# Navigate to your agent directory
cd ~/github

# Clone template with your chosen name
git clone https://github.com/aget-framework/template-advisor-aget.git my-{domain}-advisor-aget

# Example:
git clone https://github.com/aget-framework/template-advisor-aget.git my-architecture-advisor-aget

cd my-architecture-advisor-aget
```

---

### Step 3: Configure Identity

Edit `.aget/version.json`:

```json
{
  "aget_version": "2.5.0",
  "created": "2025-10-10",
  "template": "advisor",
  "tier": "specialized",

  // REQUIRED: Match your directory name exactly
  "agent_name": "my-architecture-advisor-aget",

  // REQUIRED: Always "aget" for advisors (read-only)
  "instance_type": "aget",

  // REQUIRED: Your specialization area
  "domain": "system-architecture",

  // REQUIRED: Always ["advisor"] for advisor agents
  "roles": ["advisor"],

  // REQUIRED: Choose one persona
  "persona": "consultant",

  // REQUIRED: Advisory capabilities (do not modify)
  "advisory_capabilities": {
    "read_only": true,
    "can_execute": false,
    "can_modify_files": false,
    "can_create_files": false,
    "can_recommend": true,
    "can_analyze": true,
    "can_critique": true,
    "supported_personas": ["teacher", "mentor", "consultant", "guru", "coach"],

    // Persona traits (all personas included)
    "persona_traits": {
      "teacher": {
        "focus": "instruction",
        "style": "structured_learning",
        "communication": "didactic",
        "examples": "comprehensive",
        "verification": "quiz_and_check"
      },
      "mentor": {
        "focus": "growth",
        "style": "reflective",
        "communication": "supportive",
        "guidance": "indirect",
        "timeline": "long_term"
      },
      "consultant": {
        "focus": "solutions",
        "style": "analytical",
        "communication": "formal",
        "deliverables": "trade_off_analysis",
        "confidence_explicit": true
      },
      "guru": {
        "focus": "expertise",
        "style": "authoritative",
        "communication": "principle_based",
        "context": "historical_and_best_practices"
      },
      "coach": {
        "focus": "performance",
        "style": "encouraging",
        "communication": "iterative",
        "feedback": "leveled_improvement",
        "practice": "regular_exercises"
      }
    }
  },

  // Optional: Organizational grouping
  "aget_group": "advisory",

  // Optional: Privacy classification
  "classification": "private"
}
```

**Key fields to update**:
1. `agent_name` - Match directory name exactly
2. `domain` - Your specialization area
3. `persona` - One of: teacher, mentor, consultant, guru, coach
4. `created` - Today's date (YYYY-MM-DD)

---

### Step 4: Validate Configuration

Run contract tests to verify configuration:

```bash
# Run all 16 tests
python3 -m pytest tests/ -v

# Expected output:
# tests/test_advisor_contract.py::test_instance_type_is_aget PASSED          [ 6%]
# tests/test_advisor_contract.py::test_role_includes_advisor PASSED          [12%]
# tests/test_advisor_contract.py::test_persona_declared PASSED               [18%]
# tests/test_advisor_contract.py::test_advisory_capabilities_read_only PASSED [25%]
# tests/test_advisor_contract.py::test_no_action_capabilities PASSED         [31%]
# tests/test_advisor_contract.py::test_persona_is_valid PASSED               [37%]
# tests/test_advisor_contract.py::test_supported_personas_list PASSED        [43%]
# tests/test_identity_contract.py::test_identity_consistency_version_json_vs_manifest PASSED [50%]
# tests/test_identity_contract.py::test_identity_no_conflation_with_directory_name PASSED [56%]
# tests/test_identity_contract.py::test_identity_persistence_across_invocations PASSED [62%]
# tests/test_wake_contract.py::test_wake_protocol_reports_agent_name PASSED  [68%]
# tests/test_wake_contract.py::test_wake_protocol_reports_version PASSED     [75%]
# tests/test_wake_contract.py::test_wake_protocol_reports_capabilities PASSED [81%]
# tests/test_wake_contract.py::test_wake_protocol_reports_domain PASSED      [87%]
# tests/test_wake_contract.py::test_wake_displays_advisory_mode PASSED       [93%]
# tests/test_wake_contract.py::test_wake_displays_persona PASSED             [100%]
#
# ======================== 16 passed in 0.06s =========================
```

**If tests fail**:
- Check `agent_name` matches directory name exactly (case-sensitive)
- Verify `instance_type` is "aget" (lowercase)
- Confirm `persona` is one of the 5 supported values
- Ensure `roles` includes "advisor"
- Validate `advisory_capabilities.read_only` is `true`

---

### Step 5: Customize Documentation

Edit `AGENTS.md` to add domain-specific context:

**Section to customize**: "## About This Agent"

```markdown
## About This Agent

**my-architecture-advisor-aget** - System architecture advisory agent

**Persona**: consultant (analytical, trade-off focused, formal communication)

**Domain**: System architecture decisions for web applications

**Specializations**:
- Microservices vs monolith trade-offs
- Database selection and data modeling
- API design and versioning strategies
- Scalability planning and capacity estimation
- Cloud provider selection and multi-cloud strategies

**Advisory Approach**:
- Gathers context through clarifying questions (team size, timeline, constraints)
- Presents options with explicit pros/cons and fit scores
- Provides confidence levels (High/Medium/Low) with reasoning
- States assumptions explicitly (team size, growth rate, budget)
- Identifies conditions that would change recommendation

**What I can help with**:
- "Should I use microservices or monolith?"
- "Which database fits my requirements?"
- "How should I design this API?"
- "What's the right cloud architecture for X?"

**What I won't do**:
- Implement solutions (I recommend, you execute)
- Modify your codebase
- Make decisions for you (I provide analysis, you decide)
```

**Optional sections to add**:
- **Knowledge Sources** - Books, papers, or resources you reference
- **Example Interactions** - Typical advisory flows
- **Success Criteria** - How to measure advisory value
- **Limitations** - Specific areas outside expertise

---

### Step 6: Initialize Git Repository

```bash
# Initialize as new repository
rm -rf .git  # Remove template git history
git init
git add .
git commit -m "init: Create my-{domain}-advisor-aget from template

- Configured identity (persona: {persona}, domain: {domain})
- All 16 contract tests passing
- Based on template-advisor-aget v2.5.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Step 7: Deploy to GitHub (Optional)

**Option A: Private Repository (Recommended)**

```bash
# Create private GitHub repository
gh repo create my-{domain}-advisor-aget --private --source=. --remote=origin

# Push initial commit
git push -u origin main
```

**Option B: Public Repository**

```bash
# Create public GitHub repository
gh repo create my-{domain}-advisor-aget --public --source=. --remote=origin

# Push initial commit
git push -u origin main
```

**Option C: Local Only**

Skip this step if keeping local-only. You can always deploy to GitHub later.

---

### Step 8: Verify Deployment

If deployed to GitHub, verify:

```bash
# Check repository exists
gh repo view my-{domain}-advisor-aget

# Verify version.json deployed
gh api repos/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/contents/.aget/version.json \
  | jq -r '.content' | base64 -d | jq -r '.aget_version'

# Expected: 2.5.0
```

---

### Step 9: Test Wake Protocol

Open your advisor with AI assistant and test wake protocol:

```bash
# Claude Code
claude .

# Or: Cursor, Aider, Windsurf, etc.
```

Test interaction:
```
You: wake up

AI: [Should display advisor identity with:]
    - Agent name + version
    - Mode: ADVISORY indicator
    - Persona declaration
    - Read-only warning
    - Domain/specialization
    - Readiness confirmation
```

**Expected output format**:
```
my-architecture-advisor-aget v2.5.0 (Advisor)
🎭 Mode: ADVISORY (recommendations only)
👤 Persona: consultant
📖 Domain: system-architecture

🚫 Read-only: Cannot modify files or execute commands
✅ Can: Analyze, recommend, critique, guide

Ready for questions.
```

---

## Post-Creation Checklist

- [ ] `.aget/version.json` configured with correct identity
- [ ] All 16 contract tests passing
- [ ] `AGENTS.md` customized with domain-specific context
- [ ] Git repository initialized and committed
- [ ] GitHub repository created (if deploying remotely)
- [ ] Wake protocol tested and displaying correctly
- [ ] Persona behavior matches chosen persona type

---

## Persona Behavior Validation

After creation, validate your advisor exhibits persona-appropriate behavior:

### Teacher Persona
- [ ] Provides structured explanations with numbered steps
- [ ] Includes comprehensive examples
- [ ] Asks comprehension check questions
- [ ] Breaks complex topics into digestible parts

### Mentor Persona
- [ ] Asks reflective questions
- [ ] Focuses on long-term growth
- [ ] Provides supportive, encouraging language
- [ ] Offers personalized guidance based on context

### Consultant Persona
- [ ] Presents options with pros/cons
- [ ] Includes confidence levels in recommendations
- [ ] Uses formal, professional language
- [ ] Provides fit scores or quantitative assessments

### Guru Persona
- [ ] References historical context and best practices
- [ ] Uses authoritative, principle-based language
- [ ] Cites industry standards and proven patterns
- [ ] Explains "why" with first principles

### Coach Persona
- [ ] Provides leveled improvements (Level 1, Level 2)
- [ ] Uses encouraging language ("Great start!", "Nice growth!")
- [ ] Tracks progress over time
- [ ] Suggests practice exercises

---

## Troubleshooting

### Contract Test Failures

**Test: `test_instance_type_is_aget`**
- **Error**: `instance_type must be 'aget', got 'AGET'`
- **Fix**: Change `instance_type` to lowercase "aget" in version.json

**Test: `test_persona_is_valid`**
- **Error**: `persona 'expert' not in supported_personas`
- **Fix**: Use one of: teacher, mentor, consultant, guru, coach

**Test: `test_role_includes_advisor`**
- **Error**: `roles must include 'advisor'`
- **Fix**: Set `roles: ["advisor"]` in version.json

**Test: `test_no_action_capabilities`**
- **Error**: `can_execute must be false`
- **Fix**: Ensure all action capabilities are `false` in advisory_capabilities

### Wake Protocol Issues

**Problem**: Wake protocol doesn't show advisory mode
- **Cause**: `advisory_capabilities.read_only` not set to `true`
- **Fix**: Set `"read_only": true` in advisory_capabilities section

**Problem**: Persona not displayed in wake protocol
- **Cause**: `persona` field is null or invalid
- **Fix**: Set persona to valid value (teacher/mentor/consultant/guru/coach)

### GitHub Deployment Issues

**Problem**: Repository already exists
- **Error**: `Name already exists on this account`
- **Fix**: Delete existing repo or choose different name
  ```bash
  gh repo delete my-{domain}-advisor-aget --confirm
  ```

**Problem**: Can't verify version.json on GitHub
- **Error**: 404 Not Found
- **Fix**: Ensure you pushed to main branch and file exists in .aget/ directory

---

## Next Steps

After creating your advisor:

1. **Add Knowledge Sources** - Document books, papers, or resources you reference
2. **Create Example Interactions** - Show typical advisory flows in AGENTS.md
3. **Develop Domain Expertise** - Add domain-specific patterns to `.aget/patterns/`
4. **Track Learnings** - Use `.aget/evolution/L*.md` for discoveries
5. **Session Management** - Use "wind down" to create session notes

---

## Reference Examples

See `.aget/examples/` for complete persona configurations:
- `persona_teacher.json` - Educational guidance agent
- `persona_mentor.json` - Career development advisor
- `persona_consultant.json` - Technical decision consultant
- `persona_guru.json` - Expert authority on best practices
- `persona_coach.json` - Performance improvement coach

---

## Support

**Questions or issues?**
- File issues: [aget-aget repo](https://github.com/aget-framework/aget/issues) with `[advisor-template]` prefix
- Review: [AGENTS.md](../../AGENTS.md) for complete advisor documentation
- Check: [ADVISOR_CAPABILITY_MATRIX.md](ADVISOR_CAPABILITY_MATRIX.md) for capability boundaries

---

*Guide Version: 1.0 | Template Version: v2.5.0 | Last Updated: 2025-10-10*
