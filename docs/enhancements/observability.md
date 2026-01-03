# Observability Enhancements

Improvements related to tracing, logging, monitoring, and debugging.

## Current State (Phase 1)

- No structured logging (just print statements in REPL)
- No tracing of LLM calls or tool executions
- No performance metrics
- Debugging requires reading full conversation output
- No cost tracking (token usage)

## Enhancements

### Add Structured Logging with structlog [P1] [Idea]

**Problem**: Print statements don't scale - hard to filter, search, or analyze agent behavior

**Proposed Solution**:
- Use [structlog](https://www.structlog.org/) for structured logging
- Log key events: LLM calls, tool executions, errors
- Include context: iteration number, tool name, execution time
- Support multiple output formats (JSON for analysis, pretty-print for debugging)

**Benefits**:
- Filterable logs (e.g., show only tool executions)
- Searchable (e.g., find all "search_web" calls)
- Analyzable (e.g., aggregate execution times)
- Production-ready (can ship to log aggregation systems)

**Considerations**:
- Adds dependency
- Need logging configuration management
- May increase output verbosity
- PII concerns (log sanitization needed)

**References**:
- [structlog documentation](https://www.structlog.org/)

---

### Implement LLM Call Tracing with MLflow [P2] [Idea]

**Problem**: No visibility into LLM call patterns, costs, or performance

**Proposed Solution**:
- Use [MLflow Tracing](https://mlflow.org/docs/latest/llms/tracing/index.html)
- Trace each LLM call with inputs, outputs, latency, tokens
- Track tool execution spans
- Generate trace visualizations (waterfall diagrams)

**Benefits**:
- Understand agent execution flow visually
- Identify bottlenecks (slow tools, long LLM calls)
- Track costs (token usage per query)
- Debug failures (see exact inputs/outputs)

**Considerations**:
- Requires MLflow server setup
- Storage costs for traces
- Performance overhead (minimal)
- Need to sanitize sensitive data in traces

**References**:
- [MLflow Tracing docs](https://mlflow.org/docs/latest/llms/tracing/index.html)
- [OpenTelemetry integration](https://mlflow.org/docs/latest/llms/tracing/opentelemetry.html)

---

### Add Cost Tracking Dashboard [P2] [Idea]

**Problem**: No visibility into API costs - easy to overspend during development

**Proposed Solution**:
- Track token usage per LLM call
- Calculate cost using model pricing
- Display cumulative costs in REPL footer
- Alert on budget thresholds

**Benefits**:
- Budget awareness
- Identify expensive queries
- Optimize prompt length
- Prevent runaway costs

**Considerations**:
- Pricing data needs updates when models change
- Need to handle different models (search, embeddings, etc.)
- Privacy concerns (don't log API keys)

**Example**:
```python
# After each LLM call:
tokens_used = response.usage.total_tokens
cost = calculate_cost(MODEL_NAME, tokens_used)
print(f"💰 Cost this query: ${cost:.4f} | Total session: ${session_cost:.2f}")
```

---

### Add to Enhancement List

(Template for new ideas)
