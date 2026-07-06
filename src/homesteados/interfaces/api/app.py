"""HTTP API entry point for HomeSteadOS."""

from fastapi import FastAPI
from homesteados.core.domain.room import Room

from homesteados.core.domain.device import Device
from homesteados.core.events.event import Event
from homesteados.core.results.action_result import ActionResult
from homesteados.interfaces.api.schemas import (
    ActionRequest,
    ActionResponse,
    CapabilityResponse,
    RoomResponse,
    DeviceResponse,
    EventResponse,
    SystemStatusResponse,
    SetSystemModeRequest,
    SystemModeResponse,
)
from homesteados.runtime import HomeSteadOSRuntime, create_demo_runtime
from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionRisk, ActionTargetType, ActionType
from homesteados.config.logging_config import configure_logging
from homesteados.config.settings import get_settings
from homesteados.interfaces.api.schemas import (
    ActionRequest,
    ActionResponse,
    CapabilityResponse,
    DeviceResponse,
    EventResponse,
    HealthCheckResponse,
    RoomResponse,
    SetSystemModeRequest,
    SystemHealthResponse,
    AuditLogEntryResponse,
    SceneResponse,
    SystemModeResponse,
    SystemStatusResponse,
    AutomationRuleResponse,
    TextCommandRequest,
    PendingActionResponse,
)


