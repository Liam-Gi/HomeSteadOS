"""Manual Home Assistant connection check script."""

from homesteados.adapters.home_assistant.home_assistant_adapter import (
    HomeAssistantAdapter,
)
from homesteados.config.settings import get_settings


def main() -> None:
    """Run a Home Assistant connection check."""

    settings = get_settings()
    ha_settings = settings.home_assistant

    if not ha_settings.enabled:
        print("Home Assistant integration is not enabled.")
        return

    if not ha_settings.base_url or not ha_settings.access_token:
        print("Home Assistant URL or token is missing.")
        return

    adapter = HomeAssistantAdapter(
        base_url=ha_settings.base_url,
        access_token=ha_settings.access_token,
    )

    result = adapter.check_connection()

    print(result.message)

    if result.reason:
        print(f"Reason: {result.reason}")

    if result.data:
        print(f"Data: {result.data}")


if __name__ == "__main__":
    main()