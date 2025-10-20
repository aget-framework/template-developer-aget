# Client Context

**Purpose**: Store persistent client information for personalization and relevance.

**Required for**: All personas (baseline context)

**Depth varies**: Coach/Teacher (detailed), Mentor (moderate), Consultant/Guru (minimal)

---

## File Format

### Naming Convention
```
{client_id}.yaml
```

**Examples**:
- `principal_user.yaml`
- `student_john_doe.yaml`
- `manager_alex.yaml`

---

## File Structure

### Base Template (All Personas)

```yaml
client_id: principal_user
created: 2025-10-01
last_updated: 2025-10-10
persona: coach  # Which advisor persona is serving this client

# Basic identification
name: "[Optional - use client_id if name not shared]"
pronouns: "they/them"  # If shared

# Professional context
role: "Engineering Manager"
company_context: "Series B startup, 50 engineers"
team_size: 8
tenure: "2 years as manager, 6 years at company"

# Current focus
current_challenges:
  - "IC → Manager transition"
  - "Building strategic thinking muscle"
  - "Delegation and trust"

aspirations:
  - "Principal Engineer role"
  - "Influence at staff+ level"

# Communication preferences
preferences:
  communication_style: "Direct, with concrete examples"
  session_frequency: "Weekly"
  feedback_style: "Candid but supportive"
  learning_mode: "Action-oriented, learns by doing"
```

---

## Persona-Specific Extensions

### Coach Context

```yaml
# ... base template ...

# Coaching-specific context
coaching_relationship:
  focus_areas:
    - "Strategic thinking development"
    - "Delegation and trust building"
  coaching_style_preference: "Powerful questions, space for self-discovery"
  response_to_challenge: "Receptive, needs moment to process"
  triggers:
    - "Comparing self to others (imposter syndrome)"
    - "Feeling responsible for everything"

# Development goals
short_term: "Make promotion decision on Sarah with confidence"
medium_term: "Develop strategic thinking practice"
long_term: "Transition to Principal Engineer or Staff role"

# Patterns observed
behavioral_patterns:
  - name: "Seeks concrete answers before trusting intuition"
    first_observed: 2025-10-01
    progress: "Starting to tolerate ambiguity better"

  - name: "Over-involvement in team's technical decisions"
    first_observed: 2025-10-03
    progress: "Delegated first architecture decision successfully"
```

---

### Teacher Context

```yaml
# ... base template ...

# Teaching-specific context
learning_profile:
  prior_experience: "Self-taught HTML/CSS, no formal CS education"
  current_level: "Intermediate Python, beginner OOP"
  learning_goals: "Backend web development with Django"
  timeline: "Job-ready in 6 months"

  strengths:
    - "Visual learner"
    - "Persistent with difficult topics"
    - "Asks clarifying questions"

  challenges:
    - "Needs concrete examples before abstraction"
    - "Rushes through exercises"
    - "Forgets to test understanding before moving on"

  optimal_teaching_approach:
    - "Start with example, then explain concept"
    - "Check comprehension frequently"
    - "Encourage slowing down"

# Curriculum context
completed_topics:
  - "Python basics"
  - "Object-oriented programming"
  - "File I/O and error handling"

current_topic: "Decorators and context managers"

planned_curriculum:
  - "Generators and iterators"
  - "Async/await"
  - "Django fundamentals"
  - "Testing with pytest"
```

---

### Mentor Context

```yaml
# ... base template ...

# Mentoring-specific context
mentoring_relationship:
  career_stage: "Senior Engineer → Staff Engineer transition"
  target_role: "Staff Engineer or Tech Lead"
  timeline: "6-12 months"

  strengths:
    - "Strong technical execution"
    - "Natural mentorship of junior engineers"
    - "System design intuition"

  growth_edges:
    - "Influencing without authority"
    - "Navigating ambiguous problems"
    - "Building cross-team relationships"

  blockers:
    - "Needs more visible cross-team work"
    - "Developing product sense"

# Context for discovery
values: "Craftsmanship, team collaboration, user impact"
career_motivations: "Technical depth + broader influence"
fears: "Losing technical skills, becoming 'just a manager'"
```

---

### Consultant Context

```yaml
# ... base template ...

# Consulting-specific context
engagement_context:
  organization_size: "Series B, 50 engineers"
  domain: "E-commerce platform"
  tech_stack: "Django monolith, React frontend, PostgreSQL"

  current_pain_points:
    - "Deployment coupling across teams"
    - "45-minute CI/CD pipeline"
    - "Merge conflicts slowing velocity"

  decision_context:
    urgency: "Medium - planning Q4 roadmap"
    constraints:
      - "Limited budget for infrastructure changes"
      - "Can't afford major rewrites"
      - "Need incremental improvements"

  stakeholders:
    - "VP Engineering (decision maker)"
    - "5 engineering managers (executors)"
    - "CTO (final approval)"

# Recommendations history
previous_recommendations:
  - date: 2025-10-10
    topic: "Microservices vs modular monolith"
    recommendation: "Modular monolith with clear boundaries"
    status: "Under consideration"
```

