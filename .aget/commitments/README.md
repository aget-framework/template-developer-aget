# Commitment Tracking

**Purpose**: Track client commitments for accountability and follow-up.

**Required for**: Coach (high), Mentor (medium)

**Optional for**: Teacher (low - homework tracking), Consultant (low), Guru (low)

---

## File Format

### File Structure

Two files track commitment lifecycle:

```
.aget/commitments/
├── active.yaml          # Pending and in-progress commitments
└── completed.yaml       # Fulfilled commitments (archive)
```

---

## Active Commitments Format

```yaml
# active.yaml

commitments:
  - id: C001
    description: "Observe Sarah in next week's architecture review"
    context: "IC promotion decision - testing strategic thinking assumption"
    created: 2025-10-10
    due: 2025-10-17
    status: pending  # pending / in_progress / overdue
    client_id: principal_user

  - id: C002
    description: "Draft promotion criteria for Principal role"
    context: "Need clear rubric before making decision"
    created: 2025-10-10
    due: 2025-10-15
    status: overdue  # Automatically computed if past due date
    client_id: principal_user

  - id: C003
    description: "Practice saying 'no' to 1 non-critical request"
    context: "Delegation growth area - learning boundaries"
    created: 2025-10-08
    due: 2025-10-12
    status: in_progress
    client_id: principal_user
```

---

## Completed Commitments Format

```yaml
# completed.yaml

commitments:
  - id: C001
    description: "Observe Sarah in architecture review"
    context: "IC promotion decision"
    created: 2025-10-10
    due: 2025-10-17
    completed: 2025-10-16
    status: fulfilled
    outcome: "Sarah demonstrated strategic thinking in 3 key moments. Concerns addressed."
    client_id: principal_user

  - id: C002
    description: "Draft promotion criteria"
    context: "Principal role clarity"
    created: 2025-10-10
    due: 2025-10-15
    completed: 2025-10-18
    status: fulfilled_late  # Completed but after due date
    outcome: "Created 5-point rubric covering technical, strategic, and influence dimensions"
    client_id: principal_user
```

---

## Status Values

**Active commitments** (active.yaml):
- `pending`: Not yet started
- `in_progress`: Client actively working on it
- `overdue`: Past due date without completion

**Completed commitments** (completed.yaml):
- `fulfilled`: Completed on or before due date
- `fulfilled_late`: Completed after due date
- `abandoned`: Client decided not to pursue
- `renegotiated`: Changed scope or date (create new commitment, mark old as renegotiated)

---

## Commitment ID Convention

Format: `C{NNN}` where NNN is zero-padded sequential number.

**Examples**: C001, C002, C012, C153

**Generation**: Increment from highest existing ID across both files.

---

## Creation Protocol

### When Commitment Made

**Recognition signals** (client language):
- "I'll [action]"
- "I commit to [action]"
- "By [date], I will [action]"
- "Let me [action] and report back"

**Advisor response**:
1. Acknowledge commitment: "I hear you committing to [action]"
2. Clarify deadline: "By when?" (if not specified)
3. Add to context: Note why this matters

### At Wind Down

```python
# If commitment made during session
Edit: .aget/commitments/active.yaml

# Add new commitment with:
# - Next sequential ID
# - Description (client's words)
# - Context (why this matters)
# - Due date (client-specified or negotiated)
# - status: pending
# - client_id
```

---

## Update Protocol

### At Wake Up

**Check for overdue commitments**:
```python
# Read active.yaml
# Compute status for each:
#   if due_date < today and status != in_progress:
#     status = overdue
```

**Display**:
```
📋 Active commitments: 3
   • Observe Sarah (due 10/17) ✅ On track
   • Draft criteria (due 10/15) ⚠️ OVERDUE by 2 days
   • Practice saying no (in progress)
```

**Coaching opportunity**: "How's the promotion criteria draft going? I see it was due on the 15th."

---

### During Session

**When client reports progress**:

```python
# Update status if appropriate
Edit: .aget/commitments/active.yaml

# Change status: pending → in_progress (if they started)
# Or move to completed.yaml if fulfilled
```

**When commitment fulfilled**:
```python
# 1. Read commitment from active.yaml
# 2. Add 'completed' and 'outcome' fields
# 3. Compute status: fulfilled / fulfilled_late
# 4. Append to completed.yaml
# 5. Remove from active.yaml
```

---

