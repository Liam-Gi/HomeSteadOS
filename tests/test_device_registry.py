"""Tests for the device registry."""

import pytest

from homesteados.core.domain.capability import Capability
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import CapabilityType, DeviceType
from homesteados.core.registry.device_registry import DeviceRegistry


def create_office_light() -> Device:
    return Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        capabilities=[
            Capability(
                capability_type=CapabilityType.POWER,
                name="Power",
            )
        ],
    )


def test_register_device_adds_device_to_registry():
    registry = DeviceRegistry()
    device = create_office_light()

    registry.register_device(device)

    assert registry.get_device_by_id("light.office.ceiling") == device


def test_registering_duplicate_device_id_raises_error():
    registry = DeviceRegistry()
    device = create_office_light()

    registry.register_device(device)

    with pytest.raises(ValueError):
        registry.register_device(device)


def test_remove_device_removes_device_from_registry():
    registry = DeviceRegistry()
    device = create_office_light()

    registry.register_device(device)
    removed_device = registry.remove_device("light.office.ceiling")

    assert removed_device == device
    assert registry.get_device_by_id("light.office.ceiling") is None


def test_find_device_by_name_is_case_insensitive():
    registry = DeviceRegistry()
    device = create_office_light()

    registry.register_device(device)

    found_device = registry.find_device_by_name("office ceiling light")

    assert found_device == device


def test_find_devices_by_room_returns_matching_devices():
    registry = DeviceRegistry()
    office_light = create_office_light()
    kitchen_light = Device(
        id="light.kitchen.ceiling",
        name="Kitchen Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="kitchen",
    )

    registry.register_device(office_light)
    registry.register_device(kitchen_light)

    office_devices = registry.find_devices_by_room("office")

    assert office_light in office_devices
    assert kitchen_light not in office_devices


def test_find_devices_by_type_returns_matching_devices():
    registry = DeviceRegistry()
    office_light = create_office_light()
    office_sensor = Device(
        id="sensor.office.motion",
        name="Office Motion Sensor",
        device_type=DeviceType.SENSOR,
        room_id="office",
    )

    registry.register_device(office_light)
    registry.register_device(office_sensor)

    lights = registry.find_devices_by_type(DeviceType.LIGHT)

    assert office_light in lights
    assert office_sensor not in lights


def test_find_devices_by_capability_returns_matching_devices():
    registry = DeviceRegistry()
    office_light = create_office_light()
    office_sensor = Device(
        id="sensor.office.motion",
        name="Office Motion Sensor",
        device_type=DeviceType.SENSOR,
        room_id="office",
    )

    registry.register_device(office_light)
    registry.register_device(office_sensor)

    power_devices = registry.find_devices_by_capability(CapabilityType.POWER)

    assert office_light in power_devices
    assert office_sensor not in power_devices