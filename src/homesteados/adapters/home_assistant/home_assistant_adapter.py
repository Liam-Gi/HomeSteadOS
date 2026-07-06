"""Adapter for Home Assistant integration."""

from typing import Any

import requests

from homesteados.core.domain.action import Action
from homesteados.core.domain.device import Device
from homesteados.core.domain.enums import ActionType
from homesteados.core.results.action_result import ActionResult


class HomeAssistantAdapter:
    """Executes HomeSteadOS actions through Home Assistant."""

    adapter_id = "home_assistant"

    def __init__(
        self,
        base_url: str,
        access_token: str,
        http_client: Any = requests,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self.http_client = http_client

    def execute_action(self, action: Action, device: Device) -> ActionResult:
        """Execute an action against a Home Assistant entity."""

        if device.adapter_id != self.adapter_id:
            return ActionResult.fail(
                message=f"Device '{device.id}' is not handled by the Home Assistant adapter.",
                reason=(
                    f"Device adapter_id is '{device.adapter_id}', "
                    f"but this adapter handles '{self.adapter_id}'."
                ),
                action_id=action.id,
            )

        entity_id = device.attributes.get("home_assistant_entity_id")

        if not entity_id:
            return ActionResult.fail(
                message=f"Device '{device.id}' is missing a Home Assistant entity ID.",
                reason=(
                    "Expected device.attributes['home_assistant_entity_id'] "
                    "to contain a Home Assistant entity ID."
                ),
                action_id=action.id,
            )

        if action.action_type == ActionType.TURN_ON:
            return self._call_service(
                domain="homeassistant",
                service="turn_on",
                entity_id=entity_id,
                action=action,
                device=device,
            )

        if action.action_type == ActionType.TURN_OFF:
            return self._call_service(
                domain="homeassistant",
                service="turn_off",
                entity_id=entity_id,
                action=action,
                device=device,
            )

        return ActionResult.fail(
            message=f"Action '{action.action_type.value}' is not supported by Home Assistant adapter.",
            reason="Home Assistant adapter currently supports only turn_on and turn_off.",
            action_id=action.id,
        )

    def _call_service(
        self,
        domain: str,
        service: str,
        entity_id: str,
        action: Action,
        device: Device,
    ) -> ActionResult:
        """Call a Home Assistant service."""

        url = f"{self.base_url}/api/services/{domain}/{service}"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "entity_id": entity_id,
        }

        try:
            response = self.http_client.post(
                url,
                headers=headers,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            return ActionResult.fail(
                message=f"Home Assistant service call failed for '{device.id}'.",
                reason=str(error),
                action_id=action.id,
                data={
                    "entity_id": entity_id,
                    "service": service,
                },
            )

        return ActionResult.ok(
            message=f"{device.name} {service.replace('_', ' ')} request sent to Home Assistant.",
            action_id=action.id,
            data={
                "device_id": device.id,
                "entity_id": entity_id,
                "adapter_id": self.adapter_id,
                "service": service,
            },
        )