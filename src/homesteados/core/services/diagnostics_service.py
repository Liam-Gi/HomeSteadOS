"""Service for HomeSteadOS diagnostics and health reporting."""

from homesteados.core.domain.enums import HealthStatus
from homesteados.core.domain.system_state import SystemState
from homesteados.core.events.event_bus import EventBus
from homesteados.core.registry.adapter_registry import AdapterRegistry
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.results.system_health import HealthCheck, SystemHealthReport


class DiagnosticsService:
    """Provides system diagnostics and health reporting."""

    def __init__(
        self,
        device_registry: DeviceRegistry,
        room_registry: RoomRegistry,
        adapter_registry: AdapterRegistry,
        event_bus: EventBus,
        system_state: SystemState,
    ) -> None:
        self.device_registry = device_registry
        self.room_registry = room_registry
        self.adapter_registry = adapter_registry
        self.event_bus = event_bus
        self.system_state = system_state

    def get_health_report(self) -> SystemHealthReport:
        """Return a system health report."""

        checks = [
            self._check_adapters(),
            self._check_rooms(),
            self._check_devices(),
            self._check_offline_devices(),
            self._check_missing_adapters(),
            self._check_event_bus(),
        ]

        overall_status = self._calculate_overall_status(checks)

        return SystemHealthReport(
            status=overall_status,
            checks=checks,
            summary={
                "mode": self.system_state.mode.value,
                "device_count": len(self.device_registry.list_devices()),
                "room_count": len(self.room_registry.list_rooms()),
                "adapter_count": len(self.adapter_registry.list_adapters()),
                "event_count": len(self.event_bus.list_published_events()),
            },
        )

    def _check_adapters(self) -> HealthCheck:
        """Check whether adapters are registered."""

        adapter_count = len(self.adapter_registry.list_adapters())

        if adapter_count == 0:
            return HealthCheck(
                name="adapters",
                status=HealthStatus.ERROR,
                message="No adapters are registered.",
                data={"adapter_count": adapter_count},
            )

        return HealthCheck(
            name="adapters",
            status=HealthStatus.OK,
            message=f"{adapter_count} adapter(s) registered.",
            data={"adapter_count": adapter_count},
        )

    def _check_rooms(self) -> HealthCheck:
        """Check whether rooms are registered."""

        room_count = len(self.room_registry.list_rooms())

        if room_count == 0:
            return HealthCheck(
                name="rooms",
                status=HealthStatus.WARNING,
                message="No rooms are registered.",
                data={"room_count": room_count},
            )

        return HealthCheck(
            name="rooms",
            status=HealthStatus.OK,
            message=f"{room_count} room(s) registered.",
            data={"room_count": room_count},
        )

    def _check_devices(self) -> HealthCheck:
        """Check whether devices are registered."""

        device_count = len(self.device_registry.list_devices())

        if device_count == 0:
            return HealthCheck(
                name="devices",
                status=HealthStatus.WARNING,
                message="No devices are registered.",
                data={"device_count": device_count},
            )

        return HealthCheck(
            name="devices",
            status=HealthStatus.OK,
            message=f"{device_count} device(s) registered.",
            data={"device_count": device_count},
        )

    def _check_offline_devices(self) -> HealthCheck:
        """Check for offline devices."""

        offline_devices = [
            device
            for device in self.device_registry.list_devices()
            if not device.online
        ]

        if offline_devices:
            return HealthCheck(
                name="offline_devices",
                status=HealthStatus.WARNING,
                message=f"{len(offline_devices)} offline device(s) found.",
                data={
                    "offline_devices": [
                        device.id
                        for device in offline_devices
                    ],
                },
            )

        return HealthCheck(
            name="offline_devices",
            status=HealthStatus.OK,
            message="No offline devices found.",
        )

    def _check_missing_adapters(self) -> HealthCheck:
        """Check for devices referencing missing adapters."""

        missing_adapter_devices = [
            device
            for device in self.device_registry.list_devices()
            if self.adapter_registry.get_adapter(device.adapter_id) is None
        ]

        if missing_adapter_devices:
            return HealthCheck(
                name="missing_adapters",
                status=HealthStatus.ERROR,
                message=(
                    f"{len(missing_adapter_devices)} device(s) reference "
                    "missing adapters."
                ),
                data={
                    "devices": [
                        {
                            "device_id": device.id,
                            "adapter_id": device.adapter_id,
                        }
                        for device in missing_adapter_devices
                    ],
                },
            )

        return HealthCheck(
            name="missing_adapters",
            status=HealthStatus.OK,
            message="All device adapters are registered.",
        )

    def _check_event_bus(self) -> HealthCheck:
        """Check event bus status."""

        event_count = len(self.event_bus.list_published_events())

        return HealthCheck(
            name="event_bus",
            status=HealthStatus.OK,
            message="Event bus is available.",
            data={"event_count": event_count},
        )

    def _calculate_overall_status(
        self,
        checks: list[HealthCheck],
    ) -> HealthStatus:
        """Calculate overall status from individual checks."""

        statuses = [
            check.status
            for check in checks
        ]

        if HealthStatus.ERROR in statuses:
            return HealthStatus.ERROR

        if HealthStatus.WARNING in statuses:
            return HealthStatus.WARNING

        return HealthStatus.OK