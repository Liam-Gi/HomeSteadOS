"""Tests for command history service behaviour."""

from homesteados.core.domain.action import Action
from homesteados.core.domain.enums import ActionTargetType, ActionType
from homesteados.core.results.action_result import ActionResult
from homesteados.core.services.command_history_service import CommandHistoryService


def test_command_history_records_preview():
    service = CommandHistoryService()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="office",
        target_type=ActionTargetType.ROOM,
        requested_by="test",
    )

    service.record_preview(
        command="turn on office light",
        requested_by="test",
        success=True,
        message="Parsed.",
        action=action,
        description="Turn on Office.",
    )

    entries = service.list_entries()

    assert len(entries) == 1
    assert entries[0].mode == "preview"
    assert entries[0].command == "turn on office light"
    assert entries[0].action_type == "turn_on"
    assert entries[0].target_id == "office"


def test_command_history_records_execution():
    service = CommandHistoryService()

    action = Action(
        action_type=ActionType.TURN_ON,
        target_id="office",
        target_type=ActionTargetType.ROOM,
        requested_by="test",
    )

    result = ActionResult.ok(
        message="Office lights turned on.",
        data={
            "example": True,
        },
    )

    service.record_execution(
        command="turn on office light",
        requested_by="test",
        result=result,
        action=action,
        description="Turn on Office.",
    )

    entries = service.list_entries()

    assert len(entries) == 1
    assert entries[0].mode == "execute"
    assert entries[0].success is True
    assert entries[0].result_data["example"] is True


def test_command_history_can_clear_entries():
    service = CommandHistoryService()

    service.record_preview(
        command="bad command",
        requested_by="test",
        success=False,
        message="Failed.",
    )

    service.clear()

    assert service.list_entries() == []