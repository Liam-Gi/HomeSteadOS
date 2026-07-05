"""Tests for lighting service event publishing."""

from homesteados.adapters.simulated.simulated_device_adapter import (
    SimulatedDeviceAdapter,
)
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceState, DeviceType
from homesteados.core.events.event_bus import EventBus
from homesteados.core.events.event_types import EventType
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService


def create_lighting_service_with_events() -> tuple[LightingService, EventBus, Device]:
    device_registry = DeviceRegistry()
    adapter_registry = AdapterRegistry()
    event_bus = EventBus()

    adapter_registry.register_adapter(SimulatedDeviceAdapter())

    light = Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        state=DeviceState.OFF,
    )

    device_registry.register_device(light)

    service = LightingService(
        device_registry=device_registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
    )

    return service, event_bus, light


def test_lighting_service_publishes_action_requested_event():
    service, event_bus, _ = create_lighting_service_with_events()

    service.turn_on_light("light.office.ceiling")

    event_types = [
        event.event_type
        for event in event_bus.list_published_events()
    ]

    assert EventType.ACTION_REQUESTED in event_types


def test_lighting_service_publishes_action_completed_event():
    service, event_bus, _ = create_lighting_service_with_events()

    service.turn_on_light("light.office.ceiling")

    event_types = [
        event.event_type
        for event in event_bus.list_published_events()
    ]

    assert EventType.ACTION_COMPLETED in event_types


def test_lighting_service_publishes_device_state_changed_event():
    service, event_bus, _ = create_lighting_service_with_events()

    service.turn_on_light("light.office.ceiling")

    state_change_events = [
        event
        for event in event_bus.list_published_events()
        if event.event_type == EventType.DEVICE_STATE_CHANGED
    ]

    assert len(state_change_events) == 1
    assert state_change_events[0].payload["device_id"] == "light.office.ceiling"
    assert state_change_events[0].payload["previous_state"] == "off"
    assert state_change_events[0].payload["new_state"] == "on"


def test_lighting_service_does_not_publish_state_change_when_state_unchanged():
    service, event_bus, light = create_lighting_service_with_events()
    light.set_state(DeviceState.ON)

    service.turn_on_light("light.office.ceiling")

    state_change_events = [
        event
        for event in event_bus.list_published_events()
        if event.event_type == EventType.DEVICE_STATE_CHANGED
    ]

    assert state_change_events == []