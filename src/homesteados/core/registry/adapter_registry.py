"""Registry for device adapters known to HomeSteadOS."""

from homesteados.core.ports.device_adapter import DeviceAdapter


class AdapterRegistry:
    """Stores and retrieves device adapters by adapter ID."""

    def __init__(self) -> None:
        self._adapters: dict[str, DeviceAdapter] = {}

    def register_adapter(self, adapter: DeviceAdapter) -> None:
        """Register a device adapter.

        Adapter IDs must be unique.
        """

        if adapter.adapter_id in self._adapters:
            raise ValueError(
                f"Adapter with ID '{adapter.adapter_id}' is already registered."
            )

        self._adapters[adapter.adapter_id] = adapter

    def get_adapter(self, adapter_id: str) -> DeviceAdapter | None:
        """Return an adapter by ID."""

        return self._adapters.get(adapter_id)

    def list_adapters(self) -> list[DeviceAdapter]:
        """Return all registered adapters."""

        return list(self._adapters.values())

    def clear(self) -> None:
        """Remove all registered adapters."""

        self._adapters.clear()