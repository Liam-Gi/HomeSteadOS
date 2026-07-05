"""Tests for safety engine behaviour."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionType
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