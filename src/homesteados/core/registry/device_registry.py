"""Registry for devices known to HomeSteadOS."""

from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import CapabilityType, DeviceType


class DeviceRegistry:
    """Stores and retrieves devices known to HomeSteadOS."""

    def __init__(self) -> None:
        self._devices: dict[str, Device] = {}

    def register_device(self, device: Device) -> None:
        """Register a device.

        Device IDs must be unique.
        """

        if device.id in self._devices:
            raise ValueError(f"Device with ID '{device.id}' is already registered.")

        self._devices[device.id] = device

    def remove_device(self, device_id: str) -> Device | None:
        """Remove a device by ID."""

        return self._devices.pop(device_id, None)

    def get_device_by_id(self, device_id: str) -> Device | None:
        """Return a device by ID."""

        return self._devices.get(device_id)

    def find_device_by_name(self, name: str) -> Device | None:
        """Find a device by display name.

        Name matching is case-insensitive.
        """

        normalised_name = name.lower()

        for device in self._devices.values():
            if device.name.lower() == normalised_name:
                return device

        return None

    def list_devices(self) -> list[Device]:
        """Return all registered devices."""

        return list(self._devices.values())

    def find_devices_by_room(self, room_id: str) -> list[Device]:
        """Return all devices in a room."""

        return [
            device
            for device in self._devices.values()
            if device.room_id == room_id
        ]

    def find_devices_by_type(self, device_type: DeviceType | str) -> list[Device]:
        """Return all devices matching a device type."""

        device_type_value = (
            device_type.value if isinstance(device_type, DeviceType) else device_type
        )

        return [
            device
            for device in self._devices.values()
            if device.device_type.value == device_type_value
        ]

    def find_devices_by_capability(
        self,
        capability_type: CapabilityType | str,
    ) -> list[Device]:
        """Return all devices supporting a capability."""

        capability_value = (
            capability_type.value
            if isinstance(capability_type, CapabilityType)
            else capability_type
        )

        return [
            device
            for device in self._devices.values()
            if device.supports_capability(capability_value)
        ]

    def clear(self) -> None:
        """Remove all registered devices."""

        self._devices.clear()