"""Domain model for devices known to HomeSteadOS."""

from dataclasses import dataclass, field
from typing import Any

from homesteados.core.domain.capability import Capability
from homesteados.core.domain.enums import DeviceState, DeviceType


@dataclass
class Device:
    """Represents a device known to HomeSteadOS.

    A Device is a logical representation of something in the home.
    It does not directly know how to control real hardware.
    Hardware-specific behaviour belongs in adapters.
    """

    id: str
    name: str
    device_type: DeviceType
    room_id: str
    adapter_id: str = "simulated"
    state: DeviceState = DeviceState.UNKNOWN
    online: bool = True
    capabilities: list[Capability] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)

    def supports_capability(self, capability_type: str) -> bool:
        """Return True if the device supports the provided capability."""

        return any(
            capability.capability_type.value == capability_type
            for capability in self.capabilities
        )

    def set_state(self, new_state: DeviceState) -> None:
        """Update the logical state of the device."""

        self.state = new_state

    def mark_online(self) -> None:
        """Mark the device as online."""

        self.online = True

    def mark_offline(self) -> None:
        """Mark the device as offline."""

        self.online = False