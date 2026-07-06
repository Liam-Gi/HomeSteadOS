"""API request and response schemas."""

from typing import Any

from pydantic import BaseModel
from typing import Any

from pydantic import BaseModel, Field


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
    target_type: str = "device"
    requested_by: str = "api"
    requires_confirmation: bool = False
    risk_level: str = "low"
    parameters: dict[str, Any] = Field(default_factory=dict)


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


class SystemModeResponse(BaseModel):
    """API response for current system mode."""

    mode: str
    updated_at: str
    updated_by: str


class SetSystemModeRequest(BaseModel):
    """API request to update the current system mode."""

    mode: str
    updated_by: str = "api"

class SystemStatusResponse(BaseModel):
    """API response for current HomeSteadOS status."""

    status: str
    device_count: int
    adapter_count: int
    event_count: int

class HealthCheckResponse(BaseModel):
    """API response for a single health check."""

    name: str
    status: str
    message: str
    data: dict[str, Any]


class SystemHealthResponse(BaseModel):
    """API response for system health."""

    status: str
    checks: list[HealthCheckResponse]
    summary: dict[str, Any]

class AuditLogEntryResponse(BaseModel):
    """API response for an audit log entry."""

    event_id: str
    event_type: str
    source: str
    occurred_at: str
    message: str
    payload: dict[str, Any]

class PendingActionResponse(BaseModel):
    """API response for a pending action."""

    id: str
    action_type: str
    target_id: str
    target_type: str
    requested_by: str
    requires_confirmation: bool
    risk_level: str
    parameters: dict[str, Any]

class AutomationRuleResponse(BaseModel):
    """API response for an automation rule."""

    id: str
    name: str
    enabled: bool
    trigger_event_type: str
    trigger_payload_matches: dict[str, Any]
    action_type: str
    target_id: str
    target_type: str
    requested_by: str
    risk_level: str

class SceneResponse(BaseModel):
    """API response for a scene."""

    id: str
    name: str
    enabled: bool
    action_count: int

class TextCommandRequest(BaseModel):
    """API request for a text command."""

    command: str
    requested_by: str = "api"

class TextCommandPreviewResponse(BaseModel):
    """API response for previewing a text command."""

    success: bool
    message: str
    description: str | None = None
    action_type: str | None = None
    target_id: str | None = None
    target_type: str | None = None
    requested_by: str | None = None
    risk_level: str | None = None
    requires_confirmation: bool | None = None
    parameters: dict[str, Any] | None = None

class CommandHistoryEntryResponse(BaseModel):
    """API response for a command history entry."""

    id: str
    command: str
    requested_by: str
    mode: str
    success: bool
    message: str
    occurred_at: str
    action_type: str | None = None
    target_id: str | None = None
    target_type: str | None = None
    risk_level: str | None = None
    requires_confirmation: bool | None = None
    description: str | None = None
    result_data: dict[str, Any]