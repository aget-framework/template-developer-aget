# Example: API Health Monitor - Engineering Team Tool

> How a B2B SaaS team built critical infrastructure tooling in 2 hours instead of 2 sprints

## The Story

**ContractAI Engineering Team's Challenge**: "Our AI contract review platform serves 500+ enterprise clients through APIs. When a customer reports 'it's slow', we spend hours investigating. We need real-time visibility into API performance per customer, with smart alerting before they notice issues."

**Traditional Approach**: 2-sprint project, multiple engineers, complex monitoring stack, $50K/year in tooling...

**AGET Approach**: 2-hour team session, specs first, AI implements

## Step 1: Team Alignment Meeting (30 minutes)

The team (Backend Lead, SRE, Product Manager) creates specifications together:

### `FUNCTIONAL_REQUIREMENTS.md`

```markdown
# API Health Monitor - Functional Requirements

## Core Monitoring Capabilities

### FR-001: Customer-Centric Monitoring
**User Story**: As an engineer, I need to see API health per customer
**Acceptance Criteria**:
- Track latency percentiles (p50, p95, p99) per customer
- Monitor error rates by customer tier (Enterprise, Pro, Starter)
- Show request volume trends
- API endpoint breakdown (contract-upload, review, extract)

### FR-002: Intelligent Alerting
**User Story**: As on-call engineer, I need actionable alerts only
**Acceptance Criteria**:
- Alert BEFORE customer-visible impact
- Smart thresholds based on customer SLA
- Anomaly detection (not just fixed thresholds)
- Group related alerts to prevent alert storms
- Include runbook link in every alert

### FR-003: Historical Investigation
**User Story**: As support engineer, I need to investigate customer complaints
**Acceptance Criteria**:
- Query any customer's API performance for past 30 days
- Correlate with deployment timeline
- Show comparative analysis (vs their baseline, vs peer group)
- Export data for customer success team

### FR-004: SLA Compliance Dashboard
**User Story**: As engineering manager, I need to track SLA compliance
**Acceptance Criteria**:
- Real-time SLA status per customer tier
- Monthly uptime calculations
- Predicted SLA breach warnings
- Contract-specific thresholds (some customers have custom SLAs)

### FR-005: Developer Experience Metrics
**User Story**: As platform team, we need to track API usability
**Acceptance Criteria**:
- Track API key usage patterns
- Identify common error patterns
- Show adoption of new endpoints
- Integration success rates
```

## Step 2: Define Operating Rules (20 minutes)

### `BUSINESS_RULES.md`

```markdown
# API Health Monitor - Business Rules

## Monitoring Philosophy

### BR-001: Customer Impact First
**Rule**: Prioritize metrics by customer revenue impact
**Implementation**:
- Enterprise customers (>$100K ARR): 1-minute checks
- Pro customers ($10-50K ARR): 5-minute checks
- Starter customers (<$10K ARR): 15-minute checks

### BR-002: Alert Fatigue Prevention
**Rule**: Maximum 3 alerts per hour per engineer
**How**:
- Aggregate related issues
- Suppress during known maintenance
- Escalate only if unacknowledged for 15 minutes

### BR-003: Data Retention Policy
**Rule**: Keep granular data for investigation windows
**Retention**:
- 1-minute granularity: 7 days
- 5-minute aggregates: 30 days
- Hourly aggregates: 1 year
- Daily summaries: Indefinite

### BR-004: Performance Baselines
**Rule**: Each customer has their own "normal"
**Calculation**:
- Baseline = median of same hour, same day of week, past 4 weeks
- Anomaly = >2 standard deviations from baseline
- Exclude known incident periods from baseline

### BR-005: SLA Definitions
**Rule**: SLA breaches are contractual obligations
**Tiers**:
- Enterprise: 99.9% uptime, <200ms p95 latency
- Pro: 99.5% uptime, <500ms p95 latency
- Starter: 99% uptime, <1000ms p95 latency

### BR-006: Privacy and Security
**Rule**: Never log request/response payloads
**What we track**: Metadata only (timestamps, status, latency, customer ID)
**What we DON'T track**: Contract content, PII, authentication tokens
```

## Step 3: Technical Architecture (20 minutes)

