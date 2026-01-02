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


def _save_note_impl(content: str) -> str:
    """Mock implementation of save_note tool (Phase 1 placeholder).

    Extracts the title from the first line of content (expected format: "title: <name>")
    and returns a mock success message. Does not actually save files yet.

    Args:
        content: Note content where first line should be "title: <note name>"

    Returns:
        Mock success message indicating the note was "saved"

    Example:
        >>> _save_note_impl(r"title: Python Basics\nPython is a programming language")
        "MOCK SAVE: Note 'Python Basics' saved successfully"
        >>> _save_note_impl("Python is a programming language")
        "MOCK SAVE: Note 'Python is a programming language' saved successfully"
        >>> _save_note_impl("")
        "MOCK SAVE: Note '' saved successfully"
    """
    # Split into first line (title) and rest (max 2 parts)
    lines = content.split("\n", 1)
    # Note: split() always returns at least [''], so 'else "untitled"' is unreachable
    # Kept as defensive programming for potential future changes
    title = lines[0].replace("title:", "").strip() if lines else "untitled"
    return f"MOCK SAVE: Note '{title}' saved successfully"


def get_save_note_tool() -> Tool:
    """Returns the save_note tool."""
    return Tool(
        name="save_note",
        description="Save a note with title and content",
        function=_save_note_impl,
    )


def get_all_tools() -> list[Tool]:
    """Returns all available tools."""
    return [
        get_search_web_tool(),
        get_save_note_tool(),
    ]
