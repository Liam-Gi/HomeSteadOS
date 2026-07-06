"""Load HomeSteadOS home configuration from JSON files."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from homesteados.core.domain.capability import Capability
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import (
    CapabilityType,
    DeviceState,
    DeviceType,
)
from homesteados.core.domain.room import Room
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry


@dataclass(frozen=True)
class HomeConfig:
    """Parsed HomeSteadOS home configuration."""

    rooms: list[Room]
    devices: list[Device]


def load_home_config(config_path: str | Path) -> HomeConfig:
    """Load a HomeSteadOS home config file."""

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Home config file was not found: {path}")

    raw_config = json.loads(path.read_text(encoding="utf-8"))

    rooms = [
        _parse_room(room_data)
        for room_data in raw_config.get("rooms", [])
    ]

    devices = [
        _parse_device(device_data)
        for device_data in raw_config.get("devices", [])
    ]

    return HomeConfig(
        rooms=rooms,
        devices=devices,
    )


def register_home_config(
    home_config: HomeConfig,
    room_registry: RoomRegistry,
    device_registry: DeviceRegistry,
) -> None:
    """Register rooms and devices from a parsed home configuration."""

    for room in home_config.rooms:
        room_registry.register_room(room)

    for device in home_config.devices:
        room = room_registry.get_room_by_id(device.room_id)

        if room is None:
            raise ValueError(
                f"Device '{device.id}' references unknown room '{device.room_id}'."
            )

        device_registry.register_device(device)
        room.add_device(device.id)


def load_and_register_home_config(
    config_path: str | Path,
    room_registry: RoomRegistry,
    device_registry: DeviceRegistry,
) -> HomeConfig:
    """Load and register a home configuration file."""

    home_config = load_home_config(config_path)

    register_home_config(
        home_config=home_config,
        room_registry=room_registry,
        device_registry=device_registry,
    )

    return home_config


def _parse_room(room_data: dict[str, Any]) -> Room:
    """Parse room data into a Room model."""

    return Room(
        id=room_data["id"],
        name=room_data["name"],
        floor_id=room_data["floor_id"],
    )


def _parse_device(device_data: dict[str, Any]) -> Device:
    """Parse device data into a Device model."""

    capabilities = [
        _parse_capability(capability_data)
        for capability_data in device_data.get("capabilities", [])
    ]

    return Device(
        id=device_data["id"],
        name=device_data["name"],
        device_type=DeviceType(device_data.get("device_type", "unknown")),
        room_id=device_data["room_id"],
        adapter_id=device_data.get("adapter_id", "simulated"),
        state=DeviceState(device_data.get("state", "unknown")),
        online=device_data.get("online", True),
        capabilities=capabilities,
        attributes=device_data.get("attributes", {}),
    )


def _parse_capability(capability_data: dict[str, Any]) -> Capability:
    """Parse capability data into a Capability model."""

    return Capability(
        capability_type=CapabilityType(capability_data["capability_type"]),
        name=capability_data["name"],
        metadata=capability_data.get("metadata"),
    )