def create_app(runtime: HomeSteadOSRuntime | None = None) -> FastAPI:
    """Create and configure the HomeSteadOS API app."""

    if runtime is None:
        settings = get_settings()
        configure_logging(settings.log_level)
        app_runtime = create_demo_runtime(
            config_path=settings.demo_config_path,
        )
    else:
        app_runtime = runtime

    app = FastAPI(
        title="HomeSteadOS API",
        description="HTTP API for the HomeSteadOS local-first home operating system.",
        version="0.1.0",
    )

    app.state.runtime = app_runtime

    @app.get("/system/status", response_model=SystemStatusResponse)
    def get_system_status() -> SystemStatusResponse:
        """Return basic system status."""

        runtime = app.state.runtime

        return SystemStatusResponse(
            status="running",
            device_count=len(runtime.device_registry.list_devices()),
            adapter_count=len(runtime.adapter_registry.list_adapters()),
            event_count=len(runtime.event_bus.list_published_events()),
        )

    @app.post("/commands/text", response_model=ActionResponse)
    def execute_text_command(request: TextCommandRequest) -> ActionResponse:
        """Execute a text command."""

        runtime = app.state.runtime
        result = runtime.text_command_service.execute_text(
            command=request.command,
            requested_by=request.requested_by,
        )

        return _action_result_to_response(result)

    @app.get("/scenes", response_model=list[SceneResponse])
    def list_scenes() -> list[SceneResponse]:
        """Return scenes."""

        runtime = app.state.runtime

        return [
            SceneResponse(
                id=scene.id,
                name=scene.name,
                enabled=scene.enabled,
                action_count=len(scene.actions),
            )
            for scene in runtime.scene_service.list_scenes()
        ]

    @app.post("/scenes/{scene_id}/run", response_model=ActionResponse)
    def run_scene(scene_id: str) -> ActionResponse:
        """Run a scene."""

        runtime = app.state.runtime
        result = runtime.scene_service.run_scene(
            scene_id=scene_id,
            requested_by="api",
        )

        return _action_result_to_response(result)

    @app.get("/automations", response_model=list[AutomationRuleResponse])
    def list_automation_rules() -> list[AutomationRuleResponse]:
        """Return automation rules."""

        runtime = app.state.runtime

        return [
            _automation_rule_to_response(rule)
            for rule in runtime.automation_service.list_rules()
        ]

    @app.post("/automations/{rule_id}/enable", response_model=ActionResponse)
    def enable_automation_rule(rule_id: str) -> ActionResponse:
        """Enable an automation rule."""

        runtime = app.state.runtime
        result = runtime.automation_service.enable_rule(rule_id)

        return _action_result_to_response(result)

    @app.post("/automations/{rule_id}/disable", response_model=ActionResponse)
    def disable_automation_rule(rule_id: str) -> ActionResponse:
        """Disable an automation rule."""

        runtime = app.state.runtime
        result = runtime.automation_service.disable_rule(rule_id)

        return _action_result_to_response(result)

    @app.get("/system/health", response_model=SystemHealthResponse)
    def get_system_health() -> SystemHealthResponse:
        """Return system health information."""

        runtime = app.state.runtime
        report = runtime.diagnostics_service.get_health_report()

        return SystemHealthResponse(
            status=report.status.value,
            checks=[
                HealthCheckResponse(
                    name=check.name,
                    status=check.status.value,
                    message=check.message,
                    data=check.data,
                )
                for check in report.checks
            ],
            summary=report.summary,
        )

    @app.get("/system/mode", response_model=SystemModeResponse)
    def get_system_mode() -> SystemModeResponse:
        """Return the current system mode."""

        runtime = app.state.runtime
        state = runtime.system_state

        return SystemModeResponse(
            mode=state.mode.value,
            updated_at=state.updated_at.isoformat(),
            updated_by=state.updated_by,
        )

    @app.get("/actions/pending", response_model=list[PendingActionResponse])
    def list_pending_actions() -> list[PendingActionResponse]:
        """Return actions pending confirmation."""

        runtime = app.state.runtime

        return [
            PendingActionResponse(
                id=action.id,
                action_type=action.action_type.value,
                target_id=action.target_id,
                target_type=action.target_type.value,
                requested_by=action.requested_by,
                requires_confirmation=action.requires_confirmation,
                risk_level=action.risk_level.value,
                parameters=action.parameters,
            )
            for action in runtime.confirmation_service.list_pending_actions()
        ]

    @app.post("/actions/{action_id}/confirm", response_model=ActionResponse)
    def confirm_action(action_id: str) -> ActionResponse:
        """Confirm and execute a pending action."""

        runtime = app.state.runtime
        result = runtime.confirmation_service.confirm_action(action_id)

        return _action_result_to_response(result)

    @app.post("/actions/{action_id}/cancel", response_model=ActionResponse)
    def cancel_action(action_id: str) -> ActionResponse:
        """Cancel a pending action."""

        runtime = app.state.runtime
        result = runtime.confirmation_service.cancel_action(action_id)

        return _action_result_to_response(result)

    @app.post("/system/mode", response_model=ActionResponse)
    def set_system_mode(request: SetSystemModeRequest) -> ActionResponse:
        """Update the current system mode."""

        runtime = app.state.runtime

        result = runtime.system_service.set_mode(
            mode=request.mode,
            updated_by=request.updated_by,
        )

        return _action_result_to_response(result)

    @app.get("/devices", response_model=list[DeviceResponse])
    def list_devices() -> list[DeviceResponse]:
        """Return all registered devices."""

        runtime = app.state.runtime

        return [
            _device_to_response(device)
            for device in runtime.device_registry.list_devices()
        ]

    @app.get("/devices/{device_id}", response_model=DeviceResponse | None)
    def get_device(device_id: str) -> DeviceResponse | None:
        """Return a single device by ID."""

        runtime = app.state.runtime
        device = runtime.device_registry.get_device_by_id(device_id)

        if device is None:
            return None

        return _device_to_response(device)

    @app.get("/rooms", response_model=list[RoomResponse])
    def list_rooms() -> list[RoomResponse]:
        """Return all registered rooms."""

        runtime = app.state.runtime

        return [
            _room_to_response(room)
            for room in runtime.room_registry.list_rooms()
        ]

    @app.get("/rooms/{room_id}", response_model=RoomResponse | None)
    def get_room(room_id: str) -> RoomResponse | None:
        """Return a single room by ID."""

        runtime = app.state.runtime
        room = runtime.room_registry.get_room_by_id(room_id)

        if room is None:
            return None

        return _room_to_response(room)

    @app.get("/rooms/{room_id}/devices", response_model=list[DeviceResponse])
    def list_room_devices(room_id: str) -> list[DeviceResponse]:
        """Return all devices in a room."""

        runtime = app.state.runtime

        return [
            _device_to_response(device)
            for device in runtime.room_service.list_devices_in_room(room_id)
        ]

    @app.get("/audit", response_model=list[AuditLogEntryResponse])
    def list_audit_log() -> list[AuditLogEntryResponse]:
        """Return audit log entries."""

        runtime = app.state.runtime

        return [
            AuditLogEntryResponse(
                event_id=entry.event_id,
                event_type=entry.event_type.value,
                source=entry.source,
                occurred_at=entry.occurred_at.isoformat(),
                message=entry.message,
                payload=entry.payload,
            )
            for entry in runtime.audit_log_service.list_entries()
        ]

    @app.get("/events", response_model=list[EventResponse])
    def list_events() -> list[EventResponse]:
        """Return published event history."""

        runtime = app.state.runtime

        return [
            _event_to_response(event)
            for event in runtime.event_bus.list_published_events()
        ]

    @app.post("/actions", response_model=ActionResponse)
    def request_action(request: ActionRequest) -> ActionResponse:
        """Request a HomeSteadOS action."""

        runtime = app.state.runtime

        try:
            action = Action(
                action_type=ActionType(request.action_type),
                target_id=request.target_id,
                target_type=ActionTargetType(request.target_type),
                requested_by=request.requested_by,
                requires_confirmation=request.requires_confirmation,
                risk_level=ActionRisk(request.risk_level),
                parameters=request.parameters,
            )
        except ValueError as error:
            result = ActionResult.fail(
                message="Invalid action request.",
                reason=str(error),
            )
            return _action_result_to_response(result)

        result = runtime.action_dispatcher.execute(action)

        return _action_result_to_response(result)

    return app