### `DATA_SPECIFICATIONS.md`

```markdown
# API Health Monitor - Data Specifications

## Metric Event
```json
{
  "timestamp": "2025-09-25T14:30:00Z",
  "customer_id": "cust_abc123",
  "customer_tier": "enterprise",
  "endpoint": "/api/v2/contract/review",
  "method": "POST",
  "status_code": 200,
  "latency_ms": 145,
  "request_size_bytes": 51200,
  "response_size_bytes": 8192,
  "api_version": "v2",
  "region": "us-east-1",
  "trace_id": "550e8400-e29b-41d4-a716",
  "error_type": null
}
```

## Aggregated Metrics (1-minute buckets)
```json
{
  "bucket": "2025-09-25T14:30:00Z",
  "customer_id": "cust_abc123",
  "endpoint": "/api/v2/contract/review",
  "request_count": 47,
  "error_count": 2,
  "latency_p50": 142,
  "latency_p95": 298,
  "latency_p99": 512,
  "total_bytes_processed": 2408448,
  "unique_api_keys": 3,
  "sla_compliance": true
}
```

## Alert Configuration
```json
{
  "alert_id": "alert_001",
  "name": "High latency for Enterprise customer",
  "condition": "latency_p95 > customer_baseline * 2",
  "severity": "warning|critical",
  "customer_tiers": ["enterprise"],
  "notification_channels": ["slack", "pagerduty"],
  "runbook_url": "https://wiki/runbooks/high-latency",
  "cooldown_minutes": 15
}
```

## SLA Report
```json
{
  "customer_id": "cust_abc123",
  "period": "2025-09",
  "uptime_percentage": 99.94,
  "latency_p95_avg": 187,
  "total_requests": 1847293,
  "error_rate": 0.0012,
  "sla_breaches": [],
  "credits_owed": 0
}
```
```

## Step 4: AI Implementation Sprint (60 minutes)

The team provides specs to AI with this prompt:

> "Build an API health monitoring system based on these specifications. Use Python with FastAPI for the API, TimescaleDB for time-series storage, and Redis for real-time aggregation. Create both ingestion pipeline and query API."

### AI generates the complete system:

