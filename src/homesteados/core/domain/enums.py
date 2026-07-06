"""Shared enums used across the HomeSteadOS core domain."""

from enum import Enum


class DeviceType(str, Enum):
    """Supported high-level device categories."""

    LIGHT = "light"
    SENSOR = "sensor"
    SWITCH = "switch"
    CAMERA = "camera"
    LOCK = "lock"
    CLIMATE = "climate"
    SPEAKER = "speaker"
    UNKNOWN = "unknown"


class DeviceState(str, Enum):
    """Common device states."""

    ON = "on"
    OFF = "off"
    UNKNOWN = "unknown"
    UNAVAILABLE = "unavailable"


class CapabilityType(str, Enum):
    """Capabilities that a device may support."""

    POWER = "power"
    BRIGHTNESS = "brightness"
    COLOUR = "colour"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    MOTION = "motion"
    LOCK = "lock"
    BATTERY = "battery"


class ActionType(str, Enum):
    """Supported high-level action types."""

    TURN_ON = "turn_on"
    TURN_OFF = "turn_off"
    SET_STATE = "set_state"
    SET_BRIGHTNESS = "set_brightness"
    READ_STATE = "read_state"
    RUN_SCENE = "run_scene"

class SystemMode(str, Enum):
    """Supported HomeSteadOS system modes."""

    HOME = "home"
    AWAY = "away"
    NIGHT = "night"
    GUEST = "guest"
    VACATION = "vacation"

class ActionRisk(str, Enum):
    """Risk level for requested actions."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActionTargetType(str, Enum):
    """Supported action target types."""

    DEVICE = "device"
    ROOM = "room"
    SYSTEM = "system"
    SCENE = "scene"

class HealthStatus(str, Enum):
    """Supported health statuses."""

    OK = "ok"
    WARNING = "warning"
    ERROR = "error"