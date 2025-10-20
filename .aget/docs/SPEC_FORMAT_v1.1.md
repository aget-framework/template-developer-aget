# Specifications-as-Code Format v1.1

**Version:** 1.1.0
**Date:** 2025-09-29
**Changes from v1.0:** Added EARS temporal patterns

## Grammar Structure

### Core Pattern
```
[PATTERN] SYSTEM shall <verb> <Object> [preposition] [Constraint]
```

**New in v1.1:** PATTERN prefix specifies temporal/conditional behavior using EARS (Easy Approach to Requirements Syntax).

## EARS Temporal Patterns

EARS provides 5 patterns that eliminate ambiguity about when/how requirements apply:

### 1. Ubiquitous (Always-True)
**Format:** `The SYSTEM shall <requirement>`

**When to use:** Continuous, always-active requirements

**Examples:**
```
The SYSTEM shall detect Format_Version from Export_Data
The SYSTEM shall maintain Unique_Data WITHOUT Duplicate_Records
The SYSTEM shall store Listening_History in Parquet_Format
```

### 2. Event-Driven (WHEN)
**Format:** `WHEN <trigger> the SYSTEM shall <requirement>`

**When to use:** Requirements triggered by specific events

**Examples:**
```
WHEN Import_Start is received, the SYSTEM shall parse Export_Data
WHEN Legacy_Format is detected, the SYSTEM shall convert to Modern_Format
WHEN Malformed_Data is encountered, the SYSTEM shall log Error_Details
```

### 3. State-Driven (WHILE)
**Format:** `WHILE <state> the SYSTEM shall <requirement>`

**When to use:** Requirements active during specific states

**Examples:**
```
WHILE processing Hundred_Thousand_Records, the SYSTEM shall display Progress_Indicator
WHILE in Analysis_Mode, the SYSTEM shall cache Temporal_Data
WHILE Export_In_Progress, the SYSTEM shall block New_Imports
```

### 4. Optional (WHERE)
**Format:** `WHERE <feature> the SYSTEM shall <requirement>`

**When to use:** Context-specific requirements (user preferences, configurations)

**Examples:**
```
WHERE Export_Json is enabled, the SYSTEM shall export Analysis_Results as Json_Format
WHERE Interactive_Mode is active, the SYSTEM shall render Interactive_Visualizations
WHERE Legacy_Support is enabled, the SYSTEM shall accept End_Time_Field
```

### 5. Conditional (IF...THEN)
**Format:** `IF <condition> THEN the SYSTEM shall <requirement>`

**When to use:** Logical conditions with consequences

**Examples:**
```
IF Binge_Session exceeds Thirty_Plays THEN the SYSTEM shall flag Single_Artist
IF Memory_Usage exceeds 2GB THEN the SYSTEM shall trigger Incremental_Processing
IF Duplicate_Records exceed Ninety_Five_Percent THEN the SYSTEM shall reject Export_Data
```

---

## Pattern Selection Guide

| Pattern | When Requirement Applies | Example Use Case |
|---------|-------------------------|------------------|
| **Ubiquitous** | Always (continuous) | Core functionality, data validation |
| **WHEN** | After specific event | Import triggers, error handling |
| **WHILE** | During specific state | Long operations, mode-specific behavior |
| **WHERE** | Specific configuration/feature | Optional features, user preferences |
| **IF...THEN** | Logical condition true | Thresholds, conditional logic |

**Default:** If unsure, use **ubiquitous**. It's always-active and least ambiguous.

---

## Integration with Existing Grammar

### Casing Standards
- **Controlled Vocabulary**: `Title_Case` (domain objects with underscores)
- **Verbs**: `lowercase`
- **Prepositions/Connectors**: `lowercase`
- **Constraints**: `UPPERCASE` keywords + values

## Language Elements

### Verbs (lowercase)
```
detect, identify, classify, recognize
calculate, compute, derive, aggregate
transform, convert, normalize, standardize
store, retrieve, persist, cache
display, render, export, report
filter, sort, group, partition
accept, reject, validate, process
```