#### `monitor/ingestion.py` - Real-time metric processing
```python
from typing import Dict, List
import asyncio
import json
from datetime import datetime, timedelta
import redis.asyncio as redis
import asyncpg
from dataclasses import dataclass
import numpy as np

@dataclass
class MetricEvent:
    """Incoming API metric"""
    timestamp: datetime
    customer_id: str
    customer_tier: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: int
    trace_id: str

class HealthMonitorIngestion:
    """FR-001: Customer-centric monitoring pipeline"""

    def __init__(self):
        self.redis = redis.Redis(decode_responses=True)
        self.timescale = None  # AsyncPG connection
        self.customer_baselines = {}

    async def ingest_metric(self, metric: MetricEvent):
        """Process incoming metric in real-time"""

        # BR-006: Privacy - we only track metadata
        # Never log actual contract content

        # Real-time aggregation in Redis (1-minute buckets)
        bucket = self.get_time_bucket(metric.timestamp, minutes=1)
        key = f"metrics:{bucket}:{metric.customer_id}:{metric.endpoint}"

        # Atomic increment of counters
        pipe = self.redis.pipeline()
        pipe.hincrby(key, "request_count", 1)
        if metric.status_code >= 400:
            pipe.hincrby(key, "error_count", 1)

        # Update latency percentiles (using Redis sorted sets)
        pipe.zadd(f"{key}:latencies", {metric.trace_id: metric.latency_ms})

        await pipe.execute()

        # Check for anomalies (BR-004: Performance baselines)
        if await self.is_anomaly(metric):
            await self.trigger_alert(metric)

        # Persist to TimescaleDB for long-term storage
        await self.persist_to_timescale(metric)

    async def is_anomaly(self, metric: MetricEvent) -> bool:
        """BR-004: Each customer has their own 'normal'"""
        baseline_key = f"baseline:{metric.customer_id}:{metric.endpoint}:{datetime.now().hour}"
        baseline = await self.redis.get(baseline_key)

        if not baseline:
            # Calculate baseline from historical data
            baseline = await self.calculate_baseline(
                metric.customer_id,
                metric.endpoint,
                datetime.now().hour
            )
            await self.redis.setex(baseline_key, 3600, baseline)

        baseline_val = float(baseline)
        # Anomaly = >2 standard deviations from baseline
        std_dev = baseline_val * 0.15  # Approximate std dev as 15% of baseline

        return metric.latency_ms > (baseline_val + 2 * std_dev)

    async def trigger_alert(self, metric: MetricEvent):
        """FR-002: Intelligent alerting"""

        # BR-002: Alert fatigue prevention
        alert_count = await self.redis.get(f"alert_count:{metric.customer_id}")
        if alert_count and int(alert_count) >= 3:
            return  # Max alerts per hour reached

        alert = {
            'timestamp': metric.timestamp.isoformat(),
            'customer_id': metric.customer_id,
            'customer_tier': metric.customer_tier,
            'endpoint': metric.endpoint,
            'latency_ms': metric.latency_ms,
            'severity': 'critical' if metric.customer_tier == 'enterprise' else 'warning',
            'runbook_url': self.get_runbook_url('high_latency'),
            'message': f"Anomaly detected: {metric.latency_ms}ms latency for {metric.customer_id}"
        }

        # BR-001: Customer impact first - Enterprise alerts go to PagerDuty
        if metric.customer_tier == 'enterprise':
            await self.send_to_pagerduty(alert)
        else:
            await self.send_to_slack(alert)

        # Increment alert counter
        await self.redis.incr(f"alert_count:{metric.customer_id}")
        await self.redis.expire(f"alert_count:{metric.customer_id}", 3600)

    async def calculate_percentiles(self, customer_id: str, endpoint: str, bucket: str):
        """Calculate p50, p95, p99 for a time bucket"""
        key = f"metrics:{bucket}:{customer_id}:{endpoint}:latencies"
        latencies = await self.redis.zrange(key, 0, -1, withscores=True)

        if not latencies:
            return None

        values = [score for _, score in latencies]
        return {
            'p50': np.percentile(values, 50),
            'p95': np.percentile(values, 95),
            'p99': np.percentile(values, 99)
        }

    async def aggregate_and_store(self):
        """Periodic aggregation task (runs every minute)"""
        while True:
            await asyncio.sleep(60)

            # Get all metric keys from current minute
            current_bucket = self.get_time_bucket(datetime.now() - timedelta(minutes=1))
            pattern = f"metrics:{current_bucket}:*"

            async for key in self.redis.scan_iter(pattern):
                parts = key.split(':')
                customer_id = parts[2]
                endpoint = parts[3]

                # Get aggregated values
                data = await self.redis.hgetall(key)
                percentiles = await self.calculate_percentiles(customer_id, endpoint, current_bucket)

                if data and percentiles:
                    # BR-003: Data retention policy
                    await self.store_aggregated_metric(
                        bucket=current_bucket,
                        customer_id=customer_id,
                        endpoint=endpoint,
                        request_count=int(data.get('request_count', 0)),
                        error_count=int(data.get('error_count', 0)),
                        **percentiles
                    )

                    # Check SLA compliance (BR-005)
                    await self.check_sla_compliance(customer_id, endpoint, percentiles)

                # Clean up Redis (keep only 7 days of granular data)
                await self.redis.expire(key, 7 * 24 * 3600)
```

