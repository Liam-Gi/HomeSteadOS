"""Tests for room service behaviour."""

from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceState, DeviceType
from homesteados.runtime import create_demo_runtime
from homesteados.core.domain.room import Room


def test_room_service_lists_devices_in_room():
    runtime = create_demo_runtime()

    devices = runtime.room_service.list_devices_in_room("office")

    device_ids = [
        device.id
        for device in devices
    ]

    assert "light.office.ceiling" in device_ids


def test_room_service_turns_on_room_lights():
    runtime = create_demo_runtime()

    result = runtime.room_service.turn_on_room_lights("office")
    office_light = runtime.device_registry.get_device_by_id(
        "light.office.ceiling"
    )

    assert result.success is True
    assert office_light is not None
    assert office_light.state == DeviceState.ON


def test_room_service_turns_off_room_lights():
    runtime = create_demo_runtime()

    runtime.room_service.turn_on_room_lights("office")
    result = runtime.room_service.turn_off_room_lights("office")
    office_light = runtime.device_registry.get_device_by_id(
        "light.office.ceiling"
    )

    assert result.success is True
    assert office_light is not None
    assert office_light.state == DeviceState.OFF


def test_room_service_fails_for_unknown_room():
    runtime = create_demo_runtime()

    result = runtime.room_service.turn_on_room_lights("garage")

    assert result.success is False
    assert "not found" in result.message


def test_room_service_fails_when_room_has_no_lights():
    runtime = create_demo_runtime()

    runtime.room_registry.register_room(
        Room(
            id="hallway",
            name="Hallway",
            floor_id="ground_floor",
        )
    )

    sensor = Device(
        id="sensor.hallway.motion",
        name="Hallway Motion Sensor",
        device_type=DeviceType.SENSOR,
        room_id="hallway",
    )
    runtime.device_registry.register_device(sensor)

    result = runtime.room_service.turn_on_room_lights("hallway")

    assert result.success is False
    assert "No lights found" in result.message