# Code Quality Analysis Example

Demonstrates the `code_quality.py` pattern for analyzing code quality metrics.

## Files

- `sample_code.py` - Sample Python code with quality issues (high complexity, technical debt, code smells)
- `run_analysis.py` - Script that runs code_quality pattern analysis

## Usage

```bash
cd examples/code_quality_analysis
python3 run_analysis.py
```

## Expected Output

The analysis identifies:

1. **Cyclomatic Complexity**: `calculate_total()` has high complexity (>10) due to deeply nested conditionals
2. **Maintainability Index**: Likely "fair" or "poor" (<65) due to complexity
3. **Technical Debt**: 2 TODO/FIXME comments
4. **Code Smells**:
   - Long method (calculate_total)
   - High complexity function
   - Nested conditionals (7+ levels deep)

## Learning Points

- Cyclomatic complexity measures decision points (if/for/while/and/or)
- High complexity (>10) indicates code that's hard to test and maintain
- Maintainability index combines complexity, LOC, and other factors
- Technical debt comments (TODO/FIXME) should be tracked and addressed
- Code smells are indicators of deeper design issues

## Recommended Fixes

For `calculate_total()`:
1. Extract pricing logic into separate functions
2. Use strategy pattern for country/currency pricing
3. Move member/discount logic to separate calculator
4. Address TODO/FIXME items