#### `monitor/query_api.py` - Query and visualization API
```python
from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import asyncpg

app = FastAPI(title="API Health Monitor")

class HealthMonitorAPI:
    """FR-003, FR-004, FR-005: Query interface"""

    @app.get("/health/{customer_id}")
    async def get_customer_health(
        customer_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        """FR-003: Historical investigation"""

        if not start_time:
            start_time = datetime.now() - timedelta(days=7)
        if not end_time:
            end_time = datetime.now()

        # Query time-series data
        query = """
            SELECT
                time_bucket('5 minutes', timestamp) AS bucket,
                endpoint,
                AVG(latency_p95) as avg_p95,
                AVG(latency_p99) as avg_p99,
                SUM(request_count) as total_requests,
                SUM(error_count) as total_errors,
                AVG(error_count::float / NULLIF(request_count, 0)) as error_rate
            FROM api_metrics
            WHERE customer_id = $1
                AND timestamp >= $2
                AND timestamp <= $3
            GROUP BY bucket, endpoint
            ORDER BY bucket DESC
        """

        results = await db.fetch(query, customer_id, start_time, end_time)

        # Add comparative analysis
        peer_performance = await get_peer_comparison(customer_id)
        baseline = await get_customer_baseline(customer_id)

        return {
            'customer_id': customer_id,
            'period': {'start': start_time, 'end': end_time},
            'metrics': [dict(r) for r in results],
            'peer_comparison': peer_performance,
            'baseline_comparison': baseline,
            'health_score': calculate_health_score(results)
        }

    @app.get("/sla/compliance")
    async def get_sla_compliance(tier: Optional[str] = None):
        """FR-004: SLA Compliance Dashboard"""

        # BR-005: SLA Definitions per tier
        sla_targets = {
            'enterprise': {'uptime': 99.9, 'latency_p95': 200},
            'pro': {'uptime': 99.5, 'latency_p95': 500},
            'starter': {'uptime': 99.0, 'latency_p95': 1000}
        }

        query = """
            WITH monthly_stats AS (
                SELECT
                    customer_id,
                    customer_tier,
                    COUNT(*) FILTER (WHERE status_code < 500) * 100.0 / COUNT(*) as uptime,
                    AVG(latency_p95) as avg_latency_p95,
                    COUNT(*) as total_requests
                FROM api_metrics
                WHERE timestamp >= date_trunc('month', CURRENT_DATE)
                GROUP BY customer_id, customer_tier
            )
            SELECT
                *,
                CASE
                    WHEN customer_tier = 'enterprise' AND uptime < 99.9 THEN true
                    WHEN customer_tier = 'pro' AND uptime < 99.5 THEN true
                    WHEN customer_tier = 'starter' AND uptime < 99.0 THEN true
                    ELSE false
                END as sla_breach,
                CASE
                    WHEN customer_tier = 'enterprise' AND uptime < 99.9
                    THEN (99.9 - uptime) * 10 -- 10% credit per 0.1% downtime
                    ELSE 0
                END as credits_percentage
            FROM monthly_stats
            WHERE ($1::text IS NULL OR customer_tier = $1)
            ORDER BY sla_breach DESC, uptime ASC
        """

        results = await db.fetch(query, tier)

        return {
            'timestamp': datetime.now(),
            'compliance_summary': {
                'total_customers': len(results),
                'compliant': sum(1 for r in results if not r['sla_breach']),
                'breached': sum(1 for r in results if r['sla_breach']),
                'credits_owed': sum(r['credits_percentage'] for r in results)
            },
            'customers': [dict(r) for r in results]
        }

    @app.get("/alerts/configuration")
    async def get_smart_thresholds(customer_id: str):
        """FR-002: Intelligent alerting configuration"""

        # BR-004: Performance baselines
        # Calculate dynamic thresholds based on historical patterns

        query = """
            SELECT
                endpoint,
                EXTRACT(hour FROM timestamp) as hour,
                EXTRACT(dow FROM timestamp) as day_of_week,
                percentile_cont(0.5) WITHIN GROUP (ORDER BY latency_p95) as median_p95,
                stddev(latency_p95) as stddev_p95
            FROM api_metrics
            WHERE customer_id = $1
                AND timestamp >= CURRENT_DATE - INTERVAL '30 days'
                AND status_code < 400  -- Exclude error responses from baseline
            GROUP BY endpoint, hour, day_of_week
        """

        baselines = await db.fetch(query, customer_id)

        # Generate smart thresholds
        thresholds = []
        for baseline in baselines:
            threshold = {
                'endpoint': baseline['endpoint'],
                'hour': baseline['hour'],
                'day_of_week': baseline['day_of_week'],
                'warning_threshold': baseline['median_p95'] + baseline['stddev_p95'],
                'critical_threshold': baseline['median_p95'] + (2 * baseline['stddev_p95']),
                'auto_adjusted': True,
                'confidence': 0.85 if baseline['stddev_p95'] < 50 else 0.65
            }
            thresholds.append(threshold)

        return {
            'customer_id': customer_id,
            'generated_at': datetime.now(),
            'thresholds': thresholds,
            'recommendation': "These thresholds are based on your historical patterns"
        }

    @app.get("/metrics/developer")
    async def get_developer_metrics():
        """FR-005: Developer experience metrics"""

        query = """
            WITH api_usage AS (
                SELECT
                    endpoint,
                    api_version,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    COUNT(DISTINCT api_key_hash) as unique_keys,
                    COUNT(*) as total_calls,
                    AVG(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as error_rate,
                    percentile_cont(0.5) WITHIN GROUP (ORDER BY latency_ms) as median_latency
                FROM api_metrics
                WHERE timestamp >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY endpoint, api_version
            )
            SELECT
                *,
                CASE
                    WHEN error_rate > 0.05 THEN 'needs_attention'
                    WHEN median_latency > 500 THEN 'performance_issue'
                    ELSE 'healthy'
                END as status
            FROM api_usage
            ORDER BY total_calls DESC
        """

        results = await db.fetch(query)

        # Identify patterns
        common_errors = await identify_error_patterns()
        adoption_trends = await calculate_adoption_trends()

        return {
            'api_health': [dict(r) for r in results],
            'error_patterns': common_errors,
            'adoption_trends': adoption_trends,
            'recommendations': generate_api_recommendations(results)
        }
```

