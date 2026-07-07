"""Tests for system snapshot service behaviour."""

from homesteados.runtime import create_demo_runtime


def test_system_snapshot_contains_basic_counts():
    runtime = create_demo_runtime()

    snapshot = runtime.system_snapshot_service.create_snapshot()

    assert snapshot.system_mode == "home"
    assert snapshot.metadata["room_count"] == 3
    assert snapshot.metadata["device_count"] == 3
    assert snapshot.scene_count >= 1
    assert snapshot.automation_count >= 1
    assert snapshot.shortcut_count >= 1


def test_system_snapshot_reflects_device_state_changes():
    runtime = create_demo_runtime()

    runtime.text_command_service.execute_text(
        "turn on office light",
        requested_by="test",
    )

    snapshot = runtime.system_snapshot_service.create_snapshot()

    office_device = next(
        device
        for device in snapshot.devices
        if device.id == "light.office.ceiling"
    )

    assert office_device.state == "on"


def test_system_snapshot_reflects_command_history_count():
    runtime = create_demo_runtime()

    runtime.command_history_service.record_preview(
        command="turn on office light",
        requested_by="test",
        success=True,
        message="Text command parsed.",
    )

    snapshot = runtime.system_snapshot_service.create_snapshot()

    assert snapshot.command_history_count == 1