## Usage Protocol

### At Wake Up (Coach/Mentor)

**Always check commitments first**:
```
📋 Active commitments: 2 pending
   • Observe Sarah (due 10/17)
   • Practice saying no (due 10/12)
```

If overdue:
```
⚠️ You have 1 overdue commitment:
   • Draft promotion criteria (due 10/15, now 2 days overdue)

   Would you like to start there, or has the context changed?
```

---

### During Session

**Follow up on commitments**:
- "Last time you committed to [X]. How did that go?"
- "I see you marked [Y] as in-progress. Tell me about it."

**When client reports completion**:
- Acknowledge: "Great! You followed through on [commitment]."
- Explore: "What did you learn?"
- Capture outcome in completed.yaml

**When commitment abandoned**:
- Explore: "What changed?"
- Mark as abandoned with reason
- Coach opportunity: "What does this tell us about priorities?"

---

### At Wind Down

**Summarize commitment status**:
```
✅ Updated commitment tracking:
   • C005: Marked as fulfilled (delegation experiment successful)
   • C006: New commitment added (observe Sarah, due 10/17)

Active: 2 commitments
Completed this month: 4
```

---

## Persona-Specific Guidance

### Coach (High Need)

**Why critical**: Accountability is core to coaching effectiveness.

**Track actively**: Every commitment, every session.

**Follow-up discipline**:
- Always check commitments at wake up
- Always follow up on overdue items
- Always acknowledge completion

**Coaching moves**:
- Overdue commitment: "What got in the way?"
- Pattern of abandonment: "What does this tell us about priorities?"
- Pattern of completion: "You're building a track record of follow-through!"

---

### Mentor (Medium Need)

**Why useful**: Accountability with lighter touch than coaching.

**Track selectively**: Major growth commitments, not every action item.

**Follow-up approach**:
- Check commitments but don't lead with them
- Wait for client to mention, then explore
- Focus on learning, not completion

**Mentoring moves**:
- "You said you'd try [X]. What happened?" (curious, not judge)
- If abandoned: "What did you learn about yourself?"

---

### Teacher (Low Need - Optional)

**Why sometimes useful**: Track homework completion for curriculum pacing.

**Track optionally**: Only for structured learning programs.

**Format adaptation**:
```yaml
commitments:
  - id: H001  # H for homework
    description: "Complete decorators exercises (3 problems)"
    due: 2025-10-15
    status: pending
    exercises:
      - "@retry decorator"
      - "@validate_input decorator"
      - "@cache decorator"
```

**Follow-up**: Check homework at start of session, review together.

---

### Consultant / Guru (Not Typically Used)

**Why rare**: Consultants make recommendations, clients own follow-through.

**Exception**: Long-term advisory relationships where tracking implementation is part of engagement.

---

## Privacy & Sensitivity

**Data classification**: Sensitive (client commitments may reveal personal/professional goals)

**Retention**: Active for duration of relationship, completed for 90 days

**Deletion**: Archive completed commitments after 90 days (or at relationship end)

---

## Anti-Patterns

### ❌ Creating Commitments Without Client Buy-In

**Bad**:
```yaml
# Advisor unilaterally adds commitment
commitments:
  - description: "Read 'Crucial Conversations' book"
    created: 2025-10-10
    due: 2025-10-31
```

**Why it fails**: Client didn't commit, advisor prescribed.

**Good**: Only track commitments client explicitly makes.

---

### ❌ Using Commitments as Task Management

**Bad**:
```yaml
commitments:
  - description: "Fix bug in authentication service"
  - description: "Write unit tests for new feature"
  - description: "Deploy to staging"
```

**Why it fails**: These are task lists, not developmental commitments.

**Good**: Commitments should be growth-oriented (trying new behavior, practicing skill, testing assumption).

---

### ❌ Not Following Up on Overdue Commitments

**Bad**:
```
User: "wake up"
Coach: "Ready for today's session."

[Ignores 2 overdue commitments]
```

**Why it fails**: Kills accountability, signals commitments don't matter.

**Good**: Always surface overdue commitments at wake up. Create coaching moment.

---

## Related Directories

- `.aget/sessions/` - Commitments extracted from session summaries
- `.aget/client_progress/` - Progress on focus areas (broader than individual commitments)

---

**Specification**: ADVISOR_INTERNAL_STATE_SPEC.md
**Version**: 1.0 (2025-10-10)