## Step 5: Team Deployment (30 minutes)

```bash
# Quick deployment with Docker
docker-compose up -d

# Verify it's working
curl http://localhost:8000/health/cust_enterprise_001

{
  "customer_id": "cust_enterprise_001",
  "health_score": 94,
  "current_status": "healthy",
  "latency_trend": "stable",
  "error_rate": 0.0012,
  "sla_compliance": true
}

# Check SLA dashboard
curl http://localhost:8000/sla/compliance

{
  "compliance_summary": {
    "total_customers": 487,
    "compliant": 483,
    "breached": 4,
    "credits_owed": 2.5
  }
}
```

## The Engineering Impact

### Before AGET Approach
- **Planning**: 2 days of meetings
- **Development**: 2 sprints (4 weeks)
- **Testing**: 1 week
- **Deployment**: 3 days
- **Total**: ~6 weeks, 3 engineers

### With AGET Approach
- **Specification**: 1.5 hours (whole team aligned)
- **Implementation**: 1 hour (AI generates code)
- **Review & Deploy**: 30 minutes
- **Total**: 2 hours, same-day deployment

### Key Benefits for Engineering Teams

#### 1. Specification as Contract
- Frontend team knows exactly what APIs to expect
- QA knows exactly what to test
- Product knows exactly what's being built
- No scope creep during development

#### 2. AI as Team Member
- AI handles boilerplate and infrastructure
- Engineers focus on business logic and edge cases
- Code reviews focus on requirements, not implementation

#### 3. Rapid Iteration
- Change requirement? Update spec, regenerate
- New feature? Add to spec, AI extends code
- Bug found? Fix in spec ensures it never returns

#### 4. Knowledge Persistence
- New engineer joins? Specs explain everything
- Switching AI tools? Specs work with any AI
- Year later? Specs still document the "why"

### Generalizable Patterns

This approach works for any B2B SaaS engineering team:

**For API-First Products:**
- Replace "contract review" with your domain
- Same monitoring needs apply
- Customer-centric metrics are universal

**For Data Processing Platforms:**
- Monitor pipeline health instead of API latency
- Track data quality instead of response codes
- Same SLA compliance needs

**For ML/AI Platforms:**
- Monitor model performance metrics
- Track inference latency
- Add data drift detection

**For Developer Tools:**
- Track SDK adoption
- Monitor integration success rates
- Developer experience metrics

### Team Testimonial

> "We went from dreading infrastructure projects to knocking them out in an afternoon. The specs become our documentation, our tests, and our onboarding guide. Every engineer on the team can now build production-grade tools."
> — Engineering Manager, ContractAI

---

*This example demonstrates how AGET transforms engineering teams from specification writers to system designers, leveraging AI for rapid, high-quality implementation of critical infrastructure.*