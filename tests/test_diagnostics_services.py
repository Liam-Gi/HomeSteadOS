"""Tests for diagnostics service behaviour."""

from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceType, HealthStatus
from homesteados.runtime import create_demo_runtime, create_runtime


def test_demo_runtime_health_is_ok():
    runtime = create_demo_runtime()

    report = runtime.diagnostics_service.get_health_report()

    assert report.status == HealthStatus.OK


def test_empty_runtime_health_has_warnings():
    runtime = create_runtime()

    report = runtime.diagnostics_service.get_health_report()

    assert report.status == HealthStatus.WARNING


def test_health_report_detects_offline_devices():
    runtime = create_demo_runtime()

    device = runtime.device_registry.get_device_by_id("light.office.ceiling")
    assert device is not None

    device.mark_offline()

    report = runtime.diagnostics_service.get_health_report()

    check = next(
        check
        for check in report.checks
        if check.name == "offline_devices"
    )

    assert report.status == HealthStatus.WARNING
    assert check.status == HealthStatus.WARNING
    assert "light.office.ceiling" in check.data["offline_devices"]


def test_health_report_detects_missing_adapter():
    runtime = create_runtime()

    device = Device(
        id="light.test.missing_adapter",
        name="Missing Adapter Light",
        device_type=DeviceType.LIGHT,
        room_id="test_room",
        adapter_id="missing_adapter",
    )

    runtime.device_registry.register_device(device)

    report = runtime.diagnostics_service.get_health_report()

    check = next(
        check
        for check in report.checks
        if check.name == "missing_adapters"
    )

    assert report.status == HealthStatus.ERROR
    assert check.status == HealthStatus.ERROR

def test_health_report_detects_home_assistant_device_without_adapter():
    runtime = create_runtime()

    device = Device(
        id="light.office.home_assistant_test",
        name="Office Home Assistant Test Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        adapter_id="home_assistant",
        attributes={
            "home_assistant_entity_id": "light.office_test",
        },
    )

    runtime.device_registry.register_device(device)

    report = runtime.diagnostics_service.get_health_report()

    missing_adapter_check = next(
        check
        for check in report.checks
        if check.name == "missing_adapters"
    )

    assert report.status == HealthStatus.ERROR
    assert missing_adapter_check.status == HealthStatus.ERROR