"""Tests for audit log service behaviour."""

from homesteados.core.domain.enums import DeviceState
from homesteados.core.events.event import Event
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType
from homesteados.core.services.audit_log_service import AuditLogService
from homesteados.runtime import create_demo_runtime


def test_audit_log_service_records_published_event():
    event_bus = EventBus()
    audit_log_service = AuditLogService(event_bus=event_bus)
    audit_log_service.start()

    event = Event(
        event_type=EventType.ACTION_REQUESTED,
        source="test",
        payload={
            "action_type": "turn_on",
            "target_id": "light.office.ceiling",
            "requested_by": "test",
        },
    )

    event_bus.publish(event)

    entries = audit_log_service.list_entries()

    assert len(entries) == 1
    assert entries[0].event_id == event.id
    assert "Action requested" in entries[0].message


def test_runtime_audit_log_records_lighting_action():
    runtime = create_demo_runtime()

    runtime.lighting_service.turn_on_light(
        "light.office.ceiling",
        requested_by="test",
    )

    entries = runtime.audit_log_service.list_entries()
    messages = [
        entry.message
        for entry in entries
    ]

    assert any("Action requested" in message for message in messages)
    assert any("Action completed" in message for message in messages)
    assert any("Device state changed" in message for message in messages)

    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert light is not None
    assert light.state == DeviceState.ON


def test_audit_log_service_can_clear_entries():
    event_bus = EventBus()
    audit_log_service = AuditLogService(event_bus=event_bus)
    audit_log_service.start()

    event_bus.publish(
        Event(
            event_type=EventType.ACTION_COMPLETED,
            source="test",
        )
    )

    audit_log_service.clear()

    assert audit_log_service.list_entries() == []