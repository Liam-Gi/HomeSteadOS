"""Tests for the HomeSteadOS event bus."""

from homesteados.core.events.event import Event
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType


def test_event_bus_stores_published_events():
    event_bus = EventBus()
    event = Event(
        event_type=EventType.ACTION_REQUESTED,
        source="test",
        payload={"action_id": "123"},
    )

    event_bus.publish(event)

    assert event in event_bus.list_published_events()


def test_event_bus_notifies_specific_subscriber():
    event_bus = EventBus()
    received_events: list[Event] = []

    event_bus.subscribe(
        EventType.DEVICE_STATE_CHANGED,
        received_events.append,
    )

    event = Event(
        event_type=EventType.DEVICE_STATE_CHANGED,
        source="test",
        payload={"device_id": "light.office.ceiling"},
    )

    event_bus.publish(event)

    assert received_events == [event]


def test_event_bus_notifies_global_subscriber():
    event_bus = EventBus()
    received_events: list[Event] = []

    event_bus.subscribe_all(received_events.append)

    event = Event(
        event_type=EventType.ACTION_COMPLETED,
        source="test",
    )

    event_bus.publish(event)

    assert received_events == [event]


def test_event_bus_clear_removes_event_history():
    event_bus = EventBus()
    event = Event(
        event_type=EventType.ACTION_REQUESTED,
        source="test",
    )

    event_bus.publish(event)
    event_bus.clear()

    assert event_bus.list_published_events() == []