"""Application runtime wiring for HomeSteadOS."""

from homesteados.core.safety.safety_engine import SafetyEngine
from homesteados.core.domain.system_state import SystemState
from homesteados.core.services.system_service import SystemService
from homesteados.core.domain.room import Room
from homesteados.core.services.room_service import RoomService
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
    system_state: SystemState
    safety_engine: SafetyEngine
    lighting_service: LightingService
    room_service: RoomService
    system_service: SystemService


def create_runtime() -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime without demo devices."""

    device_registry = DeviceRegistry()
    room_registry = RoomRegistry()
    adapter_registry = AdapterRegistry()
    event_bus = EventBus()
    system_state = SystemState()
    safety_engine = SafetyEngine(system_state=system_state)

    adapter_registry.register_adapter(SimulatedDeviceAdapter())

    lighting_service = LightingService(
        device_registry=device_registry,
        adapter_registry=adapter_registry,
        safety_engine=safety_engine,
        event_bus=event_bus,
    )

    room_service = RoomService(
        room_registry=room_registry,
        device_registry=device_registry,
        lighting_service=lighting_service,
    )

    system_service = SystemService(
        system_state=system_state,
        event_bus=event_bus,
    )

    return HomeSteadOSRuntime(
        device_registry=device_registry,
        room_registry=room_registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
        system_state=system_state,
        safety_engine=safety_engine,
        lighting_service=lighting_service,
        room_service=room_service,
        system_service=system_service,
    )


def create_demo_runtime() -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime with demo devices."""

    runtime = create_runtime()
    register_demo_rooms(runtime.room_registry)
    register_demo_devices(runtime.device_registry, runtime.room_registry)

    return runtime


def register_demo_rooms(room_registry: RoomRegistry) -> None:
    """Register demo rooms for early testing."""

    demo_rooms = [
        Room(
            id="office",
            name="Office",
            floor_id="ground_floor",
        ),
        Room(
            id="kitchen",
            name="Kitchen",
            floor_id="ground_floor",
        ),
        Room(
            id="bedroom",
            name="Bedroom",
            floor_id="ground_floor",
        ),
    ]

    for room in demo_rooms:
        room_registry.register_room(room)


def register_demo_devices(
    device_registry: DeviceRegistry,
    room_registry: RoomRegistry,
) -> None:
    """Register demo devices for early CLI and API testing."""

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

        room = room_registry.get_room_by_id(device.room_id)
        if room is not None:
            room.add_device(device.id)