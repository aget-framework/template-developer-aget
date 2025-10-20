# Test Coverage Improvement Plan - AGET v2.0

## Current Status (2025-09-25)
- **Overall Coverage**: 70% (1680/2387 lines)
- **Test Count**: 220 tests (174 passing, 46 failing)
- **Target**: 80% by October 7, 2025 (release date)
- **Gap to Target**: 10% (~240 lines)

## Strategic Priorities

### Priority 1: Fix Failing Tests (Quick Wins)
**Impact**: Stabilize test suite, enable CI/CD
**Effort**: 2-3 hours
**Coverage Gain**: ~2-3%

The 46 failing tests are mostly due to:
- Missing mock implementations
- Changed API signatures
- Test assumptions about return values

### Priority 2: Zero-Coverage Modules
**Impact**: Eliminate blind spots
**Effort**: 4-5 hours
**Coverage Gain**: ~5-6%

Modules with 0% coverage:
1. `aget/quality/__init__.py` (93 lines) - Quality assurance framework
2. `aget/config/commands/merge_content.py` (88 lines) - Content merger
3. `aget/config/__init__.py` (137 lines at 10%) - Core configuration

### Priority 3: Critical Path Coverage
**Impact**: Ensure reliability of core features
**Effort**: 3-4 hours
**Coverage Gain**: ~2-3%

Focus on improving:
- `aget/__main__.py` (32% → 80%) - Entry point
- `patterns/session/*` patterns (78-86% → 90%) - Critical workflows
- `aget/shared/backup.py` (74% → 85%) - Data safety

## Incremental Milestones

### Milestone 1: Stabilization (Day 1-2)
**Target Date**: September 26-27
**Coverage Target**: 72%

Tasks:
- [ ] Fix all 46 failing tests
- [ ] Ensure CI pipeline runs green
- [ ] Document test patterns for contributors

Deliverables:
- All tests passing
- Coverage baseline established
- Test documentation updated

### Milestone 2: Core Coverage (Day 3-4)
**Target Date**: September 28-29
**Coverage Target**: 75%

Tasks:
- [ ] Add tests for `aget/quality/__init__.py`
- [ ] Add tests for `aget/__main__.py` entry point
- [ ] Improve `aget/config/__init__.py` coverage

Deliverables:
- Quality module fully tested
- Entry point coverage >70%
- Configuration coverage >50%

### Milestone 3: Pattern Excellence (Day 5-6)
**Target Date**: September 30 - October 1
**Coverage Target**: 78%

Tasks:
- [ ] Enhance session pattern tests to 90%
- [ ] Complete housekeeping pattern coverage
- [ ] Add integration tests for pattern chains

Deliverables:
- All critical patterns >85% coverage
- Pattern integration tests
- Performance benchmarks

### Milestone 4: Polish & Release Prep (Day 7-8)
**Target Date**: October 2-3
**Coverage Target**: 80%+

Tasks:
- [ ] Address remaining coverage gaps
- [ ] Add edge case tests
- [ ] Create coverage report documentation
- [ ] Set up coverage badges

Deliverables:
- 80% coverage achieved
- Coverage reports automated
- Release notes prepared

### Milestone 5: Release Readiness (Day 9-10)
**Target Date**: October 4-7
**Coverage Target**: 80-82%

Tasks:
- [ ] Final test review
- [ ] Performance testing
- [ ] Documentation review
- [ ] Release candidate testing

Deliverables:
- v2.0.0 release candidate
- Full test documentation
- Performance benchmarks

## Implementation Strategy

### Phase 1: Fix Foundation (Immediate)
```bash
# Fix failing tests
python3 -m pytest tests/test_merge_content.py -xvs
python3 -m pytest tests/test_validate.py -xvs
python3 -m pytest tests/test_migrate.py -xvs

# Verify coverage baseline
python3 -m pytest --cov=. --cov-report=html
```

### Phase 2: Fill Gaps (Days 1-4)
```bash
# Test quality module
python3 -m pytest tests/test_quality.py --cov=aget/quality

# Test main entry
python3 -m pytest tests/test_main.py --cov=aget/__main__

# Test configuration
python3 -m pytest tests/test_config.py --cov=aget/config
```

### Phase 3: Enhance Patterns (Days 5-8)
```bash
# Pattern coverage
python3 -m pytest tests/test_*pattern*.py --cov=patterns

# Integration tests
python3 -m pytest tests/test_integration.py
```

## Success Metrics

### Must Have (October 7)
- [x] 70% overall coverage (achieved)
- [ ] 80% overall coverage
- [ ] All tests passing
- [ ] CI/CD pipeline green
- [ ] Critical patterns >85%

### Should Have
- [ ] 82% overall coverage
- [ ] Performance tests
- [ ] Integration test suite
- [ ] Coverage trending

### Nice to Have
- [ ] 85% overall coverage
- [ ] Mutation testing
- [ ] Property-based tests
- [ ] Coverage by feature

## Risk Mitigation

### Risk 1: Time Constraints
**Mitigation**: Focus on high-impact, low-effort improvements first

### Risk 2: Breaking Changes
**Mitigation**: Extensive use of mocks, avoid changing production code

### Risk 3: Test Complexity
**Mitigation**: Simple unit tests first, complex integration tests later

### Risk 4: Coverage Gaming
**Mitigation**: Focus on meaningful tests, not just line coverage

## Daily Tracking

### Day 1 (Sep 26)
- [ ] Morning: Fix validate tests
- [ ] Afternoon: Fix migrate tests
- [ ] Evening: Update progress

### Day 2 (Sep 27)
- [ ] Morning: Fix merge_content tests
- [ ] Afternoon: Fix critical pattern tests
- [ ] Evening: Milestone 1 review

### Day 3 (Sep 28)
- [ ] Morning: Quality module tests
- [ ] Afternoon: Main entry tests
- [ ] Evening: Coverage check

### Day 4 (Sep 29)
- [ ] Morning: Config module tests
- [ ] Afternoon: Integration tests
- [ ] Evening: Milestone 2 review

### Days 5-10
- Continue per milestone plan
- Daily coverage checks
- Adjust based on progress

## Commands Reference

```bash
# Run all tests with coverage
python3 -m pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
python3 -m pytest --cov=. --cov-report=html

# Run specific test file
python3 -m pytest tests/test_example.py -xvs

# Check coverage for specific module
python3 -m pytest --cov=aget.quality tests/

# Run only failing tests
python3 -m pytest --lf

# Run tests in parallel (if pytest-xdist installed)
python3 -m pytest -n auto

# Profile slow tests
python3 -m pytest --durations=10
```

## Automation Setup

```yaml
# .github/workflows/coverage.yml
name: Coverage Check
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install pytest pytest-cov
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
        with:
          fail_ci_if_error: true
          minimum_coverage: 80
```

## Next Actions

1. **Immediate** (Today):
   - Fix the 46 failing tests
   - Set up coverage tracking

2. **Tomorrow**:
   - Begin Milestone 1 tasks
   - Create quality module tests

3. **This Week**:
   - Achieve 75% coverage
   - Complete Milestones 1-2

4. **Next Week**:
   - Push to 80% coverage
   - Prepare v2.0 release

---

*Plan created: 2025-09-25*
*Target completion: October 7, 2025*
*Success metric: 80% test coverage with all tests passing*