"""Tests for scene service behaviour."""

from homesteados.core.domain.enums import DeviceState
from homesteados.runtime import create_demo_runtime


def test_demo_runtime_loads_good_night_scene():
    runtime = create_demo_runtime()

    scene = runtime.scene_registry.get_scene_by_id("good-night")

    assert scene is not None
    assert scene.name == "Good Night"
    assert len(scene.actions) == 3


def test_run_good_night_scene_turns_off_lights():
    runtime = create_demo_runtime()

    runtime.lighting_service.turn_on_light(
        "light.office.ceiling",
        requested_by="test",
    )
    runtime.lighting_service.turn_on_light(
        "light.kitchen.ceiling",
        requested_by="test",
    )
    runtime.lighting_service.turn_on_light(
        "light.bedroom.lamp",
        requested_by="test",
    )

    result = runtime.scene_service.run_scene(
        scene_id="good-night",
        requested_by="test",
    )

    office_light = runtime.device_registry.get_device_by_id("light.office.ceiling")
    kitchen_light = runtime.device_registry.get_device_by_id("light.kitchen.ceiling")
    bedroom_light = runtime.device_registry.get_device_by_id("light.bedroom.lamp")

    assert result.success is True
    assert office_light is not None
    assert kitchen_light is not None
    assert bedroom_light is not None
    assert office_light.state == DeviceState.OFF
    assert kitchen_light.state == DeviceState.OFF
    assert bedroom_light.state == DeviceState.OFF


def test_run_missing_scene_fails():
    runtime = create_demo_runtime()

    result = runtime.scene_service.run_scene(
        scene_id="missing-scene",
        requested_by="test",
    )

    assert result.success is False
    assert "not found" in result.message