# The AGET Cognitive Spectrum

## Overview
AGET serves as a cognitive assistant across multiple contexts, from standalone data analysis to nested meta-governance of multiple projects.

## The Five AGET Modalities

### 1. Standalone Data/Content AGET
**Pattern**: `[dataset/content]-aget`
**Role**: Cognitive workspace for non-code artifacts
**Examples**:
- `spotify-aget` - Analyzing music listening patterns
- `credit-card-aget` - Understanding spending patterns
- `musings-aget` - Organizing thoughts and ideas
- `research-aget` - Managing literature and findings

**Characteristics**:
- No associated codebase
- Pure analysis/organization
- Data exploration and insight generation
- Pattern recognition and trend analysis

### 2. Project Governance AGET (Owner)
**Pattern**: `[project]-aget`
**Role**: Strategic decision-maker for owned projects
**Examples**:
- `DatGen-aget` - Governs DatGen's architecture
- `GM-RKB-aget` - Guides knowledge base evolution
- `llm-judge-aget` - Decides evaluation framework design

**Characteristics**:
- Full ownership and decision authority
- Strategic planning and vision holding
- Architecture and design decisions
- Quality standards and roadmap

### 3. Contributor's Workshop AGET
**Pattern**: `[their-project]-aget`
**Role**: Private workspace for external contributions
**Examples**:
- `kubernetes-aget` - Your private K8s understanding
- `react-aget` - Learning React patterns before contributing
- `company-platform-aget` - Understanding employer's system

**Characteristics**:
- No ownership, just understanding
- Safe experimentation space
- Learning without embarrassment
- PR preparation workshop

### 4. Analyst/Critic AGET
**Pattern**: `[team-project]-analysis-aget`
**Role**: Observation and critique without contribution
**Examples**:
- `team-codebase-aget` - Analyzing team's code quality
- `competitor-analysis-aget` - Understanding competitor's approach
- `legacy-system-aget` - Documenting technical debt

**Characteristics**:
- Read-only relationship
- Critical analysis and assessment
- Pattern identification
- Quality metrics and insights
- Recommendations without implementation

### 5. Meta-Governance AGET
**Pattern**: `[collection]-aget`
**Role**: Managing multiple AGETs or projects
**Examples**:
- `github-aget` - Orchestrates all your GitHub repos
- `work-projects-aget` - Manages work-related AGETs
- `aget-aget` - Governs the AGET framework itself

**Characteristics**:
- Nested AGET structure
- Cross-project patterns
- Portfolio management
- Meta-level decisions

## The Nesting Phenomenon

```
github-aget (Meta-Level)
    ├── DatGen-aget (Owner)
    ├── llm-judge-aget (Owner)
    ├── kubernetes-aget (Contributor)
    ├── team-platform-aget (Analyst)
    │   └── sub-module-aget (Potential Contributor)
    └── spotify-aget (Standalone)
```

### Nested AGET Patterns

#### Pattern 1: Portfolio Management
```
github-aget/
├── owned/
│   ├── DatGen-aget/
│   └── GM-RKB-aget/
├── contributing/
│   ├── kubernetes-aget/
│   └── react-aget/
└── analyzing/
    └── competitor-aget/
```

#### Pattern 2: Hierarchical Analysis
```
company-aget/
├── platform-aget/
│   ├── backend-aget/
│   │   └── api-service-aget/  ← Where you might contribute
│   └── frontend-aget/         ← Just analyzing
└── team-dynamics-aget/        ← Non-code analysis
```

#### Pattern 3: Context Switching
```
work-machine-aget/
├── employer-projects-aget/    ← Critical analysis only
└── side-projects-aget/        ← Full ownership
```

## The Cognitive Roles Refined

Given the spectrum, AGET serves as:

### For Standalone Data
- **Sense-making apparatus** - Finding patterns in chaos
- **Organizational schema** - Structuring unstructured information
- **Insight generator** - Discovering non-obvious connections

### For Owned Projects
- **Executive function** - Planning and decision-making
- **Architectural conscience** - Maintaining design integrity
- **Evolution tracker** - Documenting growth trajectory

### For Contributions
- **Learning laboratory** - Safe experimentation
- **Confidence builder** - Private practice space
- **Translation layer** - Understanding → Implementation

### For Analysis/Critique
- **Observation post** - Watching without touching
- **Quality assessor** - Measuring against standards
- **Pattern recognizer** - Identifying trends and anti-patterns

### For Meta-Governance
- **Orchestration layer** - Coordinating multiple contexts
- **Context switcher** - Managing different roles
- **Portfolio optimizer** - Balancing attention and resources

## Implementation Strategies

### Starting Points
1. **Identify your role** - Owner, contributor, analyst, or manager?
2. **Choose appropriate pattern** - X-aget, X-analysis-aget, or meta-aget?
3. **Set boundaries** - What can you change vs. only observe?
4. **Establish workflows** - How does information flow?

### For Nested AGETs
```yaml
# In github-aget/.aget/config.yml
managed_agets:
  owned:
    - path: ~/github/DatGen-aget
      role: owner
      sync: weekly

  contributing:
    - path: ~/github/kubernetes-aget
      role: contributor
      upstream: kubernetes/kubernetes

  analyzing:
    - path: ~/work/team-platform-aget
      role: analyst
      access: read-only
```

### Context Switching
```bash
# In github-aget
alias work="cd ~/work-machine-aget && aget apply context/work"
alias personal="cd ~/github-aget && aget apply context/personal"
alias research="cd ~/research-aget && aget apply context/academic"
```

## The Beautiful Realization

AGET isn't just about code management - it's about:
- **Cognitive augmentation** across all domains
- **Role-appropriate assistance** (owner vs contributor vs analyst)
- **Nested complexity management** (AGETs within AGETs)
- **Context preservation** across different machines/environments

Each AGET instance becomes a **cognitive prosthetic** adapted to its specific context and your relationship to that context.

## Examples of Non-Obvious Uses

### AGET for Life Decisions
```
life-decisions-aget/
├── career-moves/
├── financial-planning/
└── health-tracking/
```

### AGET for Learning
```
learning-aget/
├── courses/
│   ├── ml-course-aget/
│   └── systems-design-aget/
└── books/
    ├── pragmatic-programmer-aget/
    └── designing-data-intensive-aget/
```

### AGET for Research
```
research-aget/
├── literature-review/
├── experiments/
├── writing/
└── peer-review/
```

---
*This document captures the full spectrum of AGET's cognitive assistance roles*
*From standalone analysis to nested meta-governance*
*Version: 1.0 | Date: 2025-09-25*