"""Application runtime wiring for HomeSteadOS."""

from dataclasses import dataclass

from homesteados.adapters.simulated.simulated_device_adapter import (
    SimulatedDeviceAdapter,
)
from homesteados.core.domain.capability import Capability
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import (
    CapabilityType,
    DeviceState,
    DeviceType,
)
from homesteados.core.events.event_bus import EventBus
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.services.lighting_service import LightingService


@dataclass
class HomeSteadOSRuntime:
    """Contains the main runtime components for HomeSteadOS."""

    device_registry: DeviceRegistry
    room_registry: RoomRegistry
    adapter_registry: AdapterRegistry
    event_bus: EventBus
    lighting_service: LightingService


def create_runtime() -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime without demo devices."""

    device_registry = DeviceRegistry()
    room_registry = RoomRegistry()
    adapter_registry = AdapterRegistry()
    event_bus = EventBus()

    adapter_registry.register_adapter(SimulatedDeviceAdapter())

    lighting_service = LightingService(
        device_registry=device_registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
    )

    return HomeSteadOSRuntime(
        device_registry=device_registry,
        room_registry=room_registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
        lighting_service=lighting_service,
    )


def create_demo_runtime() -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime with demo devices."""

    runtime = create_runtime()
    register_demo_devices(runtime.device_registry)

    return runtime


def register_demo_devices(device_registry: DeviceRegistry) -> None:
    """Register demo devices for early CLI testing."""

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
        device_registry.register_device(device)