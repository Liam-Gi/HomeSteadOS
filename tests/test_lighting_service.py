"""Tests for lighting service behaviour."""

from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceState, DeviceType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService


def create_registry_with_office_light() -> tuple[DeviceRegistry, Device]:
    registry = DeviceRegistry()
    light = Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
    )

    registry.register_device(light)

    return registry, light


def test_turn_on_light_updates_device_state():
    registry, light = create_registry_with_office_light()
    service = LightingService(device_registry=registry)

    result = service.turn_on_light("light.office.ceiling")

    assert result.success is True
    assert light.state == DeviceState.ON


def test_turn_off_light_updates_device_state():
    registry, light = create_registry_with_office_light()
    service = LightingService(device_registry=registry)

    service.turn_on_light("light.office.ceiling")
    result = service.turn_off_light("light.office.ceiling")

    assert result.success is True
    assert light.state == DeviceState.OFF


def test_turn_on_unknown_light_returns_failure():
    registry = DeviceRegistry()
    service = LightingService(device_registry=registry)

    result = service.turn_on_light("light.office.ceiling")

    assert result.success is False
    assert "not found" in result.message


def test_lighting_service_rejects_non_light_device():
    registry = DeviceRegistry()
    sensor = Device(
        id="sensor.office.motion",
        name="Office Motion Sensor",
        device_type=DeviceType.SENSOR,
        room_id="office",
    )
    registry.register_device(sensor)

    service = LightingService(device_registry=registry)

    result = service.turn_on_light("sensor.office.motion")

    assert result.success is False
    assert "not a light" in result.message