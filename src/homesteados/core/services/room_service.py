"""Service for room-level operations."""

from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import DeviceType
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.results.action_result import ActionResult
from homesteados.core.services.lighting_service import LightingService


class RoomService:
    """Provides controlled room-level operations."""

    def __init__(
        self,
        room_registry: RoomRegistry,
        device_registry: DeviceRegistry,
        lighting_service: LightingService,
    ) -> None:
        self.room_registry = room_registry
        self.device_registry = device_registry
        self.lighting_service = lighting_service

    def list_devices_in_room(self, room_id: str) -> list[Device]:
        """Return all devices registered in a room."""

        return self.device_registry.find_devices_by_room(room_id)

    def turn_on_room_lights(
        self,
        room_id: str,
        requested_by: str = "system",
    ) -> ActionResult:
        """Turn on all lights in a room."""

        return self._set_room_lights(
            room_id=room_id,
            turn_on=True,
            requested_by=requested_by,
        )

    def turn_off_room_lights(
        self,
        room_id: str,
        requested_by: str = "system",
    ) -> ActionResult:
        """Turn off all lights in a room."""

        return self._set_room_lights(
            room_id=room_id,
            turn_on=False,
            requested_by=requested_by,
        )

    def _set_room_lights(
        self,
        room_id: str,
        turn_on: bool,
        requested_by: str,
    ) -> ActionResult:
        """Turn all lights in a room on or off."""

        room = self.room_registry.get_room_by_id(room_id)

        if room is None:
            return ActionResult.fail(
                message=f"Room '{room_id}' was not found.",
                reason="No registered room matched the provided room ID.",
            )

        devices = self.device_registry.find_devices_by_room(room_id)

        lights = [
            device
            for device in devices
            if device.device_type == DeviceType.LIGHT
        ]

        if not lights:
            return ActionResult.fail(
                message=f"No lights found in room '{room_id}'.",
                reason="Room exists, but no registered light devices were found.",
            )

        results = []

        for light in lights:
            if turn_on:
                result = self.lighting_service.turn_on_light(
                    light.id,
                    requested_by=requested_by,
                )
            else:
                result = self.lighting_service.turn_off_light(
                    light.id,
                    requested_by=requested_by,
                )

            results.append(result)

        failed_results = [
            result
            for result in results
            if not result.success
        ]

        action_name = "turned on" if turn_on else "turned off"

        if failed_results:
            return ActionResult.fail(
                message=f"Some lights in room '{room_id}' could not be {action_name}.",
                reason="One or more lighting actions failed.",
                data={
                    "room_id": room_id,
                    "results": [
                        result.message
                        for result in results
                    ],
                },
            )

        return ActionResult.ok(
            message=f"All lights in {room.name} {action_name}.",
            data={
                "room_id": room_id,
                "light_count": len(lights),
                "results": [
                    result.message
                    for result in results
                ],
            },
        )