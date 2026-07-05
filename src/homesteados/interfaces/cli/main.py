"""Command-line interface entry point for HomeSteadOS."""

from homesteados.core.events.event_bus import EventBus
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.adapters.simulated.simulated_device_adapter import SimulatedDeviceAdapter
from homesteados.core.domain.capability import Capability
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import (
    CapabilityType,
    DeviceState,
    DeviceType,
)
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.services.lighting_service import LightingService
from homesteados.interfaces.cli.command_parser import CommandParser


def create_demo_device_registry() -> DeviceRegistry:
    """Create demo devices for local CLI testing."""

    registry = DeviceRegistry()

    power_capability = Capability(
        capability_type=CapabilityType.POWER,
        name="Power",
    )

    demo_devices = [
        Device(
            id="light.office.ceiling",
            name="Office Ceiling Light",
            device_type=DeviceType.LIGHT,
            room_id="office",
            state=DeviceState.OFF,
            capabilities=[power_capability],
        ),
        Device(
            id="light.kitchen.ceiling",
            name="Kitchen Ceiling Light",
            device_type=DeviceType.LIGHT,
            room_id="kitchen",
            state=DeviceState.OFF,
            capabilities=[power_capability],
        ),
        Device(
            id="light.bedroom.lamp",
            name="Bedroom Lamp",
            device_type=DeviceType.LIGHT,
            room_id="bedroom",
            state=DeviceState.OFF,
            capabilities=[power_capability],
        ),
    ]

    for device in demo_devices:
        registry.register_device(device)

    return registry


def main() -> None:
    """Run the HomeSteadOS CLI."""

    device_registry = create_demo_device_registry()
    adapter_registry = AdapterRegistry()
    adapter_registry.register_adapter(SimulatedDeviceAdapter())

    event_bus = EventBus()

    lighting_service = LightingService(
        device_registry=device_registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
    )
    command_parser = CommandParser(
        device_registry=device_registry,
        lighting_service=lighting_service,
    )

    print("HomeSteadOS CLI Prototype")
    print("Type 'help' for commands.")
    print("Type 'exit' to quit.\n")

    while True:
        command = input("> ").strip()

        if command.lower() in {"exit", "quit"}:
            print("Shutting down HomeSteadOS.")
            break

        response = command_parser.handle(command)
        print(response)


if __name__ == "__main__":
    main()