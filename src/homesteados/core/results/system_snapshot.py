"""System snapshot result models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class DeviceSnapshot:
    """Snapshot of one device."""

    id: str
    name: str
    device_type: str
    room_id: str
    state: str
    online: bool
    adapter_id: str


@dataclass(frozen=True)
class RoomSnapshot:
    """Snapshot of one room."""

    id: str
    name: str
    floor_id: str
    device_count: int


@dataclass(frozen=True)
class SystemSnapshot:
    """Snapshot of the HomeSteadOS runtime state."""

    system_mode: str
    rooms: list[RoomSnapshot]
    devices: list[DeviceSnapshot]
    scene_count: int
    automation_count: int
    enabled_automation_count: int
    shortcut_count: int
    pending_action_count: int
    command_history_count: int
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)