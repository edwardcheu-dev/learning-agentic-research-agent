"""Tests for TUI event system."""

from src.tui.events import AgentEvent


def test_agent_event_has_required_attributes():
    """Test that AgentEvent has type, content, and metadata attributes."""
    event = AgentEvent(type="token", content="Hello", metadata={"step": 1})

    assert event.type == "token"
    assert event.content == "Hello"
    assert event.metadata == {"step": 1}


def test_agent_event_metadata_defaults_to_empty_dict():
    """Test that AgentEvent metadata defaults to empty dict if not provided."""
    event = AgentEvent(type="thought", content="Thinking...")

    assert event.type == "thought"
    assert event.content == "Thinking..."
    assert event.metadata == {}


def test_agent_event_supports_different_event_types():
    """Test that AgentEvent supports all expected event types."""
    event_types = ["thought", "action", "observation", "answer", "token"]

    for event_type in event_types:
        event = AgentEvent(type=event_type, content="test")
        assert event.type == event_type
