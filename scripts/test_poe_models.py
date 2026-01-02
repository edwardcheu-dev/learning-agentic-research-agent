"""Comprehensive POE API model testing script.

This script tests multiple POE API models and generates a comparison report.

Usage:
    uv run python scripts/test_poe_models.py

Output:
    docs/model-comparison-{date}.md

WARNING: Makes real API calls (costs money!)
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import openai

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import API_BASE_URL, DEFAULT_MAX_TOKENS, get_api_key

# Configuration
MODELS_TO_TEST = [
    ("gpt-5.1", "GPT-5.1 (current default)"),
    ("gpt-4.1", "GPT-4.1"),
    ("gpt-4.1-mini", "GPT-4.1 Mini"),
    ("gpt4_o_mini", "GPT-4o Mini (fallback)"),
]

TEST_QUERIES = [
    "Use search_web to find information about Python programming",
    "What is machine learning? Use search_web to find out.",
    "Search for the latest features in Rust programming language",
]

# Pass/fail thresholds
REACT_THRESHOLD = 0.80  # 80% must have Thought/Action
RELIABILITY_THRESHOLD = 0.50  # 50% success rate minimum

# ReAct system prompt
REACT_PROMPT = """You are a ReAct (Reasoning and Acting) agent.

Answer the user's question by following this format:

