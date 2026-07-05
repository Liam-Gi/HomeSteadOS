"""Core port for device adapter implementations."""

from typing import Protocol

from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.results.action_result import ActionResult


class DeviceAdapter(Protocol):
    """Interface that all device adapters must implement."""

    adapter_id: str

    def execute_action(self, action: Action, device: Device) -> ActionResult:
        """Execute an action against a device."""