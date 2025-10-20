# Session Metadata Migration Guide

**Version:** v2.2.0 → v2.3.0
**Date:** 2025-10-02
**Status:** Active

---

## Overview

v2.3 introduces automated session metadata collection to address the 60% session documentation gap. This guide helps migrate AGETs from v2.2 (no metadata) to v2.3 (automated metadata).

## What's New in v2.3

**Session Metadata System:**
- Automated metadata extraction from git history and session content
- YAML frontmatter format for session files
- Validation against JSON Schema
- 80%+ adoption target (from 4.5% baseline)

**Required Fields:**
- `date`: Session date (YYYY-MM-DD)
- `duration_minutes`: Session length
- `objectives`: What you aimed to do
- `outcomes`: What you accomplished

**Optional Fields:**
- `learnings`: L-numbered learnings captured
- `issues_filed`: GitHub issues created
- `commits`: Git commits made
- `files_changed`: Number of files modified
- `patterns_used`: Patterns with versions
- `agets_collaborated`: Other AGETs involved
- `pain_points`: Difficulties encountered
- `next_steps`: Follow-up tasks

## Migration Steps

### Step 1: Deploy Metadata System

```bash
# On each AGET
cd ~/github/my-<name>-aget

# Switch to v2.3-dev branch (or create it)
git checkout v2.3-dev || git checkout -b v2.3-dev

# Copy metadata system from coordinator
# (This should already be done if deployment script ran)

# Verify files present
ls -la .aget/schemas/session_metadata_v1.0.*
ls -la .aget/tools/generate_session_metadata.py
ls -la .aget/tools/validate_session_metadata.py
```

### Step 2: Test Metadata Generation

```bash
# Test metadata generator (dry run)
python3 .aget/tools/generate_session_metadata.py \
  --objectives "Test metadata system" \
  --outcomes "Metadata working" \
  --duration 30 \
  --dry-run
```

Expected output:
```yaml
---
date: '2025-10-02'
duration_minutes: 30
objectives:
- Test metadata system
outcomes:
- Metadata working
---
```

### Step 3: Validate Existing Sessions

```bash
# Scan all sessions for baseline
python3 .aget/tools/validate_session_metadata.py --scan
```

This shows:
- How many sessions exist
- How many have metadata (probably 0-10%)
- Adoption rate baseline

### Step 4: Update Wind Down Workflow

**Option A: Manual (Recommended for v2.3)**

When winding down a session:

```bash
# Before committing session notes, run:
python3 .aget/tools/generate_session_metadata.py \
  --session-file sessions/SESSION_2025-10-02.md \
  --objectives "What I aimed to do" "Second objective" \
  --outcomes "What I accomplished" "Second outcome" \
  --duration 120

# This prepends metadata to your session file
# Then commit as usual
git add sessions/
git commit -m "session: Document <topic>"
```

**Option B: Integrated (Future v2.4)**

The wind down pattern will automatically call the metadata generator.

### Step 5: Create Session with Metadata

**Example Session File:**

```markdown
---
date: "2025-10-02"
duration_minutes: 120
objectives:
  - "Migrate to v2.3 metadata system"
  - "Test metadata generation"
outcomes:
  - "Metadata system deployed"
  - "First session with metadata created"
learnings:
  - id: "L26"
    description: "Metadata makes sessions mineable"
commits:
  - hash: "abc1234"
    message: "metadata: Deploy metadata system"
files_changed: 5
---

# Session Notes

Your regular session notes go here...

## Work Completed
- Deployed metadata system
- Tested metadata generation

## Next Steps
- Use metadata in all future sessions
```

### Step 6: Validate Session

```bash
# Validate specific session
python3 .aget/tools/validate_session_metadata.py \
  sessions/SESSION_2025-10-02.md

# Should show:
# ✅ Metadata is valid
# Completeness: X/8 optional fields
```

### Step 7: Monitor Adoption

```bash
# Check adoption progress
python3 .aget/tools/validate_session_metadata.py --scan

# Target: 80%+ of sessions should have valid metadata
```

## Migration Checklist

- [ ] v2.3-dev branch created
- [ ] Metadata system files present (.aget/schemas/, .aget/tools/)
- [ ] Test metadata generation (dry run) ✅
- [ ] Baseline adoption measured
- [ ] Created first session with metadata
- [ ] Validated session ✅
- [ ] Committed metadata-enabled session
- [ ] Adoption monitored (aim for 80%+)