Thought: [Your reasoning about what to do next]
Action: [tool_name: input]
Observation: [Result from the tool]
... (repeat Thought/Action/Observation as needed)
Answer: [Final answer to the user's question]

Available tools:
- search_web: Search the web for information

Always start with a Thought, then take an Action."""


def test_model_availability(client: openai.OpenAI, model: str) -> dict[str, Any]:
    """Test if model is available on POE API.

    Args:
        client: OpenAI client
        model: Model name to test

    Returns:
        dict with 'available', 'error', 'response_time' keys
    """
    import time

    print("  Testing availability... ", end="", flush=True)

    try:
        start = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a test assistant."},
                {"role": "user", "content": "Say 'test' and nothing else."},
            ],
            max_tokens=50,
            timeout=10,
        )
        elapsed = time.time() - start

        result = response.choices[0].message.content
        print(f"✅ ({elapsed:.2f}s)")

        return {
            "available": True,
            "error": None,
            "response_time": elapsed,
            "result": result,
        }

    except Exception as e:
        error_msg = str(e)[:100]
        print(f"❌ {error_msg}")
        return {
            "available": False,
            "error": error_msg,
            "response_time": None,
            "result": None,
        }


def test_react_compliance(client: openai.OpenAI, model: str) -> dict[str, Any]:
    """Test if model follows ReAct format.

    Args:
        client: OpenAI client
        model: Model name to test

    Returns:
        dict with 'compliant', 'has_thought', 'has_action', 'response' keys
    """
    print("  Testing ReAct format... ", end="", flush=True)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": REACT_PROMPT},
                {"role": "user", "content": TEST_QUERIES[0]},
            ],
            max_tokens=DEFAULT_MAX_TOKENS,
            timeout=20,
        )

        result = response.choices[0].message.content
        has_thought = "Thought:" in result
        has_action = "Action:" in result
        compliant = has_thought and has_action

        status = "✅" if compliant else "❌"
        print(f"{status} (Thought: {has_thought}, Action: {has_action})")

        return {
            "compliant": compliant,
            "has_thought": has_thought,
            "has_action": has_action,
            "response": result[:200],
        }

    except Exception as e:
        error_msg = str(e)[:100]
        print(f"❌ {error_msg}")
        return {
            "compliant": False,
            "has_thought": False,
            "has_action": False,
            "response": f"ERROR: {error_msg}",
        }


def test_reliability(client: openai.OpenAI, model: str) -> dict[str, Any]:
    """Test model reliability across multiple queries.

    Args:
        client: OpenAI client
        model: Model name to test

    Returns:
        dict with 'success_rate', 'successes', 'total', 'failures' keys
    """
    print("  Testing reliability... ", end="", flush=True)

    successes = 0
    failures = []

    for i, query in enumerate(TEST_QUERIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": REACT_PROMPT},
                    {"role": "user", "content": query},
                ],
                max_tokens=DEFAULT_MAX_TOKENS,
                timeout=20,
            )

            result = response.choices[0].message.content
            if result and len(result) > 0:
                successes += 1
            else:
                failures.append(f"Query {i+1}: Empty response")

        except Exception as e:
            error_msg = str(e)[:50]
            failures.append(f"Query {i+1}: {error_msg}")

    success_rate = successes / len(TEST_QUERIES)
    print(f"{successes}/{len(TEST_QUERIES)} ({success_rate:.0%})")

    return {
        "success_rate": success_rate,
        "successes": successes,
        "total": len(TEST_QUERIES),
        "failures": failures,
    }


def calculate_grade(results: dict[str, Any]) -> str:
    """Calculate letter grade based on test results.

    Args:
        results: Combined test results

    Returns:
        Letter grade (A+, A, B, C, F)
    """
    if not results["availability"]["available"]:
        return "F"

    react_score = 1.0 if results["react"]["compliant"] else 0.0
    reliability_score = results["reliability"]["success_rate"]

    # Weighted average: ReAct 60%, Reliability 40%
    overall = (react_score * 0.6) + (reliability_score * 0.4)

    if overall >= 0.95:
        return "A+"
    elif overall >= 0.80:
        return "A"
    elif overall >= 0.60:
        return "B"
    elif overall >= 0.40:
        return "C"
    else:
        return "F"


def generate_report(all_results: dict[str, dict[str, Any]]) -> str:
    """Generate markdown comparison report.

    Args:
        all_results: Results for all tested models

    Returns:
        Markdown formatted report
    """
    date_str = datetime.now().strftime("%Y-%m-%d")

    report = f"""# POE API Model Comparison - {date_str}

Generated by: `scripts/test_poe_models.py`

## Executive Summary

"""

    # Find recommended model (highest grade, prefer current if tied)
    best_model = None
    best_grade = "F"
    for model, results in all_results.items():
        grade = calculate_grade(results)
        if grade > best_grade or (grade == best_grade and "gpt-5.1" in model):
            best_model = model
            best_grade = grade

    report += f"**Recommended Model**: `{best_model}` (Grade: {best_grade})\n\n"

    # Summary table
    report += "## Test Results Summary\n\n"
    report += "| Model | Available | ReAct Compliant | Reliability | Grade |\n"
    report += "|-------|-----------|-----------------|-------------|-------|\n"

    for model, results in all_results.items():
        avail = "✅" if results["availability"]["available"] else "❌"
        react = "✅" if results["react"]["compliant"] else "❌"
        reliability = f"{results['reliability']['success_rate']:.0%}"
        grade = calculate_grade(results)

        report += f"| {model} | {avail} | {react} | {reliability} | {grade} |\n"

    report += "\n"

    # Detailed results
    report += "## Detailed Results\n\n"

    for model, results in all_results.items():
        report += f"### {model}\n\n"

        # Availability
        avail = results["availability"]
        if avail["available"]:
            report += (
                f"- **Availability**: ✅ Available ({avail['response_time']:.2f}s)\n"
            )
        else:
            report += f"- **Availability**: ❌ Failed - {avail['error']}\n"

        # ReAct
        react = results["react"]
        if react["compliant"]:
            report += (
                f"- **ReAct Format**: ✅ Compliant "
                f"(Thought: {react['has_thought']}, "
                f"Action: {react['has_action']})\n"
            )
        else:
            report += (
                f"- **ReAct Format**: ❌ Non-compliant "
                f"(Thought: {react['has_thought']}, "
                f"Action: {react['has_action']})\n"
            )

        # Reliability
        rel = results["reliability"]
        success_rate = f"{rel['success_rate']:.0%}"
        report += (
            f"- **Reliability**: {rel['successes']}/{rel['total']} "
            f"({success_rate})\n"
        )

        if rel["failures"]:
            report += "- **Failures**:\n"
            for failure in rel["failures"]:
                report += f"  - {failure}\n"

        report += f"- **Overall Grade**: {calculate_grade(results)}\n\n"

        # Sample response
        if react["response"]:
            report += (
                f"**Sample Response** (first 200 chars):\n"
                f"```\n{react['response']}\n```\n\n"
            )

    # Recommendations
    report += "## Recommendations\n\n"

    passing_models = [
        model
        for model, results in all_results.items()
        if results["availability"]["available"]
        and results["react"]["compliant"]
        and results["reliability"]["success_rate"] >= RELIABILITY_THRESHOLD
    ]

    if passing_models:
        report += "**Models that pass all tests**:\n"
        for model in passing_models:
            grade = calculate_grade(all_results[model])
            report += f"- `{model}` (Grade: {grade})\n"
    else:
        report += "⚠️ **No models passed all tests**. Review individual results above.\n"

    report += "\n"

    # Methodology
    report += "## Test Methodology\n\n"
    report += "- **Availability Test**: Simple API call with timeout\n"
    report += (
        "- **ReAct Compliance**: Check for 'Thought:' and 'Action:' " "in response\n"
    )
    threshold = f"{RELIABILITY_THRESHOLD:.0%}"
    report += (
        f"- **Reliability Test**: {len(TEST_QUERIES)} queries, "
        f"success rate ≥ {threshold}\n"
    )
    report += "- **Grading**: ReAct (60%) + Reliability (40%)\n\n"

    report += "## Test Queries\n\n"
    for i, query in enumerate(TEST_QUERIES, 1):
        report += f"{i}. {query}\n"

    report += "\n---\n\n"
    report += f"**Generated**: {datetime.now().isoformat()}\n"
    report += "**Script**: scripts/test_poe_models.py\n"

    return report


def main():
    """Run comprehensive model tests and generate report."""
    print("=" * 70)
    print("POE API Model Comparison Test")
    print("=" * 70)
    print()
    print(f"Testing {len(MODELS_TO_TEST)} models with {len(TEST_QUERIES)} queries each")
    print("⚠️  This will make real API calls (costs money!)")
    print()

    # Create client
    try:
        client = openai.OpenAI(
            api_key=get_api_key(),
            base_url=API_BASE_URL,
        )
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    # Test each model
    all_results = {}

    for model, description in MODELS_TO_TEST:
        print(f"\n📊 Testing: {model}")
        print(f"   ({description})")

        results = {
            "availability": test_model_availability(client, model),
            "react": test_react_compliance(client, model),
            "reliability": test_reliability(client, model),
        }

        all_results[model] = results

    # Generate report
    print("\n" + "=" * 70)
    print("Generating Report...")
    print("=" * 70)

    report = generate_report(all_results)

    # Save report
    output_dir = Path(__file__).parent.parent / "docs"
    output_dir.mkdir(exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"model-comparison-{date_str}.md"

    with open(output_file, "w") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {output_file}")
    print("\nTo view report:")
    print(f"  cat {output_file}")
    print()


if __name__ == "__main__":
    main()
