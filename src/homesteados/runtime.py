"""Application runtime wiring for HomeSteadOS."""

from dataclasses import dataclass
from pathlib import Path

from homesteados.adapters.simulated.simulated_device_adapter import (
    SimulatedDeviceAdapter,
)
from homesteados.config.home_config_loader import load_and_register_home_config
from homesteados.core.domain.system_state import SystemState
from homesteados.core.events.event_bus import EventBus
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.safety.safety_engine import SafetyEngine
from homesteados.core.services.action_dispatcher import ActionDispatcher
from homesteados.core.services.lighting_service import LightingService
from homesteados.core.services.room_service import RoomService
from homesteados.core.services.system_service import SystemService
from homesteados.core.services.diagnostics_service import DiagnosticsService


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEMO_CONFIG_PATH = PROJECT_ROOT / "configs" / "demo_home.json"


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
    action_dispatcher: ActionDispatcher
    diagnostics_service: DiagnosticsService


def create_runtime() -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime without registered rooms or devices."""

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

    diagnostics_service = DiagnosticsService(
        device_registry=device_registry,
        room_registry=room_registry,
        adapter_registry=adapter_registry,
        event_bus=event_bus,
        system_state=system_state,
    )

    action_dispatcher = ActionDispatcher(
        lighting_service=lighting_service,
        room_service=room_service,
        system_service=system_service,
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
        action_dispatcher=action_dispatcher,
        diagnostics_service=diagnostics_service,
    )


def create_demo_runtime(
    config_path: str | Path = DEFAULT_DEMO_CONFIG_PATH,
) -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime with demo rooms and devices."""

    runtime = create_runtime()

    load_and_register_home_config(
        config_path=config_path,
        room_registry=runtime.room_registry,
        device_registry=runtime.device_registry,
    )

    return runtime