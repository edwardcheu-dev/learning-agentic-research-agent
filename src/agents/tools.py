"""Tool interface and placeholder implementations for Phase 1."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    """Represents a tool the agent can use."""

    name: str
    description: str
    function: Callable[[str], str]


def _search_web_impl(query: str) -> str:
    """Placeholder implementation of web search."""
    return (
        f"MOCK SEARCH RESULTS for '{query}':\n"
        f"1. Example result about {query}\n"
        f"2. Another result for {query}"
    )


def get_search_web_tool() -> Tool:
    """Returns the search_web tool."""
    return Tool(
        name="search_web",
        description="Search the web for information about a query",
        function=_search_web_impl,
    )
