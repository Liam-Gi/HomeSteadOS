"""Loader for scene configuration files."""

import json
from pathlib import Path
from typing import Any

from homesteados.core.domain.action import Action
from homesteados.core.domain.scene import Scene
from homesteados.core.domain.enums import ActionRisk, ActionTargetType, ActionType
from homesteados.core.registry.scene_registry import SceneRegistry


class SceneConfigValidationError(ValueError):
    """Raised when scene configuration is invalid."""


def load_scene_config(config_path: Path) -> dict[str, Any]:
    """Load a scene config file."""

    with config_path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    _validate_scene_config(data)

    return data


def load_and_register_scene_config(
    config_path: Path,
    scene_registry: SceneRegistry,
) -> None:
    """Load scene config and register scenes."""

    data = load_scene_config(config_path)

    for scene_data in data["scenes"]:
        scene_registry.register_scene(
            _parse_scene(scene_data)
        )


def _validate_scene_config(data: dict[str, Any]) -> None:
    """Validate scene config structure."""

    if "scenes" not in data:
        raise SceneConfigValidationError(
            "Scene config must contain a 'scenes' field."
        )

    if not isinstance(data["scenes"], list):
        raise SceneConfigValidationError(
            "Scene config field 'scenes' must be a list."
        )

    seen_scene_ids: set[str] = set()

    for scene_data in data["scenes"]:
        _validate_scene(scene_data)

        scene_id = scene_data["id"]

        if scene_id in seen_scene_ids:
            raise SceneConfigValidationError(
                f"Duplicate scene ID '{scene_id}'."
            )

        seen_scene_ids.add(scene_id)


def _validate_scene(scene_data: dict[str, Any]) -> None:
    """Validate one scene config."""

    required_fields = [
        "id",
        "name",
        "actions",
    ]

    for field in required_fields:
        if field not in scene_data:
            raise SceneConfigValidationError(
                f"Scene is missing required field '{field}'."
            )

    if not isinstance(scene_data["actions"], list):
        raise SceneConfigValidationError(
            "Scene field 'actions' must be a list."
        )

    for action_data in scene_data["actions"]:
        _validate_action(action_data)


def _validate_action(action_data: dict[str, Any]) -> None:
    """Validate scene action config."""

    required_fields = [
        "action_type",
        "target_id",
        "target_type",
    ]

    for field in required_fields:
        if field not in action_data:
            raise SceneConfigValidationError(
                f"Scene action is missing required field '{field}'."
            )

    if "parameters" in action_data and not isinstance(
        action_data["parameters"],
        dict,
    ):
        raise SceneConfigValidationError(
            "Scene action field 'parameters' must be an object."
        )


def _parse_scene(scene_data: dict[str, Any]) -> Scene:
    """Parse scene config into a Scene."""

    return Scene(
        id=scene_data["id"],
        name=scene_data["name"],
        enabled=scene_data.get("enabled", True),
        actions=[
            _parse_action(action_data)
            for action_data in scene_data["actions"]
        ],
    )


def _parse_action(action_data: dict[str, Any]) -> Action:
    """Parse scene action config into an Action."""

    return Action(
        action_type=_parse_action_type(action_data["action_type"]),
        target_id=action_data["target_id"],
        target_type=_parse_action_target_type(action_data["target_type"]),
        requested_by=action_data.get("requested_by", "scene"),
        parameters=action_data.get("parameters", {}),
        requires_confirmation=action_data.get("requires_confirmation", False),
        risk_level=_parse_action_risk(action_data.get("risk_level", "low")),
    )


def _parse_action_type(value: str) -> ActionType:
    """Parse an action type value."""

    try:
        return ActionType(value)
    except ValueError as error:
        raise SceneConfigValidationError(
            f"Unknown action type '{value}'."
        ) from error


def _parse_action_target_type(value: str) -> ActionTargetType:
    """Parse an action target type value."""

    try:
        return ActionTargetType(value)
    except ValueError as error:
        raise SceneConfigValidationError(
            f"Unknown action target type '{value}'."
        ) from error


def _parse_action_risk(value: str) -> ActionRisk:
    """Parse an action risk value."""

    try:
        return ActionRisk(value)
    except ValueError as error:
        raise SceneConfigValidationError(
            f"Unknown action risk '{value}'."
        ) from error