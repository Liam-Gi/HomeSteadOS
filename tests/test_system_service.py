"""Tests for system service behaviour."""

from homesteados.core.domain.enums import SystemMode
from homesteados.core.events.event_types import EventType
from homesteados.runtime import create_runtime


def test_system_service_defaults_to_home_mode():
    runtime = create_runtime()

    assert runtime.system_service.get_mode() == SystemMode.HOME


def test_system_service_can_set_away_mode():
    runtime = create_runtime()

    result = runtime.system_service.set_mode(
        SystemMode.AWAY,
        updated_by="test",
    )

    assert result.success is True
    assert runtime.system_service.get_mode() == SystemMode.AWAY
    assert runtime.system_state.updated_by == "test"


def test_system_service_rejects_unknown_mode():
    runtime = create_runtime()

    result = runtime.system_service.set_mode("invalid_mode")

    assert result.success is False
    assert "Unsupported system mode" in result.message


def test_system_service_publishes_mode_changed_event():
    runtime = create_runtime()

    runtime.system_service.set_mode(SystemMode.NIGHT, updated_by="test")

    events = runtime.event_bus.list_published_events()

    event_types = [
        event.event_type
        for event in events
    ]

    assert EventType.SYSTEM_MODE_CHANGED in event_types