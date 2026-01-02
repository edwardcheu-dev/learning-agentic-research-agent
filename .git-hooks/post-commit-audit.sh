#!/bin/bash
# Post-commit hook: Detect if API calls were made during commit process
#
# This is a safety net to detect if integration tests accidentally ran
# during pre-commit hooks, which would indicate a configuration error.
#
# Exit codes:
#   0 - No API calls detected (success)
#   1 - API calls detected (safety net violation)

AUDIT_LOG="api-call-audit.log"

# Check if audit log exists and has recent entries
if [ -f "$AUDIT_LOG" ]; then
    # Check if file was modified in the last 2 minutes
    if [ "$(uname)" = "Darwin" ]; then
        # macOS
        LAST_MODIFIED=$(stat -f "%m" "$AUDIT_LOG" 2>/dev/null || echo "0")
    else
        # Linux
        LAST_MODIFIED=$(stat -c "%Y" "$AUDIT_LOG" 2>/dev/null || echo "0")
    fi

    CURRENT_TIME=$(date +%s)
    TIME_DIFF=$((CURRENT_TIME - LAST_MODIFIED))

    # If file was modified in last 120 seconds (2 minutes)
    if [ "$TIME_DIFF" -lt 120 ]; then
        # Count lines in audit log
        LINE_COUNT=$(wc -l < "$AUDIT_LOG" 2>/dev/null || echo "0")

        if [ "$LINE_COUNT" -gt 0 ]; then
            echo ""
            echo "=========================================="
            echo "⚠️  WARNING: API CALL SAFETY NET TRIGGERED"
            echo "=========================================="
            echo ""
            echo "Detected API call(s) during commit process!"
            echo "This should NOT happen during pre-commit hooks."
            echo ""
            echo "Recent API calls:"
            tail -n 5 "$AUDIT_LOG"
            echo ""
            echo "❌ SAFETY NET VIOLATION"
            echo "💡 This indicates a configuration error in:"
            echo "   - .pre-commit-config.yaml (should skip integration tests)"
            echo "   - pyproject.toml (should have addopts = -m 'not integration')"
            echo "   - tests/conftest.py (should block integration tests)"
            echo ""
            echo "To fix:"
            echo "  1. Review .pre-commit-config.yaml"
            echo "  2. Ensure entry: uv run pytest -m \"not integration\""
            echo "  3. Delete $AUDIT_LOG and try again"
            echo ""
            echo "=========================================="

            # Don't fail the commit, just warn
            # (commit already happened, this is post-commit)
            exit 0
        fi
    fi
fi

# No recent API calls detected - success!
exit 0
