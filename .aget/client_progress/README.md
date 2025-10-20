# Client Progress Tracking

**Purpose**: Track client development over time.

**Required for**: Coach (high), Teacher (high), Mentor (medium)

**Optional for**: Consultant (low), Guru (low)

---

## File Format

### Naming Convention
```
{client_id}.yaml
```

**Examples**:
- `principal_user.yaml`
- `student_john_doe.yaml`
- `team_lead_sarah.yaml`

---

## File Structure

### Coach Persona

```yaml
client_id: principal_user
persona: coach
first_session: 2025-10-01
total_sessions: 12
last_session: 2025-10-10

# Development focus areas
focus_areas:
  - name: "Strategic thinking"
    confidence_level: 7  # Scale 1-10
    first_noted: 2025-10-01
    current_status: "Growing comfort with ambiguity, still seeks concrete answers"
    progress_notes:
      - "2025-10-01: Identified as growth edge"
      - "2025-10-05: First strategic framework discussion"
      - "2025-10-10: Applying framework independently"

  - name: "Delegation"
    confidence_level: 4
    first_noted: 2025-10-03
    current_status: "Recognizes need, struggles with letting go"
    progress_notes:
      - "2025-10-03: Realizes over-involvement in details"
      - "2025-10-08: Delegated first architecture decision"

# Overall development
development_trajectory:
  overall_confidence: 6  # Scale 1-10
  growth_rate: "Steady"  # Rapid / Steady / Slow
  key_shifts:
    - "Moved from seeking answers to asking better questions"
    - "Starting to trust team's judgment"

# Context
current_role: "Engineering Manager"
aspiration: "Principal Engineer"
key_challenges:
  - "IC → Manager transition"
  - "Building strategic muscle"
```

---

### Teacher Persona

```yaml
client_id: student_john_doe
persona: teacher
first_session: 2025-09-01
total_sessions: 24
last_session: 2025-10-10

# Learning progress
concepts_learned:
  - name: "Python basics"
    date_introduced: 2025-09-01
    date_mastered: 2025-09-15
    mastery_level: 9  # Scale 1-10
    exercises_completed: 15

  - name: "Object-oriented programming"
    date_introduced: 2025-09-16
    date_mastered: 2025-10-01
    mastery_level: 8
    exercises_completed: 12

  - name: "Decorators"
    date_introduced: 2025-10-08
    date_mastered: null  # In progress
    mastery_level: 6
    exercises_completed: 3

# Current curriculum
current_topic: "Decorators"
next_topic: "Context managers"
curriculum_completion: 45  # Percentage

# Learning patterns
learning_style: "Visual learner, needs concrete examples"
strengths:
  - "Grasps concepts quickly"
  - "Asks clarifying questions"
  - "Persistent with difficult topics"
areas_for_growth:
  - "Testing knowledge before moving forward"
  - "Building without examples first"

# Overall progress
overall_mastery: 6  # Scale 1-10
pace: "Accelerating"  # Accelerating / Steady / Slowing
readiness_for: "Intermediate topics (ready for async/await, generators)"
```

---

### Mentor Persona

```yaml
client_id: team_lead_sarah
persona: mentor
first_session: 2025-08-15
total_sessions: 8
last_session: 2025-10-10

# Growth areas
growth_focus:
  - name: "Influencing without authority"
    confidence: 5  # Scale 1-10
    first_noted: 2025-08-15
    current_status: "Building peer relationships, learning negotiation"
    growth_indicators:
      - "2025-08-15: Frustrated with lack of authority"
      - "2025-09-01: First successful cross-team collaboration"
      - "2025-10-10: Led architecture decision without formal role"

  - name: "Systems thinking"
    confidence: 6
    first_noted: 2025-08-22
    current_status: "Connecting technical decisions to business outcomes"

# Mentor relationship
relationship_stage: "Guiding" # Building Trust / Guiding / Stepping Back
mentee_ownership: "Medium"  # Low / Medium / High
ready_for_autonomy: false

# Career context
current_role: "Senior Engineer"
target_role: "Staff Engineer / Tech Lead"
timeline: "6-12 months"
blockers:
  - "Needs more cross-team influence experience"
  - "Developing product sense"
```

---

## Update Protocol

### When to Update

**Coach**:
- After every 3-5 sessions (or when significant progress observed)
- When confidence level shifts (±2 points)
- When new focus area emerges

**Teacher**:
- After each session (mastery levels change frequently)
- When concept mastered (move to next topic)
- When learning pattern identified

**Mentor**:
- After key milestones (growth indicators)
- When relationship stage shifts
- Quarterly career progress check

---

### How to Update

**During session**:
- Observe progress indicators
- Note confidence shifts
- Identify new areas

**At wind down**:
```python
# Update client progress (if applicable)
Edit: .aget/client_progress/{client_id}.yaml

# Example changes:
# - Increment total_sessions
# - Update confidence_level in focus_area
# - Add progress_note with date
# - Update mastery_level (teacher)
```

---

## Usage Protocol

### At Wake Up
```
📊 Progress: 12 sessions, +2 confidence in strategic thinking
```

Display brief progress summary if persona requires high state need (coach/teacher).

---

### During Session
- Reference progress: "You've grown from 5 to 7 in confidence since we started"
- Identify patterns: "I notice this is the 3rd time you've mentioned delegation"
- Celebrate milestones: "You've mastered 8 concepts in 2 months!"

---

### In Status Checks
```
User: "status"

Coach response:
📊 Client Progress

Sessions: 12 total (last: 2025-10-10)
Focus areas:
  • Strategic thinking: 7/10 (+2 since start)
  • Delegation: 4/10 (newly identified)

Overall trajectory: Steady growth
Key shift: Moved from seeking answers to asking questions
```

---

## Privacy & Sensitivity

**Data classification**: Sensitive (client performance, personal development)

**Access control**: Advisor agent only

**Retention**: Keep for duration of advisory relationship + 90 days

**Deletion**: When client relationship ends (documented in exit protocol)

---

## Persona-Specific Guidance

### Coach (High Need)
**Track actively**: Confidence levels are critical for coaching effectiveness.

**Update frequency**: Every 3-5 sessions

**Key metrics**:
- Confidence levels (1-10 scale)
- Focus areas and progress notes
- Development trajectory

**Anti-pattern**: Don't track task completion (that's project management, not coaching)

---

### Teacher (High Need)
**Track actively**: Mastery levels determine curriculum progression.

**Update frequency**: Every session

**Key metrics**:
- Mastery level (1-10 scale)
- Concepts learned vs in-progress
- Learning style and patterns

**Anti-pattern**: Don't move to next topic without mastery evidence

---

### Mentor (Medium Need)
**Track selectively**: Growth indicators over time, relationship stage.

**Update frequency**: After milestones

**Key metrics**:
- Growth focus confidence
- Relationship stage (trust → guiding → autonomy)
- Career progress toward target role

**Anti-pattern**: Don't over-specify steps (mentoring is guided discovery, not instruction)

---

### Consultant / Guru (Low Need)
**Track optionally**: Most consultants don't need progress tracking.

**When useful**: Long-term engagements, recurring clients

**What to track**: Recommendations made, decisions implemented, outcomes

---

## Related Directories

- `.aget/sessions/` - Session-by-session details
- `.aget/commitments/` - Specific commitments with due dates
- `.aget/context/` - Stable client context (role, preferences)

---

**Specification**: ADVISOR_INTERNAL_STATE_SPEC.md
**Version**: 1.0 (2025-10-10)
