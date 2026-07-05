"""HTTP API entry point for HomeSteadOS."""

from fastapi import FastAPI

from homesteados.core.domain.device import Device
from homesteados.core.events.event import Event
from homesteados.core.results.action_result import ActionResult
from homesteados.interfaces.api.schemas import (
    ActionRequest,
    ActionResponse,
    CapabilityResponse,
    DeviceResponse,
    EventResponse,
    SystemStatusResponse,
)
from homesteados.runtime import HomeSteadOSRuntime, create_demo_runtime


def create_app(runtime: HomeSteadOSRuntime | None = None) -> FastAPI:
    """Create and configure the HomeSteadOS API app."""

    app_runtime = runtime or create_demo_runtime()

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

        if request.action_type == "turn_on":
            result = runtime.lighting_service.turn_on_light(
                device_id=request.target_id,
                requested_by=request.requested_by,
            )
            return _action_result_to_response(result)

        if request.action_type == "turn_off":
            result = runtime.lighting_service.turn_off_light(
                device_id=request.target_id,
                requested_by=request.requested_by,
            )
            return _action_result_to_response(result)

        result = ActionResult.fail(
            message=f"Unsupported action type '{request.action_type}'.",
            reason="The API currently supports only turn_on and turn_off actions.",
        )

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


def _event_to_response(event: Event) -> EventResponse:
    """Convert an event into an API response."""

    return EventResponse(
        id=event.id,
        event_type=event.event_type.value,
        source=event.source,
        occurred_at=event.occurred_at.isoformat(),
        payload=event.payload,
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