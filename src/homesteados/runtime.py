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
from homesteados.adapters.home_assistant.home_assistant_adapter import HomeAssistantAdapter
from homesteados.config.settings import AppSettings
from homesteados.core.services.audit_log_service import AuditLogService
from homesteados.core.registry.pending_action_store import PendingActionStore
from homesteados.core.services.confirmation_service import ConfirmationService
from homesteados.core.registry.automation_rule_registry import AutomationRuleRegistry
from homesteados.core.services.automation_service import AutomationService
from homesteados.config.automation_config_loader import load_and_register_automation_config
from homesteados.config.scene_config_loader import load_and_register_scene_config
from homesteados.core.registry.scene_registry import SceneRegistry
from homesteados.core.services.scene_service import SceneService
from homesteados.core.services.text_command_service import TextCommandService
from homesteados.core.services.action_description_service import ActionDescriptionService
from homesteados.core.services.command_history_service import CommandHistoryService
from homesteados.core.services.command_suggestion_service import CommandSuggestionService


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEMO_CONFIG_PATH = PROJECT_ROOT / "configs" / "demo_home.json"
DEFAULT_AUTOMATION_CONFIG_PATH = PROJECT_ROOT / "configs" / "demo_automations.json"
DEFAULT_SCENE_CONFIG_PATH = PROJECT_ROOT / "configs" / "demo_scenes.json"


@dataclass
class HomeSteadOSRuntime:
    """Contains the main runtime components for HomeSteadOS."""

    device_registry: DeviceRegistry
    room_registry: RoomRegistry
    adapter_registry: AdapterRegistry
    action_description_service: ActionDescriptionService
    command_suggestion_service: CommandSuggestionService
    event_bus: EventBus
    system_state: SystemState
    text_command_service: TextCommandService
    safety_engine: SafetyEngine
    lighting_service: LightingService
    command_history_service: CommandHistoryService
    room_service: RoomService
    system_service: SystemService
    scene_registry: SceneRegistry
    scene_service: SceneService
    automation_rule_registry: AutomationRuleRegistry
    automation_service: AutomationService
    action_dispatcher: ActionDispatcher
    diagnostics_service: DiagnosticsService
    audit_log_service: AuditLogService
    pending_action_store: PendingActionStore
    confirmation_service: ConfirmationService


def create_runtime(settings: AppSettings | None = None) -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime without registered rooms or devices."""

    device_registry = DeviceRegistry()
    room_registry = RoomRegistry()
    scene_registry = SceneRegistry()
    command_history_service = CommandHistoryService()
    adapter_registry = AdapterRegistry()
    automation_rule_registry = AutomationRuleRegistry()
    event_bus = EventBus()
    audit_log_service = AuditLogService(event_bus=event_bus)
    audit_log_service.start()
    system_state = SystemState()
    safety_engine = SafetyEngine(system_state=system_state)
    pending_action_store = PendingActionStore()

    adapter_registry.register_adapter(SimulatedDeviceAdapter())

    if (
        settings is not None
        and settings.home_assistant.enabled
        and settings.home_assistant.base_url
        and settings.home_assistant.access_token
    ):
        adapter_registry.register_adapter(
            HomeAssistantAdapter(
                base_url=settings.home_assistant.base_url,
                access_token=settings.home_assistant.access_token,
            )
        )

    action_description_service = ActionDescriptionService(
        device_registry=device_registry,
        room_registry=room_registry,
        scene_registry=scene_registry,
    )

    command_suggestion_service = CommandSuggestionService(
        room_registry=room_registry,
        scene_registry=scene_registry,
    )

    lighting_service = LightingService(
        device_registry=device_registry,
        adapter_registry=adapter_registry,
        safety_engine=safety_engine,
        event_bus=event_bus,
        pending_action_store=pending_action_store,
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

    scene_service = SceneService(
        scene_registry=scene_registry,
        action_executor=action_dispatcher,
    )

    action_dispatcher.set_scene_service(scene_service)

    text_command_service = TextCommandService(
        device_registry=device_registry,
        room_registry=room_registry,
        scene_registry=scene_registry,
        action_executor=action_dispatcher,
        command_suggestion_service=command_suggestion_service,
    )

    automation_service = AutomationService(
        automation_rule_registry=automation_rule_registry,
        event_bus=event_bus,
        action_executor=action_dispatcher,
    )
    automation_service.start()

    confirmation_service = ConfirmationService(
        pending_action_store=pending_action_store,
        action_executor=action_dispatcher,
    )

    return HomeSteadOSRuntime(
        device_registry=device_registry,
        room_registry=room_registry,
        adapter_registry=adapter_registry,
        action_description_service=action_description_service,
        event_bus=event_bus,
        system_state=system_state,
        safety_engine=safety_engine,
        pending_action_store=pending_action_store,
        lighting_service=lighting_service,
        command_history_service=command_history_service,
        room_service=room_service,
        system_service=system_service,
        command_suggestion_service=command_suggestion_service,
        scene_registry=scene_registry,
        scene_service=scene_service,
        diagnostics_service=diagnostics_service,
        automation_rule_registry=automation_rule_registry,
        automation_service=automation_service,
        audit_log_service=audit_log_service,
        confirmation_service=confirmation_service,
        text_command_service=text_command_service,
        action_dispatcher=action_dispatcher,
    )


def create_demo_runtime(
    config_path: str | Path = DEFAULT_DEMO_CONFIG_PATH,
    settings: AppSettings | None = None,
) -> HomeSteadOSRuntime:
    """Create a HomeSteadOS runtime with demo rooms and devices."""

    runtime = create_runtime(settings=settings)

    load_and_register_home_config(
        config_path=config_path,
        room_registry=runtime.room_registry,
        device_registry=runtime.device_registry,
    )

    load_and_register_scene_config(
        config_path=DEFAULT_SCENE_CONFIG_PATH,
        scene_registry=runtime.scene_registry,
    )

    load_and_register_automation_config(
        config_path=DEFAULT_AUTOMATION_CONFIG_PATH,
        automation_rule_registry=runtime.automation_rule_registry,
    )

    return runtime

