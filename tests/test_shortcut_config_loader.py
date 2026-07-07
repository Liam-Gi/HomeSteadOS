"""Tests for shortcut config loading."""

import json

import pytest

from homesteados.config.shortcut_config_loader import (
    ShortcutConfigValidationError,
    load_and_register_shortcut_config,
    load_shortcut_config,
)
from homesteados.core.registry.shortcut_registry import ShortcutRegistry


def test_load_shortcut_config_reads_shortcuts(tmp_path):
    config_path = tmp_path / "shortcuts.json"
    config_path.write_text(
        json.dumps(
            {
                "shortcuts": [
                    {
                        "id": "test-shortcut",
                        "name": "Test Shortcut",
                        "command": "turn on office light",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    data = load_shortcut_config(config_path)

    assert len(data["shortcuts"]) == 1
    assert data["shortcuts"][0]["id"] == "test-shortcut"


def test_load_and_register_shortcut_config_registers_shortcut(tmp_path):
    config_path = tmp_path / "shortcuts.json"
    config_path.write_text(
        json.dumps(
            {
                "shortcuts": [
                    {
                        "id": "test-shortcut",
                        "name": "Test Shortcut",
                        "command": "turn on office light",
                        "enabled": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    registry = ShortcutRegistry()

    load_and_register_shortcut_config(
        config_path=config_path,
        shortcut_registry=registry,
    )

    shortcut = registry.get_shortcut_by_id("test-shortcut")

    assert shortcut is not None
    assert shortcut.name == "Test Shortcut"
    assert shortcut.command == "turn on office light"


def test_shortcut_config_rejects_missing_shortcuts_field(tmp_path):
    config_path = tmp_path / "shortcuts.json"
    config_path.write_text(
        json.dumps({}),
        encoding="utf-8",
    )

    with pytest.raises(ShortcutConfigValidationError):
        load_shortcut_config(config_path)


def test_shortcut_config_rejects_duplicate_shortcut_ids(tmp_path):
    config_path = tmp_path / "shortcuts.json"
    config_path.write_text(
        json.dumps(
            {
                "shortcuts": [
                    {
                        "id": "duplicate",
                        "name": "First",
                        "command": "turn on office light",
                    },
                    {
                        "id": "duplicate",
                        "name": "Second",
                        "command": "turn off office light",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ShortcutConfigValidationError):
        load_shortcut_config(config_path)