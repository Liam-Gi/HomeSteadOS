"""Loader for automation rule configuration files."""

import json
from pathlib import Path
from typing import Any

from homesteados.core.domain.action import Action
from homesteados.core.domain.automation_rule import AutomationRule
from homesteados.core.domain.enums import ActionRisk, ActionTargetType, ActionType
from homesteados.core.events.event_types import EventType
from homesteados.core.registry.automation_rule_registry import AutomationRuleRegistry


class AutomationConfigValidationError(ValueError):
    """Raised when automation configuration is invalid."""


def load_automation_config(config_path: Path) -> dict[str, Any]:
    """Load an automation config file."""

    with config_path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    _validate_automation_config(data)

    return data


def load_and_register_automation_config(
    config_path: Path,
    automation_rule_registry: AutomationRuleRegistry,
) -> None:
    """Load automation config and register automation rules."""

    data = load_automation_config(config_path)

    for rule_data in data["automations"]:
        automation_rule_registry.register_rule(
            _parse_automation_rule(rule_data)
        )


def _validate_automation_config(data: dict[str, Any]) -> None:
    """Validate automation config structure."""

    if "automations" not in data:
        raise AutomationConfigValidationError(
            "Automation config must contain an 'automations' field."
        )

    if not isinstance(data["automations"], list):
        raise AutomationConfigValidationError(
            "Automation config field 'automations' must be a list."
        )

    seen_rule_ids: set[str] = set()

    for rule_data in data["automations"]:
        _validate_rule(rule_data)

        rule_id = rule_data["id"]

        if rule_id in seen_rule_ids:
            raise AutomationConfigValidationError(
                f"Duplicate automation rule ID '{rule_id}'."
            )

        seen_rule_ids.add(rule_id)


def _validate_rule(rule_data: dict[str, Any]) -> None:
    """Validate one automation rule config."""

    required_fields = [
        "id",
        "name",
        "trigger_event_type",
        "action",
    ]

    for field in required_fields:
        if field not in rule_data:
            raise AutomationConfigValidationError(
                f"Automation rule is missing required field '{field}'."
            )

    if "trigger_payload_matches" in rule_data and not isinstance(
        rule_data["trigger_payload_matches"],
        dict,
    ):
        raise AutomationConfigValidationError(
            "Automation rule field 'trigger_payload_matches' must be an object."
        )

    if not isinstance(rule_data["action"], dict):
        raise AutomationConfigValidationError(
            "Automation rule field 'action' must be an object."
        )

    _validate_action(rule_data["action"])


def _validate_action(action_data: dict[str, Any]) -> None:
    """Validate automation action config."""

    required_fields = [
        "action_type",
        "target_id",
        "target_type",
    ]

    for field in required_fields:
        if field not in action_data:
            raise AutomationConfigValidationError(
                f"Automation action is missing required field '{field}'."
            )

    if "parameters" in action_data and not isinstance(
        action_data["parameters"],
        dict,
    ):
        raise AutomationConfigValidationError(
            "Automation action field 'parameters' must be an object."
        )


def _parse_automation_rule(rule_data: dict[str, Any]) -> AutomationRule:
    """Parse automation rule config into an AutomationRule."""

    return AutomationRule(
        id=rule_data["id"],
        name=rule_data["name"],
        enabled=rule_data.get("enabled", True),
        trigger_event_type=_parse_event_type(rule_data["trigger_event_type"]),
        trigger_payload_matches=rule_data.get("trigger_payload_matches", {}),
        action=_parse_action(rule_data["action"]),
    )


def _parse_action(action_data: dict[str, Any]) -> Action:
    """Parse automation action config into an Action."""

    return Action(
        action_type=_parse_action_type(action_data["action_type"]),
        target_id=action_data["target_id"],
        target_type=_parse_action_target_type(action_data["target_type"]),
        requested_by=action_data.get("requested_by", "automation"),
        parameters=action_data.get("parameters", {}),
        requires_confirmation=action_data.get("requires_confirmation", False),
        risk_level=_parse_action_risk(action_data.get("risk_level", "low")),
    )


def _parse_event_type(value: str) -> EventType:
    """Parse an event type value."""

    try:
        return EventType(value)
    except ValueError as error:
        raise AutomationConfigValidationError(
            f"Unknown event type '{value}'."
        ) from error


def _parse_action_type(value: str) -> ActionType:
    """Parse an action type value."""

    try:
        return ActionType(value)
    except ValueError as error:
        raise AutomationConfigValidationError(
            f"Unknown action type '{value}'."
        ) from error


def _parse_action_target_type(value: str) -> ActionTargetType:
    """Parse an action target type value."""

    try:
        return ActionTargetType(value)
    except ValueError as error:
        raise AutomationConfigValidationError(
            f"Unknown action target type '{value}'."
        ) from error


def _parse_action_risk(value: str) -> ActionRisk:
    """Parse an action risk value."""

    try:
        return ActionRisk(value)
    except ValueError as error:
        raise AutomationConfigValidationError(
            f"Unknown action risk '{value}'."
        ) from error