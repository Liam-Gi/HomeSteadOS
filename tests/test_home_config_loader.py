"""Tests for loading HomeSteadOS home configuration files."""

import json
from pathlib import Path

import pytest

from homesteados.config.home_config_loader import (
    HomeConfigValidationError,
    load_and_register_home_config,
    load_home_config,
)
from homesteados.core.domain.enums import DeviceState, DeviceType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry


def write_config(path: Path, config: dict) -> None:
    path.write_text(
        json.dumps(config),
        encoding="utf-8",
    )


def create_test_config() -> dict:
    return {
        "rooms": [
            {
                "id": "office",
                "name": "Office",
                "floor_id": "ground_floor",
            }
        ],
        "devices": [
            {
                "id": "light.office.ceiling",
                "name": "Office Ceiling Light",
                "device_type": "light",
                "room_id": "office",
                "adapter_id": "simulated",
                "state": "off",
                "online": True,
                "capabilities": [
                    {
                        "capability_type": "power",
                        "name": "Power",
                        "metadata": None,
                    }
                ],
                "attributes": {},
            }
        ],
    }


def test_load_home_config_loads_rooms_and_devices(tmp_path):
    config_path = tmp_path / "home.json"
    write_config(config_path, create_test_config())

    home_config = load_home_config(config_path)

    assert len(home_config.rooms) == 1
    assert len(home_config.devices) == 1
    assert home_config.rooms[0].id == "office"
    assert home_config.devices[0].id == "light.office.ceiling"


def test_load_home_config_parses_device_enums(tmp_path):
    config_path = tmp_path / "home.json"
    write_config(config_path, create_test_config())

    home_config = load_home_config(config_path)
    device = home_config.devices[0]

    assert device.device_type == DeviceType.LIGHT
    assert device.state == DeviceState.OFF


def test_load_and_register_home_config_registers_rooms_and_devices(tmp_path):
    config_path = tmp_path / "home.json"
    write_config(config_path, create_test_config())

    room_registry = RoomRegistry()
    device_registry = DeviceRegistry()

    load_and_register_home_config(
        config_path=config_path,
        room_registry=room_registry,
        device_registry=device_registry,
    )

    room = room_registry.get_room_by_id("office")
    device = device_registry.get_device_by_id("light.office.ceiling")

    assert room is not None
    assert device is not None
    assert "light.office.ceiling" in room.device_ids


def test_load_and_register_home_config_rejects_unknown_room(tmp_path):
    config = create_test_config()
    config["devices"][0]["room_id"] = "missing_room"

    config_path = tmp_path / "home.json"
    write_config(config_path, config)

    room_registry = RoomRegistry()
    device_registry = DeviceRegistry()

    with pytest.raises(HomeConfigValidationError):
        load_and_register_home_config(
            config_path=config_path,
            room_registry=room_registry,
            device_registry=device_registry,
        )

def test_load_home_config_supports_home_assistant_device(tmp_path):
    config = {
        "rooms": [
            {
                "id": "office",
                "name": "Office",
                "floor_id": "ground_floor",
            }
        ],
        "devices": [
            {
                "id": "light.office.home_assistant_test",
                "name": "Office Home Assistant Test Light",
                "device_type": "light",
                "room_id": "office",
                "adapter_id": "home_assistant",
                "state": "unknown",
                "online": True,
                "capabilities": [
                    {
                        "capability_type": "power",
                        "name": "Power",
                        "metadata": None,
                    }
                ],
                "attributes": {
                    "home_assistant_entity_id": "light.office_test",
                },
            }
        ],
    }

    config_path = tmp_path / "home_assistant_home.json"
    write_config(config_path, config)

    home_config = load_home_config(config_path)
    device = home_config.devices[0]

    assert device.adapter_id == "home_assistant"
    assert device.attributes["home_assistant_entity_id"] == "light.office_test"

def test_load_home_config_rejects_duplicate_room_ids(tmp_path):
    config = create_test_config()
    config["rooms"].append(
        {
            "id": "office",
            "name": "Duplicate Office",
            "floor_id": "ground_floor",
        }
    )

    config_path = tmp_path / "home.json"
    write_config(config_path, config)

    with pytest.raises(HomeConfigValidationError) as error:
        load_home_config(config_path)

    assert "Duplicate room ID" in str(error.value)


def test_load_home_config_rejects_duplicate_device_ids(tmp_path):
    config = create_test_config()
    config["devices"].append(config["devices"][0].copy())

    config_path = tmp_path / "home.json"
    write_config(config_path, config)

    with pytest.raises(HomeConfigValidationError) as error:
        load_home_config(config_path)

    assert "Duplicate device ID" in str(error.value)


def test_load_home_config_rejects_device_missing_required_field(tmp_path):
    config = create_test_config()
    del config["devices"][0]["room_id"]

    config_path = tmp_path / "home.json"
    write_config(config_path, config)

    with pytest.raises(HomeConfigValidationError) as error:
        load_home_config(config_path)

    assert "Device config is missing required field" in str(error.value)


def test_load_home_config_rejects_room_missing_required_field(tmp_path):
    config = create_test_config()
    del config["rooms"][0]["floor_id"]

    config_path = tmp_path / "home.json"
    write_config(config_path, config)

    with pytest.raises(HomeConfigValidationError) as error:
        load_home_config(config_path)

    assert "Room config is missing required field" in str(error.value)


def test_load_home_config_rejects_home_assistant_device_without_entity_id(tmp_path):
    config = create_test_config()
    config["devices"][0]["adapter_id"] = "home_assistant"
    config["devices"][0]["attributes"] = {}

    config_path = tmp_path / "home.json"
    write_config(config_path, config)

    with pytest.raises(HomeConfigValidationError) as error:
        load_home_config(config_path)

    assert "home_assistant_entity_id" in str(error.value)