### Prepositions/Connectors (lowercase)
```
from, to, as, with, within, containing
when, upon, after, before, during
matching, excluding, including
```

### Constraint Keywords (UPPERCASE)
```
WITHIN <time>
ACCURACY <percentage>
PRECISION <value>
WITHOUT <consequence>
MAINTAINING <property>
EXCEEDING <threshold>
```

## Controlled Vocabulary (Title_Case)

### Data Objects
```
Export_Data              # Spotify export archive
Format_Version           # Version identifier
Legacy_Format            # 2014-2020 format
Modern_Format            # 2021+ format
End_Time_Field           # Legacy timestamp
Ts_Field                 # Modern timestamp
Multiple_Archives        # Multiple export files
```

### Processing Objects
```
Duplicate_Records        # Repeated entries
Unique_Data             # Non-duplicated records
Listening_History       # Complete play history
Temporal_Data           # Time-series information
Malformed_Data          # Corrupted/invalid data
```

### Analysis Objects
```
Hourly_Distribution     # Plays by hour
Daily_Patterns          # Plays by day
Seasonal_Patterns       # Seasonal trends
Binge_Sessions          # Concentrated listening
Single_Artist           # Individual artist
Thirty_Plays            # 30 play threshold
```

### Output Objects
```
Analysis_Results        # Computed insights
Json_Format            # JSON output
Parquet_Format         # Parquet output
Interactive_Visualizations  # Plotly charts
```

### Quantities
```
Hundred_Thousand_Records  # 100,000 records
Twenty_Four_Hours         # 24 hour period
Thirty_Seconds           # 30 second limit
Ninety_Five_Percent      # 95% threshold
```

## Complete Specification Example (v1.1 with EARS)

```yaml
spec:
  id: SPEC-SPOTIFY-ANALYST
  version: 2.1.0  # Updated with EARS patterns
  format_version: "1.1"

capabilities:
  CAP-001:
    domain: ingestion
    type: ubiquitous
    statement: "The SYSTEM shall detect Format_Version from Export_Data"

  CAP-002:
    domain: ingestion
    type: event-driven
    statement: "WHEN Legacy_Format is detected, the SYSTEM shall convert End_Time_Field to Ts_Field"

  CAP-003:
    domain: ingestion
    type: ubiquitous
    statement: "The SYSTEM shall accept both Legacy_Format and Modern_Format"

  CAP-004:
    domain: processing
    type: event-driven
    statement: "WHEN processing Multiple_Archives, the SYSTEM shall identify Duplicate_Records"

  CAP-005:
    domain: processing
    type: ubiquitous
    statement: "The SYSTEM shall maintain Unique_Data WITHOUT Duplicate_Records"

  CAP-006:
    domain: performance
    type: ubiquitous
    statement: "The SYSTEM shall process Hundred_Thousand_Records WITHIN Thirty_Seconds"
    governance: [CONST-P-001]

  CAP-007:
    domain: analysis
    type: ubiquitous
    statement: "The SYSTEM shall calculate Hourly_Distribution from Listening_History"

  CAP-008:
    domain: analysis
    type: ubiquitous
    statement: "The SYSTEM shall derive Seasonal_Patterns from Temporal_Data with ACCURACY Ninety_Five_Percent"

  CAP-009:
    domain: analysis
    type: conditional
    statement: "IF Single_Artist exceeds Thirty_Plays WITHIN Twenty_Four_Hours, THEN the SYSTEM shall flag Binge_Session"

  CAP-010:
    domain: export
    type: optional
    statement: "WHERE Export_Json is enabled, the SYSTEM shall export Analysis_Results as Json_Format"

  CAP-011:
    domain: export
    type: ubiquitous
    statement: "The SYSTEM shall export Analysis_Results as Parquet_Format"

  CAP-012:
    domain: visualization
    type: optional
    statement: "WHERE Interactive_Mode is active, the SYSTEM shall render Interactive_Visualizations"

  CAP-013:
    domain: quality
    statement: "SYSTEM shall validate All_Calculations with ACCURACY Ninety_Nine_Percent"

  CAP-014:
    domain: resilience
    statement: "SYSTEM shall reject Malformed_Data WITHOUT termination"

dependencies:
  CAP-004: [CAP-001, CAP-002, CAP-003]  # Format detection required first
  CAP-005: [CAP-004]                    # Must identify before removing
  CAP-007: [CAP-005]                    # Clean data for analysis
  CAP-008: [CAP-005]                    # Clean data for analysis
  CAP-009: [CAP-005]                    # Clean data for analysis
```

