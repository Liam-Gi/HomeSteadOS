"""Shared event type definitions."""

from enum import Enum


class EventType(str, Enum):
    """Supported internal HomeSteadOS event types."""

    ACTION_REQUESTED = "action_requested"
    ACTION_COMPLETED = "action_completed"
    ACTION_FAILED = "action_failed"
    ACTION_BLOCKED = "action_blocked"
    DEVICE_STATE_CHANGED = "device_state_changed"
    DEVICE_REGISTERED = "device_registered"
    ROOM_REGISTERED = "room_registered"
    SYSTEM_MODE_CHANGED = "system_mode_changed"
    AUTOMATION_TRIGGERED = "automation_triggered"
    AUTOMATION_FAILED = "automation_failed"