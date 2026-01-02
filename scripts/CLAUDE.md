# Scripts Directory - AI Agent Context

> **For complete script usage**, see [README.md](README.md)
> **For project context**, see [../CLAUDE.md](../CLAUDE.md)

**This file provides AI-essential context only. See README.md for comprehensive documentation.**

---

## Purpose

The `scripts/` directory contains utility scripts for testing, validation, and tooling that are NOT part of the main application.

**Key Principle**: Scripts here are standalone tools, not application code.

---

## Available Scripts

### test_poe_models.py

**Purpose**: Comprehensive POE API model testing and comparison

**Type**: Manual execution tool (not run by pytest or pre-commit)

**When to Run**:
- Before changing `MODEL_NAME` in `src/config.py`
- When POE API adds new models
- To validate model performance after POE API updates
- To troubleshoot model-related issues
- To generate comparison reports for documentation

**Usage**:
```bash
# Run from project root (uses cache by default)
uv run python scripts/test_poe_models.py

# Force retest all models (ignore cache, makes API calls)
uv run python scripts/test_poe_models.py --force-retest
```

**Key Points for AI**:
- Uses **pydantic-validated cache** at `data/model-test-cache.json`
- Default: uses cache (no API calls, FREE)
- `--force-retest`: bypasses cache (makes API calls, costs money)
- Generates report in `docs/model-comparison-{date}.md`
- Tests: availability, ReAct compliance, reliability, performance

**For complete workflow**, see [README.md#when-to-use-scripts](README.md#when-to-use-scripts)

**Important Notes**:
- ⚠️ Makes REAL API calls (costs money!)
- ⚠️ Not run by pre-commit hooks
- ⚠️ Not run by pytest automatically
- ✅ Safe to run manually anytime

---

## Integration with Project

### Relationship to Tests

| Location | Purpose | Run By | Makes API Calls |
|----------|---------|--------|-----------------|
| `tests/` | Unit & integration tests | pytest, pre-commit | Only with ALLOW_INTEGRATION_TESTS=1 |
| `scripts/` | Standalone validation tools | Manual execution | Yes (when run manually) |

**Key Difference**:
- `tests/` = Automated testing (TDD, CI/CD)
- `scripts/` = Manual tools (validation, reports)

### When Scripts Run

- ❌ **NOT** run by pre-commit hooks
- ❌ **NOT** run by `pytest` automatically
- ❌ **NOT** part of CI/CD pipeline
- ✅ Run **manually** before major changes
- ✅ Run when **validating new models**
- ✅ Run when **generating reports**

---

## Safety Considerations

### API Call Costs

Scripts in this directory may make expensive API calls:
- Each model test = 3-5 API calls per model
- Comprehensive test of 5 models = ~25 API calls
- Costs accumulate with POE API usage

**Best Practice**: Only run when needed, not on every change.

### Script Execution Safety

- Scripts are NOT sandboxed
- Scripts can modify files in `docs/`
- Scripts can consume API quota
- Always review script code before running

### Data Generated

Scripts may generate:
- Log files (`*.log`)
- Report files (`docs/model-comparison-*.md`)
- Audit trails (`api-call-audit.log`)

All log files are gitignored. Reports should be committed for historical reference.

---

## Adding New Scripts

When adding a new script to this directory:

1. **Update this CLAUDE.md file** with script purpose and usage
2. **Update README.md** with human-readable documentation
3. **Add to .gitignore** if script generates logs or temporary files
4. **Document in main CLAUDE.md** if script is important for workflow
5. **Test manually** before committing

---

## Important Context for AI Agents

### When Working in scripts/

If you're asked to create or modify scripts:

1. **Check if it belongs here**: Scripts for validation/tooling only
2. **Check if it belongs in tests/**: If it's automated testing, use `tests/`
3. **Check if it belongs in src/**: If it's application code, use `src/`

### Scripts vs Tests

- **Script**: Manual tool, generates reports, not part of TDD
- **Test**: Automated validation, part of TDD, run by pytest

### Scripts vs Application Code

- **Script**: Standalone utility, run manually, not imported
- **Application Code**: Part of main app, imported by other modules

---

## Quick Reference

### Run Model Testing
```bash
uv run python scripts/test_poe_models.py
```

### Review Latest Report
```bash
ls -t docs/model-comparison-*.md | head -1 | xargs cat
```

### Check API Call Audit
```bash
cat api-call-audit.log
```

### Clean Up Logs
```bash
rm -f test-api-calls.log api-call-audit.log
```

---

## Related Documentation

- **[README.md](README.md)** - Human-readable script documentation
- **[../CLAUDE.md](../CLAUDE.md)** - Main project documentation for AI agents
- **[../docs/reference/poe-api-troubleshooting.md](../docs/reference/poe-api-troubleshooting.md)** - POE API model selection guide

---
