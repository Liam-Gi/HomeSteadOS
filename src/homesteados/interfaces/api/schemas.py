"""API request and response schemas."""

from typing import Any

from pydantic import BaseModel


class CapabilityResponse(BaseModel):
    """API representation of a device capability."""

    capability_type: str
    name: str
    metadata: dict[str, Any] | None = None


class DeviceResponse(BaseModel):
    """API representation of a device."""

    id: str
    name: str
    device_type: str
    room_id: str
    adapter_id: str
    state: str
    online: bool
    capabilities: list[CapabilityResponse]
    attributes: dict[str, Any]


class RoomResponse(BaseModel):
    """API representation of a room."""

    id: str
    name: str
    floor_id: str
    device_ids: list[str]

class ActionRequest(BaseModel):
    """API request for a HomeSteadOS action."""

    action_type: str
    target_id: str
    requested_by: str = "api"
    parameters: dict[str, Any] = {}


class ActionResponse(BaseModel):
    """API response for an action result."""

    success: bool
    message: str
    action_id: str | None = None
    requires_confirmation: bool = False
    reason: str | None = None
    data: dict[str, Any]


class EventResponse(BaseModel):
    """API representation of a HomeSteadOS event."""

    id: str
    event_type: str
    source: str
    occurred_at: str
    payload: dict[str, Any]


class SystemStatusResponse(BaseModel):
    """API response for current HomeSteadOS status."""

    status: str
    device_count: int
    adapter_count: int
    event_count: int