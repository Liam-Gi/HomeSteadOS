"""Tests for behaviour insight service behaviour."""

from homesteados.runtime import create_demo_runtime


def test_behaviour_insights_empty_when_no_history():
    runtime = create_demo_runtime()

    insights = runtime.behaviour_insight_service.generate_insights()

    assert insights == []


def test_behaviour_insights_detect_repeated_successful_command():
    runtime = create_demo_runtime()

    action = runtime.text_command_service.parse_text(
        "turn on office light",
        requested_by="test",
    ).action

    assert action is not None

    for _ in range(3):
        result = runtime.action_dispatcher.execute(action)

        runtime.command_history_service.record_execution(
            command="turn on office light",
            requested_by="test",
            result=result,
            action=action,
            description="Turn on all supported devices in room 'Office'.",
        )

    insights = runtime.behaviour_insight_service.generate_insights()

    assert len(insights) == 1
    assert insights[0].insight_type == "repeated_command"
    assert insights[0].data["command"] == "turn on office light"
    assert insights[0].data["count"] == 3