## Backwards Compatibility

**v2.2 Sessions (no metadata):**
- ✅ Still readable
- ✅ No migration required
- ⚠️  Won't appear in metadata-based queries
- 💡 Consider adding metadata retroactively to important sessions

**Mixed Ecosystem:**
- Coordinator on v2.3 can read v2.2 and v2.3 sessions
- Visibility features work with metadata-enabled sessions only
- Session mining quality improves as adoption increases

## Common Issues

### Issue: "No metadata frontmatter found"

**Cause:** Session file doesn't start with `---`

**Solution:**
```bash
# Add metadata to existing session
python3 .aget/tools/generate_session_metadata.py \
  --session-file sessions/SESSION_2025-10-01.md \
  --objectives "Original objective" \
  --outcomes "What was accomplished" \
  --duration 60
```

### Issue: "Missing required field: objectives"

**Cause:** Metadata missing required fields

**Solution:** Add required fields to frontmatter:
```yaml
---
date: "2025-10-02"
duration_minutes: 120
objectives:   # REQUIRED
  - "At least one objective"
outcomes:     # REQUIRED
  - "At least one outcome"
---
```

### Issue: "Invalid date format"

**Cause:** Date not in YYYY-MM-DD format

**Solution:** Fix date format:
```yaml
# Wrong:
date: 10/02/2025

# Right:
date: "2025-10-02"
```

### Issue: "Learning ID invalid format"

**Cause:** Learning ID doesn't match L[0-9]+ pattern

**Solution:**
```yaml
# Wrong:
learnings:
  - id: "Learning 1"

# Right:
learnings:
  - id: "L26"
    description: "Learning description"
```

## FAQ

### Q: Do I need to migrate old sessions?

**A:** No. Old sessions without metadata will continue to work. However, they won't benefit from:
- Cross-AGET visibility queries
- Session mining improvements
- Collaboration context tracking

Consider adding metadata to important/recent sessions retroactively.

### Q: How much overhead does metadata add?

**A:** Minimal:
- Generation: <2 seconds (automated extraction from git)
- Manual input: ~30 seconds (objectives + outcomes)
- Validation: <1 second per session

Target: <5 seconds total overhead per session.

### Q: What if I forget to add metadata?

**A:** The session is still valid. You can:
- Add metadata later with `--session-file` flag
- Skip metadata for quick/trivial sessions
- Aim for 80%+ adoption, not 100%

### Q: Can I customize the metadata fields?

**A:** Optional fields can be omitted. Required fields are:
- `date`, `duration_minutes`, `objectives`, `outcomes`

Future versions may support custom fields via `additionalProperties`.

### Q: How does this help with collaboration?

**A:** Session metadata enables:
- **Cross-AGET Visibility** (Gate A4): Coordinator sees all AGET activity
- **Discovery** (Gate A5): Find AGETs by recent work
- **Context Handoff** (Gate A6): Include session refs in collaboration context
- **Session Mining** (v2.3+): Extract 3x more enhancement ideas

## Validation Schema

Full JSON Schema: `.aget/schemas/session_metadata_v1.0.json`

Quick reference:
```json
{
  "required": ["date", "duration_minutes", "objectives", "outcomes"],
  "properties": {
    "date": {"type": "string", "format": "date"},
    "duration_minutes": {"type": "integer", "minimum": 1, "maximum": 600},
    "objectives": {"type": "array", "minItems": 1},
    "outcomes": {"type": "array", "minItems": 1},
    "learnings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "description"],
        "properties": {
          "id": {"pattern": "^L[0-9]+$"}
        }
      }
    }
  }
}
```

## Resources

- Schema: `.aget/schemas/session_metadata_v1.0.yaml`
- JSON Schema: `.aget/schemas/session_metadata_v1.0.json`
- Generator: `.aget/tools/generate_session_metadata.py`
- Validator: `.aget/tools/validate_session_metadata.py`
- Example: `sessions/SESSION_2025-10-02_v2.3_gates_A1_A2_A3.md`

---

*Session Metadata Migration Guide - v2.3.0*
*Enabling automated session documentation and cross-AGET visibility*
