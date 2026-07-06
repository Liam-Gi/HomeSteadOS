"""Tests for safety engine behaviour."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionRisk, ActionType, SystemMode
from homesteados.core.domain.system_state import SystemState
from homesteados.core.safety.safety_engine import SafetyEngine


def test_safety_engine_allows_basic_action():
    safety_engine = SafetyEngine()
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
    )

    decision = safety_engine.review_action(action)

    assert decision.allowed is True
    assert decision.requires_confirmation is False


def test_safety_engine_requires_confirmation_when_action_requires_it():
    safety_engine = SafetyEngine()
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        requires_confirmation=True,
    )

    decision = safety_engine.review_action(action)

    assert decision.allowed is False
    assert decision.requires_confirmation is True


def test_safety_engine_requires_confirmation_for_high_risk_action():
    safety_engine = SafetyEngine()
    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="lock.front_door.primary",
        risk_level=ActionRisk.HIGH,
    )

    decision = safety_engine.review_action(action)

    assert decision.allowed is False
    assert decision.requires_confirmation is True
    assert "High-risk" in decision.reason


def test_safety_engine_blocks_critical_risk_action():
    safety_engine = SafetyEngine()
    action = Action(
        action_type=ActionType.TURN_OFF,
        target_id="camera.driveway.main",
        risk_level=ActionRisk.CRITICAL,
    )

    decision = safety_engine.review_action(action)

    assert decision.allowed is False
    assert decision.requires_confirmation is False
    assert "Critical-risk" in decision.reason


def test_safety_engine_requires_confirmation_for_ai_action_in_away_mode():
    system_state = SystemState()
    system_state.set_mode(SystemMode.AWAY)

    safety_engine = SafetyEngine(system_state=system_state)

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        requested_by="ai",
    )

    decision = safety_engine.review_action(action)

    assert decision.allowed is False
    assert decision.requires_confirmation is True
    assert "AI-requested actions" in decision.reason


def test_safety_engine_allows_cli_action_in_away_mode():
    system_state = SystemState()
    system_state.set_mode(SystemMode.AWAY)

    safety_engine = SafetyEngine(system_state=system_state)

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="light.office.ceiling",
        requested_by="cli",
    )

    decision = safety_engine.review_action(action)

    assert decision.allowed is True
    assert decision.requires_confirmation is False