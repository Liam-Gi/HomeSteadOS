"""Tests for HomeSteadOS runtime wiring."""

from homesteados.core.domain.enums import DeviceState
from homesteados.runtime import create_demo_runtime, create_runtime
from pathlib import Path

from homesteados.config.settings import AppSettings, HomeAssistantSettings


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

def test_runtime_wires_safety_engine_to_system_state():
    runtime = create_runtime()

    runtime.system_service.set_mode("away", updated_by="test")

    assert runtime.safety_engine.system_state is runtime.system_state
    assert runtime.safety_engine.system_state.mode.value == "away"

def test_demo_runtime_loads_rooms_from_config():
    runtime = create_demo_runtime()

    office = runtime.room_registry.get_room_by_id("office")

    assert office is not None
    assert "light.office.ceiling" in office.device_ids

def test_runtime_creates_diagnostics_service():
    runtime = create_runtime()

    assert runtime.diagnostics_service is not None

def test_runtime_registers_home_assistant_adapter_when_enabled():
    settings = AppSettings(
        environment="test",
        log_level="INFO",
        demo_config_path=Path("configs/demo_home.json"),
        home_assistant=HomeAssistantSettings(
            enabled=True,
            base_url="http://homeassistant.local:8123",
            access_token="test-token",
        ),
    )

    runtime = create_runtime(settings=settings)

    adapter = runtime.adapter_registry.get_adapter("home_assistant")

    assert adapter is not None

def test_demo_runtime_can_load_home_assistant_sample_config_when_enabled():
    settings = AppSettings(
        environment="test",
        log_level="INFO",
        demo_config_path=Path("configs/home_assistant_sample.json"),
        home_assistant=HomeAssistantSettings(
            enabled=True,
            base_url="http://homeassistant.local:8123",
            access_token="test-token",
        ),
    )

    runtime = create_demo_runtime(
        config_path=settings.demo_config_path,
        settings=settings,
    )

    device = runtime.device_registry.get_device_by_id(
        "light.office.home_assistant_test"
    )
    adapter = runtime.adapter_registry.get_adapter("home_assistant")

    assert device is not None
    assert device.adapter_id == "home_assistant"
    assert adapter is not None

def test_runtime_creates_audit_log_service():
    runtime = create_runtime()

    assert runtime.audit_log_service is not None