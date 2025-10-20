# [PROJECT NAME] Data Specifications

> Document your data structures, schemas, and flows

## Data Overview
<!-- What kind of data does your system handle? -->

**Primary Data Types**:
- <!-- User data, transactions, logs, etc. -->

**Data Sources**:
- <!-- Database, APIs, files, user input -->

**Data Destinations**:
- <!-- Where does processed data go? -->

---

## Core Data Models
<!-- Document your main data structures -->

### [Entity Name]
**Purpose**: <!-- What this data represents -->
**Source**: <!-- Where it comes from -->

#### Schema
```json
{
  "field_name": {
    "type": "string|number|boolean|array|object",
    "required": true|false,
    "description": "What this field contains",
    "example": "Example value",
    "constraints": "Any validation rules"
  }
}
```

#### Relationships
- **Has Many**: <!-- Related entities -->
- **Belongs To**: <!-- Parent entities -->
- **References**: <!-- External IDs -->

#### Lifecycle
1. **Created**: <!-- When/how created -->
2. **Updated**: <!-- When/how modified -->
3. **Archived/Deleted**: <!-- Retention policy -->

---

## Data Formats
<!-- For file-based or API data -->

### Input Formats
#### [Format Name] (e.g., CSV Import)
**File Type**: <!-- .csv, .json, .xml -->
**Structure**:
```
Example of the format
```
**Validation Rules**:
- <!-- Required fields -->
- <!-- Format constraints -->

### Output Formats
#### [Format Name] (e.g., Report Export)
**File Type**: <!-- Generated format -->
**Template**: <!-- If applicable -->
**Contents**: <!-- What's included -->

---

## Data Flow Diagrams
<!-- How data moves through your system -->

```
[Source] → [Process] → [Transform] → [Store] → [Output]
```

### Flow: [Flow Name]
1. **Input**: <!-- What comes in -->
2. **Validation**: <!-- Checks performed -->
3. **Processing**: <!-- Transformations -->
4. **Storage**: <!-- Where it's saved -->
5. **Output**: <!-- What goes out -->

---

## Database Schema
<!-- If using a database -->

### Table: [table_name]
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY | Unique identifier |
| <!-- name --> | <!-- type --> | <!-- constraints --> | <!-- purpose --> |

**Indexes**:
- <!-- Performance optimizations -->

**Triggers**:
- <!-- Automated actions -->

---

## API Data Contracts
<!-- For API-based systems -->

### Endpoint: [GET|POST|PUT|DELETE] /path
**Request**:
```json
{
  "parameter": "description"
}
```

**Response**:
```json
{
  "field": "description"
}
```

**Error Codes**:
- `400`: <!-- Bad request reason -->
- `404`: <!-- Not found reason -->
- `500`: <!-- Server error reason -->

---

## Data Quality Rules

### Validation Rules
- **Required Fields**: <!-- Must be present -->
- **Format Validation**: <!-- Patterns to match -->
- **Range Checks**: <!-- Min/max values -->
- **Referential Integrity**: <!-- Foreign key constraints -->

### Data Cleaning
- **Normalization**: <!-- How data is standardized -->
- **Deduplication**: <!-- How duplicates are handled -->
- **Default Values**: <!-- What's used when missing -->

---

## Privacy & Security

### Sensitive Data
<!-- Mark fields that need protection -->

| Field | Classification | Protection Method |
|-------|---------------|-------------------|
| <!-- field --> | PII/Confidential/Public | Encryption/Hashing/Masking |

### Data Retention
- **Active**: <!-- How long kept accessible -->
- **Archive**: <!-- Long-term storage -->
- **Deletion**: <!-- When permanently removed -->

### Access Control
- **Read Access**: <!-- Who can view -->
- **Write Access**: <!-- Who can modify -->
- **Admin Access**: <!-- Who can delete -->

---

## Data Migration
<!-- For evolving schemas -->

### Version History
| Version | Date | Changes | Migration Script |
|---------|------|---------|------------------|
| 1.0 | <!-- date --> | Initial schema | <!-- script --> |

### Migration Strategy
- **Forward**: <!-- How to upgrade -->
- **Rollback**: <!-- How to downgrade -->
- **Data Preservation**: <!-- What to keep -->

---

## Discovery Notes

### Questions
- <!-- What's unclear about the data? -->

### Observations
- <!-- Patterns noticed -->
- <!-- Potential issues -->

### TODOs
- [ ] <!-- Document this data structure -->
- [ ] <!-- Verify this relationship -->
- [ ] <!-- Check this constraint -->

---

*Template Version: 1.0*
*Last Updated: [DATE]*
*Coverage: Documented [X] of [Y] data models*