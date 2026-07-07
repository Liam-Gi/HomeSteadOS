"""Loader for shortcut configuration files."""

import json
from pathlib import Path
from typing import Any

from homesteados.core.domain.shortcut import Shortcut
from homesteados.core.registry.shortcut_registry import ShortcutRegistry


class ShortcutConfigValidationError(ValueError):
    """Raised when shortcut configuration is invalid."""


def load_shortcut_config(config_path: Path) -> dict[str, Any]:
    """Load a shortcut config file."""

    with config_path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    _validate_shortcut_config(data)

    return data


def load_and_register_shortcut_config(
    config_path: Path,
    shortcut_registry: ShortcutRegistry,
) -> None:
    """Load shortcut config and register shortcuts."""

    data = load_shortcut_config(config_path)

    for shortcut_data in data["shortcuts"]:
        shortcut_registry.register_shortcut(
            _parse_shortcut(shortcut_data)
        )


def _validate_shortcut_config(data: dict[str, Any]) -> None:
    """Validate shortcut config structure."""

    if "shortcuts" not in data:
        raise ShortcutConfigValidationError(
            "Shortcut config must contain a 'shortcuts' field."
        )

    if not isinstance(data["shortcuts"], list):
        raise ShortcutConfigValidationError(
            "Shortcut config field 'shortcuts' must be a list."
        )

    seen_shortcut_ids: set[str] = set()

    for shortcut_data in data["shortcuts"]:
        _validate_shortcut(shortcut_data)

        shortcut_id = shortcut_data["id"]

        if shortcut_id in seen_shortcut_ids:
            raise ShortcutConfigValidationError(
                f"Duplicate shortcut ID '{shortcut_id}'."
            )

        seen_shortcut_ids.add(shortcut_id)


def _validate_shortcut(shortcut_data: dict[str, Any]) -> None:
    """Validate one shortcut config."""

    required_fields = [
        "id",
        "name",
        "command",
    ]

    for field in required_fields:
        if field not in shortcut_data:
            raise ShortcutConfigValidationError(
                f"Shortcut is missing required field '{field}'."
            )

    if not isinstance(shortcut_data["command"], str):
        raise ShortcutConfigValidationError(
            "Shortcut field 'command' must be a string."
        )


def _parse_shortcut(shortcut_data: dict[str, Any]) -> Shortcut:
    """Parse shortcut config into a Shortcut."""

    return Shortcut(
        id=shortcut_data["id"],
        name=shortcut_data["name"],
        command=shortcut_data["command"],
        enabled=shortcut_data.get("enabled", True),
    )