def _device_to_response(device: Device) -> DeviceResponse:
    """Convert a domain device into an API response."""

    return DeviceResponse(
        id=device.id,
        name=device.name,
        device_type=device.device_type.value,
        room_id=device.room_id,
        adapter_id=device.adapter_id,
        state=device.state.value,
        online=device.online,
        capabilities=[
            CapabilityResponse(
                capability_type=capability.capability_type.value,
                name=capability.name,
                metadata=capability.metadata,
            )
            for capability in device.capabilities
        ],
        attributes=device.attributes,
    )


def _automation_rule_to_response(rule) -> AutomationRuleResponse:
    """Convert an automation rule into an API response."""

    return AutomationRuleResponse(
        id=rule.id,
        name=rule.name,
        enabled=rule.enabled,
        trigger_event_type=rule.trigger_event_type.value,
        trigger_payload_matches=rule.trigger_payload_matches,
        action_type=rule.action.action_type.value,
        target_id=rule.action.target_id,
        target_type=rule.action.target_type.value,
        requested_by=rule.action.requested_by,
        risk_level=rule.action.risk_level.value,
    )

def _event_to_response(event: Event) -> EventResponse:
    """Convert an event into an API response."""

    return EventResponse(
        id=event.id,
        event_type=event.event_type.value,
        source=event.source,
        occurred_at=event.occurred_at.isoformat(),
        payload=event.payload,
    )


def _room_to_response(room: Room) -> RoomResponse:
    """Convert a domain room into an API response."""

    return RoomResponse(
        id=room.id,
        name=room.name,
        floor_id=room.floor_id,
        device_ids=room.device_ids,
    )

def _action_result_to_response(result: ActionResult) -> ActionResponse:
    """Convert an action result into an API response."""

    return ActionResponse(
        success=result.success,
        message=result.message,
        action_id=result.action_id,
        requires_confirmation=result.requires_confirmation,
        reason=result.reason,
        data=result.data,
    )


app = create_app()