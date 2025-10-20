# Incremental Plan: AGET Specification Templates

## Overview
Transform AGET specifications from "framework documentation" to "user discovery templates" through incremental phases.

## Phase 1: Template Conversion (Day 1 - Today)
**Goal**: Convert existing specs to fill-in templates

### Step 1.1: Create templates directory
```bash
mkdir -p docs/specs/templates
mkdir -p docs/specs/examples
mkdir -p docs/specs/guides
```

### Step 1.2: Transform FUNCTIONAL_REQUIREMENTS.md
**From**: Detailed AGET requirements
**To**: Template with prompts

```markdown
# [PROJECT NAME] Functional Requirements

## Core Functionality
<!-- What must your system do? -->

### FR-001: [Primary Function]
**Description**: <!-- What is the main thing your system does? -->
**Trigger**: <!-- How is this initiated? -->
**Success Criteria**:
- <!-- How do you know it worked? -->

### FR-002: [Secondary Function]
<!-- Copy this block for each major function -->
```

### Step 1.3: Transform BUSINESS_RULES.md
**From**: 25 AGET-specific rules
**To**: Categories with prompts

```markdown
# [PROJECT NAME] Business Rules

## Data Rules
<!-- How should data be handled? -->

### BR-001: [Data Validation Rule]
**Rule**: <!-- What must always be true about your data? -->
**Example**: <!-- Show a specific case -->

## Safety Rules
<!-- What operations must be prevented? -->

## Performance Rules
<!-- What performance constraints exist? -->
```

### Step 1.4: Add specification guide
Create `docs/specs/guides/DISCOVERING_YOUR_SPECS.md`:
- How to analyze existing code
- Questions to ask yourself
- Where to look for hidden rules
- How to document discoveries

**Deliverable**: Empty templates users can fill in

---

## Phase 2: Discovery Patterns (Day 2)
**Goal**: Create tools to help users find their specifications

### Step 2.1: Create analysis patterns
```
patterns/analysis/
├── discover_endpoints.py    # Find API endpoints → FR docs
├── find_validations.py      # Find validation → BR docs
├── extract_constants.py     # Find magic numbers → BR docs
├── identify_patterns.py     # Find repeated code → Templates
└── README.md                # How to use these tools
```

### Step 2.2: Create specification generator
```python
# patterns/analysis/generate_spec.py
def generate_functional_spec(project_path):
    """Analyze code and generate draft FUNCTIONAL_REQUIREMENTS.md"""
    # 1. Find all public functions
    # 2. Group by module/class
    # 3. Generate FR entries
    # 4. Add TODO comments for human review
```

### Step 2.3: Create "spec evolution" example
Show how a spec grows:
```
examples/spec_evolution/
├── day_001_empty.md        # Starting template
├── day_007_discovered.md    # After initial analysis
├── day_030_refined.md       # After understanding
├── day_090_complete.md      # Fully documented
└── README.md                # The journey explained
```

**Deliverable**: Tools that help users discover their specs

---

## Phase 3: Minimal Examples (Day 3)
**Goal**: Provide just enough examples without overwhelming

### Step 3.1: Create micro-examples
```
docs/specs/examples/
├── cli_tool/
│   ├── FUNCTIONAL_REQUIREMENTS.md  # 3-4 simple FRs
│   └── README.md                    # "For command-line tools"
├── data_analysis/
│   ├── DATA_SPECIFICATIONS.md      # Schema example
│   └── README.md                    # "For data projects"
├── web_api/
│   ├── API_SPECIFICATIONS.md       # 2-3 endpoints
│   └── README.md                    # "For REST APIs"
└── README.md                        # "Pick your project type"
```

### Step 3.2: Keep AGET's own specs minimal
Move detailed AGET specs to aget-aget, keep only:
- 2-3 example requirements
- 2-3 example business rules
- Clear note: "See aget-aget for complete reference"

**Deliverable**: Small, digestible examples

---

## Phase 4: Reference Implementation in aget-aget (Day 4-5)
**Goal**: Create rich reference in private repo

