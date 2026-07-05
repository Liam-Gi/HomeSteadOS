"""Tests for the device domain model."""

from homesteados.core.domain.capability import Capability
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import CapabilityType, DeviceState, DeviceType


def test_device_can_change_state():
    device = Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
    )

    device.set_state(DeviceState.ON)

    assert device.state == DeviceState.ON


def test_device_can_be_marked_offline():
    device = Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
    )

    device.mark_offline()

    assert device.online is False


def test_device_supports_capability():
    device = Device(
        id="light.office.ceiling",
        name="Office Ceiling Light",
        device_type=DeviceType.LIGHT,
        room_id="office",
        capabilities=[
            Capability(
                capability_type=CapabilityType.POWER,
                name="Power",
            )
        ],
    )

    assert device.supports_capability("power") is True