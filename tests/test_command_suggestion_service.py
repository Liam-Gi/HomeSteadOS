"""Tests for command suggestion service behaviour."""

from homesteados.runtime import create_demo_runtime


def test_command_suggestions_include_room_light_commands():
    runtime = create_demo_runtime()

    suggestions = runtime.command_suggestion_service.suggest_commands(
        "office bright"
    )

    assert "turn on office light" in suggestions
    assert "turn off office light" in suggestions


def test_command_suggestions_include_scene_commands():
    runtime = create_demo_runtime()

    suggestions = runtime.command_suggestion_service.suggest_commands(
        "good night"
    )

    assert "run good night" in suggestions
    assert "run scene good-night" in suggestions


def test_command_suggestions_include_system_mode_commands():
    runtime = create_demo_runtime()

    suggestions = runtime.command_suggestion_service.suggest_commands(
        "night mode"
    )

    assert "set mode night" in suggestions


def test_text_command_parse_failure_includes_suggestions():
    runtime = create_demo_runtime()

    result = runtime.text_command_service.parse_text(
        "make office bright",
        requested_by="test",
    )

    assert result.success is False
    assert "turn on office light" in result.suggestions