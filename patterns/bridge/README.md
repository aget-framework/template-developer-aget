# Bridge Patterns

Bridge patterns enable the transformation of private agent outputs into public Outputs (products) that provide value to the community.

## Core Concept

The bridge represents the critical transformation point where:
- **outputs/** (lowercase) = Agent's private workspace for exploration and experimentation
- **Outputs/** (uppercase) = Public products the agent creates and maintains for others

## Available Patterns

### extract_output.py
Identifies valuable outputs from an agent's workspace and prepares them for public release.

**Features:**
- Scans outputs/ directory for valuable content
- Calculates value scores based on size, recency, documentation, and tests
- Transforms private naming to public-friendly names
- Creates extraction manifests for traceability
- Records extractions in .aget/evolution/

**Usage:**
```bash
# Scan for valuable outputs
python3 patterns/bridge/extract_output.py

# Or via aget (when integrated)
aget apply bridge
```

## How Bridges Work

1. **Discovery Phase**
   - Agent explores and creates in outputs/
   - Pattern recognition identifies valuable outputs
   - Value scoring prioritizes candidates

2. **Extraction Phase**
   - Selected outputs are transformed
   - Private names become public names
   - Manifests track the transformation

3. **Publication Phase**
   - Outputs become standalone products
   - Community can use without knowing origin
   - Agent maintains the Output over time

## Value Scoring

Outputs are scored based on:
- **Size**: Substantial content (not trivial)
- **Recency**: Recently modified (actively used)
- **Documentation**: Has README or docs
- **Tests**: Has test coverage
- **Uniqueness**: Not generic/boilerplate

## Transformation Rules

### Naming Conventions
- `my_tool.py` → `my-tool` (underscores to hyphens)
- `config.toml` → `{project}-config.toml` (prefix generic names)
- `data_processor.js` → `data-processor.js`

### Directory Structure
```
agent-repo/
├── outputs/           # Private workspace
│   ├── my_tool.py
│   └── analysis.json
└── Outputs/          # Public products (after extraction)
    ├── my-tool/
    │   ├── my-tool.py
    │   └── my-tool.manifest.json
    └── README.md
```

## Evolution Tracking

Each extraction is recorded in `.aget/evolution/` with:
- Source path
- Output name
- Extraction date
- Transformation notes

This creates a historical record of how private exploration becomes public value.

## Best Practices

1. **Let outputs accumulate naturally** - Don't force extraction
2. **Extract when stable** - Outputs should be tested and documented
3. **Maintain backwards compatibility** - Once public, Outputs have users
4. **Document the transformation** - Help others understand the bridge

## Integration with AGET

Bridge patterns integrate with the AGET framework:

```bash
# Future commands (Phase 4)
aget extract outputs/my_tool.py    # Extract specific output
aget bridge scan                    # Scan for valuable outputs
aget bridge history                 # Show extraction history
```

## Philosophy

The bridge pattern embodies the AGET philosophy:
- Private exploration leads to public value
- Agents are co-creators, not just automators
- Every extraction adds value to the community
- The bridge makes private innovation accessible

---

*Bridge patterns are a key innovation of AGET v2, enabling agents to become true co-creators of community tools.*