### Step 4.1: Copy current detailed specs to aget-aget
```bash
# In aget-aget repo
cp ../aget-cli-agent-template/docs/specs/*.md docs/specs/
# These become the full AGET framework specs
```

### Step 4.2: Add meta-specifications
Create in aget-aget:
- `META_SPECIFICATIONS.md` - How aget-aget manages projects
- `PROJECT_GOVERNANCE.md` - How we handle multiple projects
- `SPECIFICATION_STANDARDS.md` - How we write specs

### Step 4.3: Document real project specs
```
projects/spotify-aget/specs/
├── DATA_SCHEMA.md           # Actual Spotify data structure
├── ANALYSIS_PATTERNS.md     # Real queries we run
├── PRIVACY_BOUNDARIES.md    # What we don't analyze
└── EVOLUTION_HISTORY.md     # How these specs grew
```

**Deliverable**: Complete reference implementation

---

## Phase 5: Documentation & Integration (Day 6)
**Goal**: Tie it all together

### Step 5.1: Update main README
Add section: "Understanding Your Project with AGET"
- Specification-first development
- Progressive understanding
- Links to templates and guides

### Step 5.2: Create pattern for spec checking
```python
# patterns/analysis/check_specs.py
def check_specification_coverage():
    """Compare code to specs, find gaps"""
    # What's documented vs what exists
    # What's specified but not implemented
    # What's implemented but not specified
```

### Step 5.3: Add to standard templates
Update template configurations:
```yaml
# templates/agent/config.yaml
includes:
  - specs/templates/*
  - patterns/analysis/*
```

**Deliverable**: Integrated specification workflow

---

## Phase 6: Testing & Refinement (Day 7)
**Goal**: Validate the approach

### Step 6.1: Test on real project
1. Take an unknown codebase
2. Use templates to document it
3. Note friction points
4. Refine templates

### Step 6.2: Create tutorial
`docs/tutorials/REVERSE_ENGINEERING_WITH_AGET.md`:
1. Starting with unknown code
2. Running discovery patterns
3. Filling in templates
4. Growing specifications
5. Managing with AGET

### Step 6.3: Get feedback
- Test with a new user
- Document confusion points
- Refine templates and guides

**Deliverable**: Validated, tested approach

---

## Success Metrics

### Phase 1 Success
- [ ] Templates are clear and inviting
- [ ] No overwhelming detail
- [ ] Clear prompts guide users

### Phase 2 Success
- [ ] Discovery tools find real specs
- [ ] Generated drafts are useful starting points
- [ ] Evolution example is compelling

### Phase 3 Success
- [ ] Examples are minimal but helpful
- [ ] Different project types covered
- [ ] Users can find relevant example

### Phase 4 Success
- [ ] aget-aget has complete specs
- [ ] Real project examples exist
- [ ] Reference implementation is clear

### Phase 5 Success
- [ ] Workflow is integrated
- [ ] Documentation is cohesive
- [ ] Pattern works end-to-end

### Phase 6 Success
- [ ] Tested on real project
- [ ] Tutorial is clear
- [ ] New user can follow process

---

## Timeline

- **Today**: Phase 1 (Templates)
- **Tomorrow**: Phase 2 (Discovery)
- **Day 3**: Phase 3 (Examples)
- **Day 4-5**: Phase 4 (Reference)
- **Day 6**: Phase 5 (Integration)
- **Day 7**: Phase 6 (Testing)

Total: One week to transform AGET's specification approach

---

## Risk Mitigation

### Risk: Users confused by empty templates
**Mitigation**: Provide clear guide and small examples

### Risk: Discovery tools miss important specs
**Mitigation**: Tools are aids, not replacements for thinking

### Risk: Reference too complex
**Mitigation**: Clear separation between template and reference

### Risk: Breaking existing users
**Mitigation**: Keep backward compatibility, gradual transition

---

This incremental approach transforms AGET from a framework with specs to a framework that helps users discover and document their own specifications.