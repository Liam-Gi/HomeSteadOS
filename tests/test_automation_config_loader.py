"""Tests for automation config loading."""

import json

import pytest

from homesteados.config.automation_config_loader import (
    AutomationConfigValidationError,
    load_and_register_automation_config,
    load_automation_config,
)
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.core.events.event_types import EventType
from homesteados.core.registry.automation_rule_registry import AutomationRuleRegistry
from homesteados.runtime import create_demo_runtime


def test_load_automation_config_reads_automations(tmp_path):
    config_path = tmp_path / "automations.json"
    config_path.write_text(
        json.dumps(
            {
                "automations": [
                    {
                        "id": "test-rule",
                        "name": "Test Rule",
                        "trigger_event_type": "system_mode_changed",
                        "trigger_payload_matches": {
                            "new_mode": "night",
                        },
                        "action": {
                            "action_type": "turn_off",
                            "target_id": "kitchen",
                            "target_type": "room",
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    data = load_automation_config(config_path)

    assert len(data["automations"]) == 1
    assert data["automations"][0]["id"] == "test-rule"


def test_load_and_register_automation_config_registers_rule(tmp_path):
    config_path = tmp_path / "automations.json"
    config_path.write_text(
        json.dumps(
            {
                "automations": [
                    {
                        "id": "test-rule",
                        "name": "Test Rule",
                        "enabled": True,
                        "trigger_event_type": "system_mode_changed",
                        "trigger_payload_matches": {
                            "new_mode": "night",
                        },
                        "action": {
                            "action_type": "turn_off",
                            "target_id": "kitchen",
                            "target_type": "room",
                            "requested_by": "automation",
                            "risk_level": "low",
                            "requires_confirmation": False,
                            "parameters": {},
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    registry = AutomationRuleRegistry()

    load_and_register_automation_config(
        config_path=config_path,
        automation_rule_registry=registry,
    )

    rule = registry.get_rule_by_id("test-rule")

    assert rule is not None
    assert rule.trigger_event_type == EventType.SYSTEM_MODE_CHANGED
    assert rule.action.action_type == ActionType.TURN_OFF
    assert rule.action.target_type == ActionTargetType.ROOM


def test_automation_config_rejects_missing_automations_field(tmp_path):
    config_path = tmp_path / "automations.json"
    config_path.write_text(
        json.dumps({}),
        encoding="utf-8",
    )

    with pytest.raises(AutomationConfigValidationError):
        load_automation_config(config_path)


def test_automation_config_rejects_duplicate_rule_ids(tmp_path):
    config_path = tmp_path / "automations.json"
    config_path.write_text(
        json.dumps(
            {
                "automations": [
                    {
                        "id": "duplicate-rule",
                        "name": "First Rule",
                        "trigger_event_type": "system_mode_changed",
                        "action": {
                            "action_type": "turn_off",
                            "target_id": "kitchen",
                            "target_type": "room",
                        },
                    },
                    {
                        "id": "duplicate-rule",
                        "name": "Second Rule",
                        "trigger_event_type": "system_mode_changed",
                        "action": {
                            "action_type": "turn_on",
                            "target_id": "kitchen",
                            "target_type": "room",
                        },
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(AutomationConfigValidationError):
        load_automation_config(config_path)


def test_demo_runtime_loads_automation_config():
    runtime = create_demo_runtime()

    rule = runtime.automation_rule_registry.get_rule_by_id(
        "night-turn-off-kitchen"
    )

    assert rule is not None
    assert rule.name == "Turn off kitchen lights in Night mode"