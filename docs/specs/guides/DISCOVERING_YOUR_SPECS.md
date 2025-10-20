# Discovering Your Specifications

> A practical guide to reverse-engineering specifications from existing code

## Why Discover Specifications?

Specifications are the bridge between code and understanding. They help you:
- Understand what a system does (functional requirements)
- Understand why it does it (business rules)
- Understand how it does it (data specs, APIs)
- Communicate with AI agents about your project
- Onboard new team members
- Maintain consistency as code evolves

## The Discovery Process

### Step 1: Initial Reconnaissance (30 minutes)

Start with the big picture:

1. **Run the application** (if possible)
   - What does it do?
   - Who would use it?
   - What problem does it solve?

2. **Read existing documentation**
   - README files
   - Comments in code
   - Test descriptions
   - API documentation

3. **Examine project structure**
   ```bash
   find . -type f -name "*.py" | head -20  # See code organization
   find . -type f -name "*test*" | head -10 # Find tests
   find . -type f -name "*.md" | head -10   # Find docs
   ```

4. **Look for entry points**
   - main() functions
   - CLI commands
   - API routes
   - Event handlers

### Step 2: Functional Requirements Discovery (1-2 hours)

Find out WHAT the system does:

#### Look for User Actions
```python
# Search for function definitions
grep -r "def " --include="*.py" | grep -v "__" | head -20

# Search for API endpoints
grep -r "@app.route\|@router" --include="*.py"

# Search for CLI commands
grep -r "click.command\|argparse" --include="*.py"
```

#### Read Test Files
Tests often reveal requirements:
```python
# Look at test names - they describe behavior
grep -r "def test_" --include="*.py" | head -20

# Look at test assertions - they show expected outcomes
grep -r "assert " --include="*.py" | head -20
```

#### Document in Template
For each discovered function:
```markdown
### FR-00X: [Function Name]
**Description**: [What it does based on code/tests]
**User Story**: As a [user], I want to [action] so that [benefit]
**Acceptance Criteria**:
- [ ] [What tests verify]
- [ ] [What the code ensures]
```

### Step 3: Business Rules Discovery (1-2 hours)

Find out WHY the system behaves as it does:

#### Look for Validation
```python
# Find validation patterns
grep -r "raise\|assert\|validate" --include="*.py"

# Find constraints
grep -r "if.*not\|if.*<\|if.*>" --include="*.py"

# Find magic numbers/constants
grep -r "[0-9]\+\|MAX\|MIN\|LIMIT" --include="*.py"
```

#### Examine Conditionals
```python
# Complex business logic often has comments
grep -r "if.*:.*#" --include="*.py"

# Look for state machines
grep -r "status\|state\|phase" --include="*.py"
```

#### Check Configuration
```python
# Config files reveal business rules
find . -name "*.conf" -o -name "*.ini" -o -name "*.yaml"

# Environment variables
grep -r "os.environ\|getenv" --include="*.py"
```

#### Document in Template
```markdown
### BR-00X: [Rule Name]
**Rule**: [The constraint or policy]
**Rationale**: [Why - from comments or context]
**Example**: [Specific case from code]
```

### Step 4: Data Specifications Discovery (1-2 hours)

Find out HOW data flows:

#### Find Data Models
```python
# Database models
grep -r "class.*Model\|class.*Schema" --include="*.py"

# Data classes
grep -r "@dataclass\|TypedDict\|BaseModel" --include="*.py"

# Database migrations
find . -path "*/migrations/*.py"
```

#### Trace Data Flow
```python
# Input functions
grep -r "request.get\|input()\|read\|load" --include="*.py"

# Output functions
grep -r "response\|print\|write\|save" --include="*.py"

# Transformations
grep -r "map\|filter\|transform\|process" --include="*.py"
```

#### Document in Template
```markdown
### [Entity Name]
**Source**: [Where it comes from]
**Schema**: [Fields and types]
**Transformations**: [What happens to it]
**Destination**: [Where it goes]
```

## Progressive Documentation

### Week 1: Skeleton
- List main functions (FR)
- Note obvious constraints (BR)
- Identify main data types (DS)

### Week 2: Flesh Out
- Add user stories to FRs
- Find rationales for BRs
- Map data relationships

### Week 3: Refine
- Add edge cases
- Document exceptions
- Note missing specs

### Week 4: Complete
- Fill all templates
- Cross-reference specs
- Validate with testing

## Tools to Help

### AGET Discovery Patterns
```bash
# Use AGET patterns to help discover specs
aget apply analysis/discover_endpoints
aget apply analysis/find_validations
aget apply analysis/extract_constants
```

### Questions to Ask

#### For Functional Requirements:
1. Who uses this feature?
2. What triggers it?
3. What's the happy path?
4. What can go wrong?
5. How do we know it worked?

#### For Business Rules:
1. Why is this check here?
2. What happens if we remove it?
3. Where did this number come from?
4. Who decided this policy?
5. When does this not apply?

#### For Data Specifications:
1. Where does this data originate?
2. What format must it be in?
3. How is it validated?
4. Where is it stored?
5. Who can access it?

## Common Patterns to Look For

### Authentication/Authorization
- Who can do what?
- How are permissions checked?
- What requires login?

### Data Validation
- Required fields
- Format constraints
- Range limitations
- Referential integrity

### Business Workflows
- State transitions
- Approval processes
- Notification triggers
- Deadline handling

### Integration Points
- API calls
- File imports/exports
- Message queues
- Database connections

## Red Flags

Watch for these signs of hidden requirements:

1. **Magic numbers without explanation**
   ```python
   if count > 7:  # Why 7?
   ```

2. **Complex conditions without comments**
   ```python
   if (a and b) or (c and not d):  # What rule is this?
   ```

3. **Try/except with silent failures**
   ```python
   try:
       process()
   except:
       pass  # What should happen here?
   ```

4. **Hardcoded values**
   ```python
   url = "https://api.example.com/v1"  # What if this changes?
   ```

## Making It Systematic

### Daily Practice (15 minutes)
1. Pick one function
2. Document its requirements
3. Find one business rule
4. Update templates

### Weekly Review (1 hour)
1. Review discovered specs
2. Look for patterns
3. Fill in gaps
4. Update confidence levels

### Monthly Milestone
1. Calculate coverage %
2. Validate with tests
3. Review with team
4. Plan next month

## When You're Stuck

### No Documentation?
- Read test files
- Check commit messages
- Look for comments
- Examine error messages

### Complex Business Logic?
- Draw a flowchart
- List all conditions
- Find test cases
- Ask "what if?" questions

### Unknown Data Formats?
- Check sample files
- Examine database schema
- Look at API responses
- Review validation code

## Success Metrics

You've successfully discovered specifications when:

- [ ] You can explain what the system does to a newcomer
- [ ] You can predict how it will behave in different scenarios
- [ ] You understand why certain decisions were made
- [ ] You can identify missing or incomplete functionality
- [ ] AI agents can use your specs to help you effectively

---

Remember: Specification discovery is iterative. You don't need perfect documentation on day one. Start with what you can see, and refine as your understanding grows.

*"The code is the truth, but the specifications are the understanding."*