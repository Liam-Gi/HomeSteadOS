"""Service for creating HomeSteadOS system snapshots."""

from homesteados.core.registry.automation_rule_registry import AutomationRuleRegistry
from homesteados.core.registry.device_registry import DeviceRegistry
from homesteados.core.registry.pending_action_store import PendingActionStore
from homesteados.core.registry.room_registry import RoomRegistry
from homesteados.core.registry.scene_registry import SceneRegistry
from homesteados.core.registry.shortcut_registry import ShortcutRegistry
from homesteados.core.results.system_snapshot import (
    DeviceSnapshot,
    RoomSnapshot,
    SystemSnapshot,
)
from homesteados.core.services.command_history_service import CommandHistoryService
from homesteados.core.services.system_service import SystemService


class SystemSnapshotService:
    """Creates a read-only snapshot of current HomeSteadOS state."""

    def __init__(
        self,
        system_service: SystemService,
        room_registry: RoomRegistry,
        device_registry: DeviceRegistry,
        scene_registry: SceneRegistry,
        automation_rule_registry: AutomationRuleRegistry,
        shortcut_registry: ShortcutRegistry,
        pending_action_store: PendingActionStore,
        command_history_service: CommandHistoryService,
    ) -> None:
        self.system_service = system_service
        self.room_registry = room_registry
        self.device_registry = device_registry
        self.scene_registry = scene_registry
        self.automation_rule_registry = automation_rule_registry
        self.shortcut_registry = shortcut_registry
        self.pending_action_store = pending_action_store
        self.command_history_service = command_history_service

    def create_snapshot(self) -> SystemSnapshot:
        """Create a system snapshot."""

        rooms = [
            RoomSnapshot(
                id=room.id,
                name=room.name,
                floor_id=room.floor_id,
                device_count=len(room.device_ids),
            )
            for room in self.room_registry.list_rooms()
        ]

        devices = [
            DeviceSnapshot(
                id=device.id,
                name=device.name,
                device_type=device.device_type.value,
                room_id=device.room_id,
                state=device.state.value,
                online=device.online,
                adapter_id=device.adapter_id,
            )
            for device in self.device_registry.list_devices()
        ]

        automation_rules = self.automation_rule_registry.list_rules()

        online_count = sum(1 for device in devices if device.online)
        offline_count = len(devices) - online_count

        return SystemSnapshot(
            system_mode=self.system_service.get_mode().value,
            rooms=rooms,
            devices=devices,
            scene_count=len(self.scene_registry.list_scenes()),
            automation_count=len(automation_rules),
            enabled_automation_count=sum(
                1
                for rule in automation_rules
                if rule.enabled
            ),
            shortcut_count=len(self.shortcut_registry.list_shortcuts()),
            pending_action_count=len(self.pending_action_store.list_actions()),
            command_history_count=len(
                self.command_history_service.list_entries()
            ),
            metadata={
                "room_count": len(rooms),
                "device_count": len(devices),
                "online_device_count": online_count,
                "offline_device_count": offline_count,
            },
        )