# Session History

**Purpose**: Track advisor sessions for continuity across conversations.

**Required for**: All personas

---

## File Format

### Naming Convention
```
SESSION_YYYY-MM-DD_HH-MM.md
```

**Examples**:
- `SESSION_2025-10-10_14-00.md` (session started at 2:00 PM)
- `SESSION_2025-10-11_09-30.md` (session started at 9:30 AM)

---

## File Structure

```yaml
---
session_date: YYYY-MM-DD
session_start: YYYY-MM-DDTHH:MM:SS+TZ
session_end: YYYY-MM-DDTHH:MM:SS+TZ
duration_minutes: <number>
client_id: <string>
agent: <agent_name>
agent_version: <version>
persona: <teacher|mentor|consultant|guru|coach>
exchanges: <number>
---

# Session Summary

## Topic
[What was discussed]

## Key Insights / What We Explored
[Main points covered, client realizations, progress]

## Commitments (if any)
[What client committed to do, with due dates]

## Next Session
[What to explore next, follow-up items]
```

---

## Persona-Specific Content

### Coach
```markdown
## Topic
Promotion decision: Sr Engineer → Principal

## What We Explored
• Technical strength vs strategic thinking gap
• Specific concerns about readiness
• Client's underlying fear of setting Sarah up to fail

## Client's Insights
• Realized they're conflating strategic thinking with strategic communication
• Noticed they haven't actually observed Sarah in strategic contexts
• Recognized need to test assumption before making decision

## Commitment Made
"I'll observe Sarah in next week's architecture review and note specific
 moments of strategic thinking or gaps."

Due: 2025-10-17

## Next Session
• Follow up on observation
• Explore: What does strategic thinking look like for Principal role?
• If observation complete: Discuss decision criteria
```

### Teacher
```markdown
## Topic
Python decorators - Understanding and application

## Concepts Covered
1. First-class functions (functions as objects)
2. Closure (inner functions accessing outer scope)
3. Decorator syntax (@decorator)
4. Common use cases (logging, timing, validation)

## Student Understanding
- Grasped concept quickly (8/10 comprehension)
- Struggled with closure initially, clicked after 2nd example
- Successfully wrote simple timing decorator

## Homework
Practice exercises: Write 3 decorators
1. @retry (retry failed operations)
2. @validate_input (check function arguments)
3. @cache (memoization)

## Next Session
- Review homework
- Introduce decorator with arguments
- Teach class-based decorators
```

### Mentor
```markdown
## Topic
Career growth: IC Engineer → Tech Lead transition

## What We Explored
- Current strengths (technical execution, mentorship)
- Growth edges (influencing without authority, prioritization)
- Fears about transition (losing technical skills, imposter syndrome)

## Reflections
- Recognized pattern: Saying yes to everything = no time for strategic work
- Insight: "I've been managing tasks, not outcomes"
- Commitment: Start saying no to 1 request this week

## Growth Areas
1. Delegation (currently 2/10, target 6/10)
2. Strategic communication (currently 5/10, target 8/10)

## Next Session
- Debrief saying-no experiment
- Explore: What does "strategic" mean in practice?
```

### Consultant
```markdown
## Topic
Microservices vs Monolith decision

## Analysis Presented
**Current state**: Django monolith, 5 teams, 200k LOC
**Pain points**: Deployment coupling, slow CI/CD (45 min), merge conflicts
**Options**: Microservices, modular monolith, service-oriented monolith

## Recommendation
Modular monolith with clear boundaries
- Pros: Refactor incrementally, keep deployment simple, lower risk
- Cons: Doesn't solve all coupling (still one deployment)
- Timeline: 3-6 months to establish boundaries

## Questions to Resolve
1. Team autonomy priority (high/medium/low)?
2. Deployment frequency target (daily/weekly)?
3. Investment capacity (20%/50% team time)?

## Next Session
- User answers questions above
- Refine recommendation based on priorities
- Discuss implementation roadmap if approved
```

### Guru
```markdown
## Topic
SOLID principles - When to apply vs when to bend

## Principles Discussed
1. Single Responsibility: "One reason to change"
2. Open/Closed: Extension without modification
3. Liskov Substitution: Behavioral compatibility
4. Interface Segregation: Narrow, focused interfaces
5. Dependency Inversion: Depend on abstractions

## Deep Dives
- Why SOLID emerged (managing change in large systems)
- Historical context (Java/C# enterprise, 2000s)
- Modern critique (functional programming challenges, over-engineering)

## When to Bend
- Early prototyping (too early to know responsibilities)
- Small systems (<5k LOC, single developer)
- Performance-critical paths (abstraction overhead)

## Core Wisdom
"Principles are guides, not laws. The real skill is knowing when
 they apply and when they don't."

## Next Session
- Explore: Design patterns that embody SOLID
- Discuss: How functional programming changes the game
```

---

## Creation Protocol

**When**: Automatically at wind down

**How**:
1. Advisor constructs session summary during wind down
2. Uses Write tool to create `.aget/sessions/SESSION_{date}_{time}.md`
3. Populates YAML frontmatter with session metadata
4. Writes persona-specific markdown body

**Example**:
```python
# Wind down protocol - automatic
Write: .aget/sessions/SESSION_2025-10-10_14-00.md
content: session_summary_with_frontmatter
```

---

## Usage Protocol

### At Wake Up
1. Check for last session file (most recent by filename)
2. Display: "Last session: {date} ({days} ago)"
3. Load context if needed for persona (coach: commitments, teacher: concepts covered)

### During Session
- Reference previous sessions if client mentions past topics
- Track continuity: "Last time you mentioned..."

### At Wind Down
- Create new session file automatically
- Reference: Do NOT ask permission (advisor has write access to .aget/**)

---

## File Maintenance

**Retention**: Keep all session files (no automatic deletion)

**Organization**: Chronological by filename (YYYY-MM-DD_HH-MM.md sorts correctly)

**Privacy**: Session files contain client information - treat as sensitive

**Backup**: Include in version control (.aget/ is committed)

---

## Related Directories

- `.aget/commitments/` - Extracted commitments from sessions
- `.aget/client_progress/` - Aggregate progress over time
- `.aget/context/` - Persistent client context learned across sessions

---

**Specification**: ADVISOR_INTERNAL_STATE_SPEC.md
**Version**: 1.0 (2025-10-10)
