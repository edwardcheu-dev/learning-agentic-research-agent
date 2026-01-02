# Scripts Directory

Utility scripts for testing, validation, and tooling.

## Available Scripts

### test_poe_models.py

Comprehensive POE API model testing and comparison script.

**Purpose**: Test multiple POE API models before changing `MODEL_NAME` in config.

**Usage**:
```bash
# Run from project root
uv run python scripts/test_poe_models.py
```

**What it does**:
- Tests model availability (does it exist on POE?)
- Validates ReAct format compliance (Thought/Action/Observation)
- Measures reliability (success rate across queries)
- Calculates performance (response time, token usage)
- Generates comparison report

**Output**:
- Report: `docs/model-comparison-YYYY-MM-DD.md`
- Logs: `test-api-calls.log`, `api-call-audit.log`

**⚠️ Warning**: Makes real API calls (costs money!)

---

## When to Use Scripts

### Before Changing Models

**Scenario**: You want to change `MODEL_NAME` from `gpt-5.1` to `gpt-4.1`

**TDD Workflow**:

1. **Test the new model first**:
   ```bash
   uv run python scripts/test_poe_models.py
   ```

2. **Review the generated report**:
   ```bash
   cat docs/model-comparison-$(date +%Y-%m-%d).md
   ```

3. **Check if new model passes**:
   - ✅ Available (no 404 errors)
   - ✅ ReAct compliance ≥ 80%
   - ✅ Reliability ≥ 50%
   - ✅ No timeout issues

4. **If tests pass, update config**:
   ```python
   # src/config.py
   MODEL_NAME: str = "gpt-4.1"
   ```

5. **Update test assertions**:
   ```python
   # tests/test_config.py
   def test_config_has_model_name():
       assert MODEL_NAME == "gpt-4.1"
   ```

6. **Run integration tests**:
   ```bash
   ALLOW_INTEGRATION_TESTS=1 uv run pytest -m integration -v
   ```

7. **Run full test suite**:
   ```bash
   uv run pytest -v
   ```

8. **Commit changes**:
   ```bash
   git add src/config.py tests/test_config.py docs/model-comparison-*.md
   git commit -m "feat: change model to gpt-4.1 after validation"
   ```

---

## Configuration

### test_poe_models.py Configuration

Edit the script to customize:

```python
# Models to test
MODELS_TO_TEST = [
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-5.1",
    "gpt4_o_mini",
]

# Test queries
TEST_QUERIES = [
    "Use search_web to find Python info",
    "What is machine learning?",
    "Explain quantum computing",
]

# Pass/fail thresholds
REACT_THRESHOLD = 0.80  # 80% must have Thought/Action
RELIABILITY_THRESHOLD = 0.50  # 50% success rate minimum
```

---

## Understanding Output

### Sample Report Structure

```markdown
# POE API Model Comparison - 2026-01-02

## Executive Summary
Recommended Model: gpt-5.1

## Test Results

| Model | Available | ReAct | Reliability | Grade |
|-------|-----------|-------|-------------|-------|
| gpt-5.1 | ✅ | 100% | 67% | A |
| gpt-4.1 | ✅ | 100% | 100% | A+ |
| gpt4_o_mini | ✅ | 100% | 100% | A |

## Detailed Findings
[...]
```

### Interpreting Grades

- **A+**: Perfect (100% across all metrics)
- **A**: Excellent (≥80% ReAct, ≥50% reliability)
- **B**: Good (≥60% ReAct, ≥30% reliability)
- **C**: Marginal (below recommended thresholds)
- **F**: Failed (unavailable or critical issues)

---

## Cost Considerations

### API Call Costs

Each test run makes approximately:
- **3-5 API calls per model** (availability, format, reliability tests)
- **Testing 5 models** = ~25 API calls
- **Comprehensive test** = ~$0.10-0.50 (estimate)

**Best Practice**: Run tests when needed, not frequently.

### When to Run Tests

✅ **Do run tests**:
- Before changing `MODEL_NAME` in production
- After POE API announces new models
- When experiencing model issues
- Before major releases

❌ **Don't run tests**:
- On every commit
- During development of unrelated features
- Just to "check" without purpose

---

## Troubleshooting

### Script Fails with "Model not found"

**Problem**: POE API doesn't recognize model name

**Solution**:
1. Check POE API documentation for correct model names
2. Try alternative naming (e.g., `gpt-4.1` vs `gpt4-1`)
3. Update `MODELS_TO_TEST` list in script

### Script Times Out

**Problem**: Model is slow or unavailable

**Solution**:
1. Increase timeout in script (default: 20s)
2. Try again later (POE API may be experiencing issues)
3. Check POE status page

### ReAct Compliance is Low

**Problem**: Model doesn't follow Thought/Action format

**Solution**:
1. Review system prompt in script
2. Test with different queries
3. Consider using a different model
4. Update docs/reference/poe-api-troubleshooting.md with findings

---

## Safety Features

Scripts in this directory:
- ❌ Are NOT run by pre-commit hooks
- ❌ Are NOT run by pytest automatically
- ✅ Must be run manually
- ✅ Generate reports for review
- ✅ Log all API calls to audit trail

This ensures scripts never make unexpected API calls.

---

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - AI agent context for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Main project documentation
- **[../docs/reference/poe-api-troubleshooting.md](../docs/reference/poe-api-troubleshooting.md)** - Detailed POE API guide

---

## Adding New Scripts

To add a new script:

1. Create script in `scripts/` directory
2. Update this README.md with usage instructions
3. Update CLAUDE.md with AI agent context
4. Add to main CLAUDE.md if important for workflow
5. Test manually before committing
6. Document expected input/output

---

**Last Updated**: January 2, 2026
