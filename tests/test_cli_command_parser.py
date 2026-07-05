"""Tests for the CLI command parser."""

from homesteados.core.events.event_bus import EventBus
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.adapters.simulated.simulated_device_adapter import SimulatedDeviceAdapter
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceState, DeviceType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService
from homesteados.interfaces.cli.command_parser import CommandParser


def create_parser_with_office_light() -> tuple[CommandParser, Device]:
    registry = DeviceRegistry()
    light = Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        state=DeviceState.OFF,
    )

    registry.register_device(light)

    adapter_registry = AdapterRegistry()
    adapter_registry.register_adapter(SimulatedDeviceAdapter())

    event_bus = EventBus()

    service = LightingService(
        device_registry=registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
    )

    parser = CommandParser(
        device_registry=registry,
        lighting_service=service,
        event_bus=event_bus,
    )

    return parser, light


def test_cli_can_turn_on_light_by_friendly_name():
    parser, light = create_parser_with_office_light()

    response = parser.handle("turn on office light")

    assert "turned on" in response
    assert light.state == DeviceState.ON


def test_cli_can_turn_off_light_by_friendly_name():
    parser, light = create_parser_with_office_light()

    parser.handle("turn on office light")
    response = parser.handle("turn off office light")

    assert "turned off" in response
    assert light.state == DeviceState.OFF


def test_cli_lists_registered_devices():
    parser, _ = create_parser_with_office_light()

    response = parser.handle("devices")

    assert "light.office.ceiling" in response
    assert "Office Ceiling Light" in response


def test_cli_returns_help_text():
    parser, _ = create_parser_with_office_light()

    response = parser.handle("help")

    assert "Available commands" in response


def test_cli_rejects_unknown_command():
    parser, _ = create_parser_with_office_light()

    response = parser.handle("do something random")

    assert "Command not recognised" in response

def test_cli_can_show_event_log_after_action():
    parser, _ = create_parser_with_office_light()

    parser.handle("turn on office light")
    response = parser.handle("events")

    assert "Event log" in response
    assert "action_requested" in response
    assert "action_completed" in response
    assert "device_state_changed" in response