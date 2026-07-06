"""Tests for the CLI command parser."""

from homesteados.core.events.event_bus import EventBus
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.adapters.simulated.simulated_device_adapter import SimulatedDeviceAdapter
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceState, DeviceType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService
from homesteados.interfaces.cli.command_parser import CommandParser
from homesteados.runtime import create_demo_runtime
from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionRisk, ActionTargetType, ActionType


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


def create_demo_parser() -> CommandParser:
    runtime = create_demo_runtime()

    return CommandParser(
        device_registry=runtime.device_registry,
        lighting_service=runtime.lighting_service,
        automation_service=runtime.automation_service,
        room_service=runtime.room_service,
        system_service=runtime.system_service,
        diagnostics_service=runtime.diagnostics_service,
        audit_log_service=runtime.audit_log_service,
        confirmation_service=runtime.confirmation_service,
        event_bus=runtime.event_bus,
    )

def test_cli_can_list_automation_rules():
    parser = create_demo_parser()

    response = parser.handle("automations")

    assert "Automation rules" in response
    assert "night-turn-off-kitchen" in response


def test_cli_can_disable_automation_rule():
    parser = create_demo_parser()

    response = parser.handle("disable automation night-turn-off-kitchen")

    assert "disabled" in response

def test_cli_can_show_system_mode():
    parser = create_demo_parser()

    response = parser.handle("mode")

    assert "System mode: home" in response


def test_cli_can_set_system_mode():
    parser = create_demo_parser()

    response = parser.handle("set mode away")

    assert "System mode changed to away" in response

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


def test_cli_can_list_pending_actions():
    runtime = create_demo_runtime()
    parser = CommandParser(
        device_registry=runtime.device_registry,
        lighting_service=runtime.lighting_service,
        room_service=runtime.room_service,
        system_service=runtime.system_service,
        diagnostics_service=runtime.diagnostics_service,
        audit_log_service=runtime.audit_log_service,
        confirmation_service=runtime.confirmation_service,
        event_bus=runtime.event_bus,
    )

    runtime.action_dispatcher.execute(
        Action(
            action_type=ActionType.TURN_ON,
            target_id="light.office.ceiling",
            target_type=ActionTargetType.DEVICE,
            requested_by="test",
            risk_level=ActionRisk.HIGH,
        )
    )

    response = parser.handle("pending")

    assert "Pending actions" in response
    assert "light.office.ceiling" in response

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

def test_cli_can_list_rooms():
    parser = create_demo_parser()

    response = parser.handle("rooms")

    assert "office" in response
    assert "kitchen" in response
    assert "bedroom" in response


def test_cli_can_show_room_status():
    parser = create_demo_parser()

    response = parser.handle("room status office")

    assert "Office devices" in response
    assert "light.office.ceiling" in response


def test_cli_can_turn_on_room_lights():
    parser = create_demo_parser()

    response = parser.handle("turn on room office")

    assert "All lights in Office turned on" in response

def test_cli_can_show_event_log_after_action():
    parser, _ = create_parser_with_office_light()

    parser.handle("turn on office light")
    response = parser.handle("events")

    assert "Event log" in response
    assert "action_requested" in response
    assert "action_completed" in response
    assert "device_state_changed" in response

def test_cli_can_show_system_health():
    parser = create_demo_parser()

    response = parser.handle("health")

    assert "System health" in response
    assert "Checks:" in response

def test_cli_can_show_audit_log_after_action():
    parser = create_demo_parser()

    parser.handle("turn on office light")
    response = parser.handle("audit")

    assert "Audit log" in response
    assert "Action requested" in response
    assert "Action completed" in response
    assert "Device state changed" in response