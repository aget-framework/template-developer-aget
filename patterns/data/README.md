# Data Management Patterns

Patterns for database consolidation, migration, and management in AGET-enabled projects.

## Purpose

Many projects suffer from database proliferation - multiple SQLite files, JSON stores, and ad-hoc tracking systems. Data management patterns provide standardized approaches to consolidate and manage data effectively.

## Pattern Structure

```
patterns/data/
├── unified_db.py        # Base unified database implementation
├── adapters/           # Backward compatibility adapters
├── migrations/         # Schema migration tools
└── examples/          # Example implementations
```

## Core Concepts

### 1. Unified Database Pattern
Single source of truth replacing multiple databases:
- Consolidated schema design
- Thread-safe operations
- Connection pooling
- Automatic migrations

### 2. Adapter Pattern
Drop-in replacements for existing interfaces:
- Zero code changes required
- Gradual migration support
- Performance improvements
- Backward compatibility

### 3. Operation Context
Track operations across their lifecycle:
```python
context = db.start_operation("enhance", page_title="Example")
# ... do work ...
db.complete_operation(context.operation_id)
```

## Implementation Template

```python
from patterns.data.base import UnifiedDatabaseBase

class ProjectDatabase(UnifiedDatabaseBase):
    """
    Project-specific unified database.
    Consolidates: tracking.db, metrics.db, queue.db
    """

    SCHEMA_VERSION = "1.0.0"

    def get_schema(self):
        return """
        CREATE TABLE operations (...);
        CREATE TABLE metrics (...);
        CREATE TABLE queue (...);
        """

    def get_adapters(self):
        return {
            'TrackingDB': TrackingAdapter,
            'MetricsDB': MetricsAdapter,
            'QueueDB': QueueAdapter
        }
```

## Migration Strategy

### Phase 1: Analysis
```bash
python patterns/data/analyze.py --scan .
# Output: Found 5 databases, 12 interfaces
```

### Phase 2: Schema Design
```bash
python patterns/data/design_schema.py --input analysis.json
# Output: Unified schema with 4 tables, 23 columns
```

### Phase 3: Implementation
```bash
python patterns/data/implement.py --schema unified.sql
# Creates: patterns/data/project_db.py
```

### Phase 4: Migration
```bash
python patterns/data/migrate.py --dry-run
python patterns/data/migrate.py --execute
```

## Benefits

### Before (Multiple Databases)
```
data/
├── tracking.db     # 50MB
├── metrics.db      # 30MB
├── queue.db        # 10MB
├── cache.db        # 20MB
└── temp.db         # 5MB
Total: 115MB, 5 backup points, complex queries
```

### After (Unified Database)
```
data/
└── unified.db      # 80MB (compressed, indexed)
Total: 80MB, 1 backup point, efficient queries
```

## Common Patterns

### 1. Event Tracking
```python
class EventDatabase(UnifiedDatabaseBase):
    """Track all system events in one place"""
```

### 2. Multi-tenant Data
```python
class TenantDatabase(UnifiedDatabaseBase):
    """Separate data by tenant/project"""
```

### 3. Time-series Data
```python
class TimeSeriesDatabase(UnifiedDatabaseBase):
    """Optimized for time-based queries"""
```

## Best Practices

1. **Always use transactions** for multi-table operations
2. **Index foreign keys** for performance
3. **Implement soft deletes** for audit trails
4. **Use JSON columns** for flexible metadata
5. **Version your schema** for migrations
6. **Test with production data volumes**

## Example: RKB Unified Tracking

The RKB project consolidated 7+ databases into one:

```python
# Before: Multiple imports and connections
from action_tracker import ActionTracker
from cost_tracker import CostTracker
from quality_tracker import QualityTracker
# ... 7 different database connections

# After: Single unified interface
from patterns.data.rkb_unified import RKBDatabase
db = RKBDatabase()
# All functionality through one connection
```

## Testing Data Patterns

```bash
# Test thread safety
python -m pytest patterns/data/tests/test_concurrency.py

# Test migration
python -m pytest patterns/data/tests/test_migration.py

# Performance benchmarks
python patterns/data/benchmark.py
```

## Trigger Phrases

When integrated with AGENTS.md:

- **"analyze databases"** - Scan for consolidation opportunities
- **"unify tracking"** - Create unified database schema
- **"migrate data"** - Run migration with safety checks
- **"optimize database"** - Compact and reindex

---
*Part of EP-13: Data Management Patterns*