"""Tests for scene config loading."""

import json

import pytest

from homesteados.config.scene_config_loader import (
    SceneConfigValidationError,
    load_and_register_scene_config,
    load_scene_config,
)
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.core.registry.scene_registry import SceneRegistry


def test_load_scene_config_reads_scenes(tmp_path):
    config_path = tmp_path / "scenes.json"
    config_path.write_text(
        json.dumps(
            {
                "scenes": [
                    {
                        "id": "test-scene",
                        "name": "Test Scene",
                        "actions": [
                            {
                                "action_type": "turn_off",
                                "target_id": "kitchen",
                                "target_type": "room",
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    data = load_scene_config(config_path)

    assert len(data["scenes"]) == 1
    assert data["scenes"][0]["id"] == "test-scene"


def test_load_and_register_scene_config_registers_scene(tmp_path):
    config_path = tmp_path / "scenes.json"
    config_path.write_text(
        json.dumps(
            {
                "scenes": [
                    {
                        "id": "test-scene",
                        "name": "Test Scene",
                        "enabled": True,
                        "actions": [
                            {
                                "action_type": "turn_off",
                                "target_id": "kitchen",
                                "target_type": "room",
                                "requested_by": "scene",
                                "risk_level": "low",
                                "requires_confirmation": False,
                                "parameters": {},
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    registry = SceneRegistry()

    load_and_register_scene_config(
        config_path=config_path,
        scene_registry=registry,
    )

    scene = registry.get_scene_by_id("test-scene")

    assert scene is not None
    assert scene.name == "Test Scene"
    assert scene.actions[0].action_type == ActionType.TURN_OFF
    assert scene.actions[0].target_type == ActionTargetType.ROOM


def test_scene_config_rejects_missing_scenes_field(tmp_path):
    config_path = tmp_path / "scenes.json"
    config_path.write_text(
        json.dumps({}),
        encoding="utf-8",
    )

    with pytest.raises(SceneConfigValidationError):
        load_scene_config(config_path)


def test_scene_config_rejects_duplicate_scene_ids(tmp_path):
    config_path = tmp_path / "scenes.json"
    config_path.write_text(
        json.dumps(
            {
                "scenes": [
                    {
                        "id": "duplicate-scene",
                        "name": "First Scene",
                        "actions": [
                            {
                                "action_type": "turn_off",
                                "target_id": "kitchen",
                                "target_type": "room",
                            }
                        ],
                    },
                    {
                        "id": "duplicate-scene",
                        "name": "Second Scene",
                        "actions": [
                            {
                                "action_type": "turn_on",
                                "target_id": "kitchen",
                                "target_type": "room",
                            }
                        ],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(SceneConfigValidationError):
        load_scene_config(config_path)