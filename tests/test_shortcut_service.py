"""Tests for shortcut service behaviour."""

from homesteados.core.domain.enums import DeviceState
from homesteados.runtime import create_demo_runtime


def test_demo_runtime_loads_shortcuts():
    runtime = create_demo_runtime()

    shortcuts = runtime.shortcut_service.list_shortcuts()

    shortcut_ids = [
        shortcut.id
        for shortcut in shortcuts
    ]

    assert "bedtime" in shortcut_ids
    assert "office-on" in shortcut_ids


def test_run_office_on_shortcut_turns_on_office_light():
    runtime = create_demo_runtime()

    result = runtime.shortcut_service.run_shortcut(
        shortcut_id="office-on",
        requested_by="test",
    )

    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.ON


def test_run_bedtime_shortcut_runs_good_night_scene():
    runtime = create_demo_runtime()

    runtime.text_command_service.execute_text(
        "turn on office light",
        requested_by="test",
    )

    result = runtime.shortcut_service.run_shortcut(
        shortcut_id="bedtime",
        requested_by="test",
    )

    light = runtime.device_registry.get_device_by_id("light.office.ceiling")

    assert result.success is True
    assert light is not None
    assert light.state == DeviceState.OFF


def test_run_missing_shortcut_fails():
    runtime = create_demo_runtime()

    result = runtime.shortcut_service.run_shortcut(
        shortcut_id="missing",
        requested_by="test",
    )

    assert result.success is False
    assert "not found" in result.message