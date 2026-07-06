# Home Assistant Setup

## Purpose

HomeSteadOS can use Home Assistant as a hardware integration adapter.

Home Assistant is not the HomeSteadOS brain. It acts as an external platform that HomeSteadOS can send device commands to.

## Environment Variables

To enable the Home Assistant adapter, set:

```powershell
$env:HOMESTEADOS_HOME_ASSISTANT_ENABLED="true"
$env:HOMESTEADOS_HOME_ASSISTANT_URL="http://homeassistant.local:8123"
$env:HOMESTEADOS_HOME_ASSISTANT_TOKEN="your-token-here"
Device Configuration

A Home Assistant-backed device must use:

"adapter_id": "home_assistant"

It must also include a Home Assistant entity ID:

"attributes": {
  "home_assistant_entity_id": "light.office_test"
}
Example Device
{
  "id": "light.office.home_assistant_test",
  "name": "Office Home Assistant Test Light",
  "device_type": "light",
  "room_id": "office",
  "adapter_id": "home_assistant",
  "state": "unknown",
  "online": true,
  "capabilities": [
    {
      "capability_type": "power",
      "name": "Power",
      "metadata": null
    }
  ],
  "attributes": {
    "home_assistant_entity_id": "light.office_test"
  }
}
```
Current Status

The Home Assistant adapter currently supports:

turn_on
turn_off

State synchronisation is not implemented yet.