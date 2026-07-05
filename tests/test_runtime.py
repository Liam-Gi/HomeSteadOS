"""Tests for HomeSteadOS runtime wiring."""

from homesteados.core.domain.enums import DeviceState
from homesteados.runtime import create_demo_runtime, create_runtime


def test_create_runtime_registers_simulated_adapter():
    runtime = create_runtime()

    adapter = runtime.adapter_registry.get_adapter("simulated")

    assert adapter is not None


def test_create_demo_runtime_registers_demo_devices():
    runtime = create_demo_runtime()

    office_light = runtime.device_registry.get_device_by_id(
        "light.office.ceiling"
    )

    assert office_light is not None
    assert office_light.name == "Office Ceiling Light"


def test_demo_runtime_can_turn_on_demo_light():
    runtime = create_demo_runtime()

    result = runtime.lighting_service.turn_on_light("light.office.ceiling")
    office_light = runtime.device_registry.get_device_by_id(
        "light.office.ceiling"
    )

    assert result.success is True
    assert office_light is not None
    assert office_light.state == DeviceState.ON