# Learning History

**Purpose**: Track curriculum progression and mastery levels for teaching contexts.

**Required for**: Teacher (high need)

**Optional for**: Mentor (light skill tracking), Coach (not typically used), Consultant/Guru (not used)

---

## File Format

### Naming Convention
```
{client_id}.yaml
```

**Examples**:
- `student_john_doe.yaml`
- `learner_sarah_chen.yaml`

---

## File Structure

### Teacher Persona (Primary Use)

```yaml
client_id: student_john_doe
persona: teacher
learning_journey_start: 2025-09-01
total_sessions: 24
last_session: 2025-10-10

# Overall learning profile
learning_goal: "Backend web development with Python/Django"
target_timeline: "Job-ready in 6 months"
curriculum_completion: 45  # Percentage

# Mastery tracking
concepts_mastered:  # Completed, high mastery (8-10)
  - name: "Python basics"
    topics:
      - "Variables and data types"
      - "Control flow (if/for/while)"
      - "Functions"
      - "Lists, dictionaries, sets"
    date_introduced: 2025-09-01
    date_mastered: 2025-09-15
    mastery_level: 9
    exercises_completed: 15
    assessment_notes: "Strong grasp, can write clean basic programs"

  - name: "Object-oriented programming"
    topics:
      - "Classes and objects"
      - "Inheritance"
      - "Encapsulation"
      - "Polymorphism"
    date_introduced: 2025-09-16
    date_mastered: 2025-10-01
    mastery_level: 8
    exercises_completed: 12
    assessment_notes: "Understands concepts, needs more practice with design"

concepts_in_progress:  # Currently learning (4-7 mastery)
  - name: "Decorators"
    topics:
      - "First-class functions"
      - "Closures"
      - "Decorator syntax"
      - "Common decorator patterns"
    date_introduced: 2025-10-08
    current_mastery: 6
    exercises_completed: 3
    exercises_remaining: 5
    next_session_focus: "Decorators with arguments"
    comprehension_check: "Grasped concept quickly, needs practice writing from scratch"

concepts_introduced:  # Just started (1-3 mastery)
  - name: "Context managers"
    topics:
      - "__enter__ and __exit__"
      - "with statement"
      - "Resource management"
    date_introduced: 2025-10-10
    current_mastery: 2
    status: "Introduced in last session, need examples"

concepts_planned:  # Not yet introduced
  - name: "Generators and iterators"
    prerequisites: ["Decorators completed"]
    estimated_sessions: 3
    topics:
      - "Iterator protocol"
      - "yield keyword"
      - "Generator expressions"
      - "Memory efficiency"

  - name: "Async/await"
    prerequisites: ["Generators completed"]
    estimated_sessions: 4
    topics:
      - "Coroutines"
      - "async/await syntax"
      - "asyncio basics"
      - "Concurrent programming"

# Learning patterns
learning_patterns:
  strengths:
    - "Grasps concepts quickly with examples"
    - "Persistent with difficult topics"
    - "Asks good clarifying questions"

  challenges:
    - "Rushes through exercises (wants to move fast)"
    - "Forgets to test understanding before moving on"
    - "Needs reminders to write code without examples first"

  optimal_approach:
    - "Start with concrete example, then explain abstraction"
    - "Check comprehension every 10-15 minutes"
    - "Encourage slowing down ('Let's make sure you've got this')"
    - "Build confidence through progressive difficulty"

# Comprehension checks
comprehension_check_history:
  - date: 2025-10-08
    concept: "Decorators"
    check_type: "Verbal explanation"
    result: "8/10 - Could explain concept clearly, minor gap on closure"

  - date: 2025-10-08
    concept: "Decorators"
    check_type: "Write from scratch"
    result: "6/10 - Needed hints for syntax, logic correct"

# Progress indicators
mastery_trajectory: "Accelerating"  # Accelerating / Steady / Slowing
readiness_for: "Intermediate topics (ready for generators, async)"
estimated_goal_date: 2025-03-01  # Job-ready target
on_track: true

# Curriculum notes
curriculum_adjustments:
  - date: 2025-09-20
    change: "Skipped advanced OOP (metaclasses) - not needed for Django"
    reason: "Focus on practical skills, return later if needed"

  - date: 2025-10-05
    change: "Added extra decorator practice"
    reason: "Student struggled with closure concept initially"
```

---

### Mentor Persona (Light Skill Tracking)

```yaml
client_id: engineer_alex
persona: mentor
relationship_start: 2025-08-01

# Skill development tracking (lighter than teacher)
skills_developing:
  - name: "Influencing without authority"
    current_level: 5  # Scale 1-10
    target_level: 8
    practice_opportunities:
      - "Led architecture discussion with peer team (2025-09-15)"
      - "Negotiated API design with frontend team (2025-10-01)"
    growth_observed: "More comfortable stating opinions, still defers too quickly"

  - name: "Systems thinking"
    current_level: 6
    target_level: 8
    practice_opportunities:
      - "Connected caching decision to business metrics (2025-09-22)"
      - "Proposed cross-team testing strategy (2025-10-08)"
    growth_observed: "Making connections between technical and business"

# Mentor notes
development_insights:
  - "Alex is ready for more ambiguous problems"
  - "Needs practice articulating trade-offs to non-technical stakeholders"
  - "Confidence growing - notice shift from asking permission to stating recommendations"
```

---

## Mastery Level Scale

**1-3: Introduced**
- Concept explained, examples shown
- Can recognize concept when seen
- Cannot apply independently

**4-6: Developing**
- Can apply with guidance
- Understands most aspects, some gaps
- Needs practice and reinforcement