## Vocabulary Registry

```yaml
vocabulary:
  version: 1.0.0

  # Data Objects
  Export_Data:
    definition: "Spotify privacy export archive containing listening history"
    format: "ZIP archive"

  Format_Version:
    definition: "Identifier for export format structure"
    values: ["Legacy_Format", "Modern_Format"]

  End_Time_Field:
    definition: "Timestamp field used in legacy exports (2014-2020)"
    type: "ISO 8601 datetime"

  Ts_Field:
    definition: "Timestamp field used in modern exports (2021+)"
    type: "Unix timestamp milliseconds"

  # Analysis Objects
  Binge_Sessions:
    definition: "Concentrated listening period of single artist"
    criteria: "≥30 plays within 24 hours"

  Seasonal_Patterns:
    definition: "Listening behavior variations across seasons"
    granularity: "3-month periods"

  # Quantities
  Hundred_Thousand_Records:
    value: 100000
    unit: "records"

  Thirty_Plays:
    value: 30
    unit: "plays"

  Twenty_Four_Hours:
    value: 24
    unit: "hours"

  Ninety_Five_Percent:
    value: 95
    unit: "percent"
```

## Change Request Format

```yaml
change_request:
  id: CR-006
  title: "Add podcast support"

  vocabulary_additions:
    Podcast_Data:
      definition: "Spotify podcast listening history"
      format: "Episode metadata with timestamps"

    Episode_Metadata:
      definition: "Podcast episode information"
      fields: ["show_name", "episode_name", "duration"]

  capability_additions:
    CAP-015:
      domain: ingestion
      statement: "SYSTEM shall identify Podcast_Data when containing Episode_Metadata"

    CAP-016:
      domain: analysis
      statement: "SYSTEM shall separate Podcast_Data from Music_Data during processing"

  capability_modifications:
    CAP-007:
      from: "SYSTEM shall calculate Hourly_Distribution from Listening_History"
      to: "SYSTEM shall calculate Hourly_Distribution from Listening_History excluding Podcast_Data"
```

## Parsing Example

```python
def parse_statement(statement):
    """Parse a capability statement"""
    # Example: "SYSTEM shall detect Format_Version from Export_Data"

    tokens = statement.split()
    assert tokens[0] == "SYSTEM"
    assert tokens[1] == "shall"

    verb = tokens[2]  # "detect"
    object = tokens[3]  # "Format_Version"

    # Verify object is in vocabulary
    assert object in vocabulary

    # Extract prepositions and constraints
    if "from" in tokens:
        source = tokens[tokens.index("from") + 1]

    if "WITHIN" in tokens:
        constraint = tokens[tokens.index("WITHIN") + 1]

    return {
        "verb": verb,
        "object": object,
        "source": source if source else None,
        "constraint": constraint if constraint else None
    }
```

## Benefits of Title_Case Format

1. **Unambiguous Parsing** - Single tokens, no quote handling
2. **Clear Visual Distinction** - Domain objects stand out
3. **Version Control Friendly** - Clean diffs
4. **Validation Ready** - Simple regex matching
5. **IDE Support** - Autocomplete works naturally

## Migration Checklist

- [ ] Convert all existing specs to Title_Case format
- [ ] Create vocabulary registry for current system
- [ ] Build parser/validator tool
- [ ] Update CR templates
- [ ] Train team on new format

---
*This format achieves true "specifications-as-code" with machine-parseable precision*