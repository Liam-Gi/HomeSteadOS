"""Domain model for a floor within the home."""

from dataclasses import dataclass, field

from homesteados.core.domain.room import Room


@dataclass
class Floor:
    """Represents a level within the home."""

    id: str
    name: str
    rooms: dict[str, Room] = field(default_factory=dict)

    def add_room(self, room: Room) -> None:
        """Add a room to the floor."""

        self.rooms[room.id] = room

    def get_room(self, room_id: str) -> Room | None:
        """Return a room by ID."""

        return self.rooms.get(room_id)

    def list_rooms(self) -> list[Room]:
        """Return all rooms on this floor."""

        return list(self.rooms.values())