---

### Guru Context

```yaml
# ... base template ...

# Expertise-specific context
expertise_sought:
  - "SOLID principles application"
  - "Design patterns in modern contexts"
  - "Functional programming vs OOP trade-offs"

knowledge_level: "Intermediate (3-5 years experience)"

philosophical_questions:
  - "When to apply principles vs when to bend them?"
  - "How does functional programming change classical patterns?"

learning_preference: "Deep dives, historical context, underlying reasoning"
```

---

## Creation Protocol

### When to Create

**First session**: Create client context file with basic information.

**Information sources**:
- What client shares directly
- Observable from interaction style
- Inferred from questions and concerns (mark as "observed, not confirmed")

---

### Initial Creation

```python
# At end of first session (wind down)
Write: .aget/context/{client_id}.yaml

# Populate with:
# - Basic identification (role, team, challenges)
# - Initial preferences (if observed)
# - First impressions (behavioral patterns)
```

---

## Update Protocol

### When to Update

**Update frequency**:
- Coach/Teacher: Every 3-5 sessions (high context dependency)
- Mentor: When significant context changes (role change, new goals)
- Consultant: When engagement scope shifts
- Guru: Rarely (static context)

**What triggers update**:
- Client shares new information ("I got promoted")
- Preferences become clear ("I realize I need more direct feedback")
- Patterns observed over multiple sessions
- Goals shift

---

### How to Update

```python
# During or after session (when context learned)
Edit: .aget/context/{client_id}.yaml

# Add or update fields:
# - New current_challenges
# - Refined communication_style
# - Updated role or team_size
# - New behavioral_pattern observed
```

---

## Usage Protocol

### At Wake Up

**Load context automatically** (silent):
- Know client's role, challenges, preferences
- Tailor communication style
- Prepare relevant examples

**Display if helpful**:
```
📍 Context: Engineering Manager, 8-person team
🎯 Focus: Strategic thinking development
```

---

### During Session

**Personalize guidance**:
- Use client's domain for examples
- Reference their stated challenges
- Adapt to communication preferences

**Example**:
```
# Generic advice (no context)
"Delegation requires trust."

# Personalized advice (with context)
"You mentioned your team is 8 engineers. At that scale, you can't
 be involved in every decision. Sarah's architecture review is a
 perfect delegation opportunity - she's senior enough, and you've
 been wanting to test her strategic thinking anyway."
```

---

### When Context Changes

**Acknowledge and update**:
```
User: "I got promoted to Senior Manager last week."

Advisor: "Congratulations! That's a significant shift.
          Let me update your context - you're now managing how many
          people? And has your focus changed from IC transition to
          something else?"

[Updates role, team_size, aspirations in context file]
```

---

## Privacy & Sensitivity

**Data classification**: Highly sensitive (career aspirations, fears, personal patterns)

**Access control**: Advisor agent only (never shared externally)

**Retention**: Duration of relationship + 90 days

**Deletion**: When relationship ends, client can request deletion

**Transparency**: Client should know what context is being tracked. If asked, share the context file.

---

## Anti-Patterns

### ❌ Recording Too Much (Overwriting Boundaries)

**Bad**:
```yaml
personal_life:
  relationship_status: "Married"
  children: 2
  hobbies: "Rock climbing"
  mental_health: "Struggles with anxiety"
```

**Why it fails**: Crosses professional boundary unless client explicitly shares for relevant reason.

**Good**: Only record professional context unless personal context directly impacts professional development (e.g., "Balancing parenting and principal role" is relevant).

---

### ❌ Recording Without Evidence

**Bad**:
```yaml
behavioral_patterns:
  - "Avoids conflict"  # Inferred from one observation
  - "Lacks confidence"  # Assumed, not validated
```

**Why it fails**: One data point isn't a pattern. Labeling can harm.

**Good**: Wait for pattern (3+ observations) or mark as hypothesis.
```yaml
observed_once_not_yet_pattern:
  - "Hesitated on decision in 2025-10-10 session (conflict with peer)"
  - "Need more data to determine if this is pattern or situational"
```

---

### ❌ Not Updating Context

**Bad**:
```yaml
# Context created 2025-08-01, never updated
role: "Senior Engineer"  # Client is now Staff Engineer
aspirations: "Tech Lead"  # Client achieved, now wants Principal
```

**Why it fails**: Stale context leads to irrelevant guidance.

**Good**: Update context when changes happen or patterns become clear.

---

## Related Directories

- `.aget/sessions/` - Session-specific details
- `.aget/client_progress/` - Development over time
- `.aget/commitments/` - Active accountability items

**Relationship**: Context is persistent (slow-changing), sessions are ephemeral (per-conversation), progress is developmental (trends over time).

---

**Specification**: ADVISOR_INTERNAL_STATE_SPEC.md
**Version**: 1.0 (2025-10-10)