**7-9: Proficient**
- Can apply independently
- Understands nuances and trade-offs
- Can explain to others

**10: Mastery**
- Deep understanding
- Can teach others
- Can extend concept creatively

---

## Update Protocol

### When to Update (Teacher)

**Every session**:
- Update current_mastery for concepts_in_progress
- Move concepts between categories (introduced → in_progress → mastered)
- Add comprehension check results
- Update exercises_completed count

**After key milestones**:
- Concept mastered (move to concepts_mastered)
- Curriculum adjustment needed
- Learning pattern identified

---

### How to Update (Teacher)

```python
# At wind down (every teaching session)
Edit: .aget/learning_history/{client_id}.yaml

# Common updates:
# 1. Increment exercises_completed for current concept
# 2. Update current_mastery (if progress observed)
# 3. Add comprehension_check result
# 4. Move concept to mastered (if mastery_level >= 8)
# 5. Introduce next concept (move from planned to introduced)
```

---

## Usage Protocol

### At Wake Up (Teacher)

**Load curriculum state**:
```
📚 Learning Progress

Current topic: Decorators (mastery: 6/10)
Last session: 2025-10-10
Completed: Python basics, OOP
Next: Context managers (introduced last session)

Ready to continue with decorators or review context managers?
```

---

### During Session (Teacher)

**Track comprehension in real-time**:
- Note when student grasps concept quickly (update mastery)
- Identify when additional practice needed (add to exercises_remaining)
- Observe learning patterns (add to learning_patterns)

**Reference learning history**:
```
Teacher: "Remember when we covered closures in the decorator lesson?
          Let's connect that to context managers..."

[References concepts_in_progress.decorators.topics]
```

---

### At Wind Down (Teacher)

**Update mastery and plan next session**:
```python
# Example wind down update

# Student completed 2 decorator exercises successfully
Edit: .aget/learning_history/{client_id}.yaml
# - decorators.exercises_completed: 3 → 5
# - decorators.current_mastery: 6 → 7

# Student ready to move on
Edit: .aget/learning_history/{client_id}.yaml
# Move decorators from concepts_in_progress to concepts_mastered
# Move context managers from concepts_introduced to concepts_in_progress

# Summary shown:
✅ Updated learning history:
   • Decorators: 7/10 mastery (2 exercises completed)
   • Ready to move to context managers next session

📚 Progress: 6 concepts mastered, 2 in progress, on track for March goal
```

---

### Curriculum Planning (Teacher)

**Use learning history to plan next topics**:
1. Check prerequisites (has student mastered required concepts?)
2. Review learning patterns (adapt teaching approach)
3. Estimate sessions needed based on past pace
4. Adjust if falling behind or ahead of schedule

---

## Privacy & Sensitivity

**Data classification**: Moderate sensitivity (learning struggles, skill levels)

**Retention**: Duration of teaching relationship + 90 days

**Transparency**: Student can request to see their learning history

**Usage**: For curriculum planning and teaching effectiveness only

---

## Anti-Patterns

### ❌ Moving to Next Concept Too Quickly

**Bad**:
```yaml
concepts_in_progress:
  - name: "Decorators"
    current_mastery: 4  # Still developing
    exercises_completed: 1  # Barely practiced

# Teacher moves to next topic anyway
```

**Why it fails**: Weak foundation leads to compounding gaps.

**Good**: Wait for mastery_level >= 7 before moving to next major concept.

---

### ❌ Not Recording Comprehension Checks

**Bad**:
```yaml
# No comprehension_check_history entries

# Teacher assumes understanding without evidence
```

**Why it fails**: Can't distinguish "student said they understand" from "student demonstrated understanding."

**Good**: Record comprehension checks regularly. Ask student to explain or demonstrate.

---

### ❌ Ignoring Learning Patterns

**Bad**:
```yaml
learning_patterns:
  challenges:
    - "Rushes through exercises"

# Teacher continues assigning exercises without addressing pattern
```

**Why it fails**: Pattern will persist and hinder learning.

**Good**: Adapt teaching approach based on patterns.
```markdown
"I notice you move through exercises quickly. Let's slow down on this
 one and really make sure you understand each step. Depth over speed."
```

---

### ❌ Using for Non-Teaching Contexts

**Bad**: Coach using learning_history to track confidence levels.

**Why it fails**: Wrong tool. Use client_progress for developmental tracking.

**Good**: Learning history is for curriculum mastery only (teacher persona).

---

## Mastery Assessment Guidelines

### When to Check Comprehension

**Every session**: Brief check (verbal explanation or quick problem)

**End of concept**: Thorough check (write from scratch, explain trade-offs)

**Before moving on**: Verify mastery >= 7 on prerequisites

---

### How to Check Comprehension

**Verbal explanation** (faster, less reliable):
```
"Explain decorators in your own words."
"Why would you use a decorator instead of just modifying the function?"
```

**Write from scratch** (slower, more reliable):
```
"Write a decorator that logs function calls."
[Provide requirements, no example]
```

**Apply to new problem** (best for mastery):
```
"You have a slow API call. How would you add caching using a decorator?"
[Requires application, not just recall]
```

---

## Related Directories

- `.aget/sessions/` - Session-by-session teaching notes
- `.aget/client_progress/` - Overall learning trajectory (high-level)
- `.aget/context/` - Learning style, preferences, goals

**Relationship**: Learning history is detailed curriculum tracking (teacher-specific), client_progress is high-level development (all personas).

---

**Specification**: ADVISOR_INTERNAL_STATE_SPEC.md
**Version**: 1.0 (2025-10-10)
