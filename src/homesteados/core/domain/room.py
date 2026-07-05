"""Domain model for a room within the home."""

from dataclasses import dataclass, field


@dataclass
class Room:
    """Represents a physical room or area in the home."""

    id: str
    name: str
    floor_id: str
    device_ids: list[str] = field(default_factory=list)

    def add_device(self, device_id: str) -> None:
        """Add a device ID to the room if it is not already present."""

        if device_id not in self.device_ids:
            self.device_ids.append(device_id)

    def remove_device(self, device_id: str) -> None:
        """Remove a device ID from the room if present."""

        if device_id in self.device_ids:
            self.device_ids.remove(device_id)