"""Domain model for the full home structure."""

from dataclasses import dataclass, field

from homesteados.core.domain.floor import Floor
from homesteados.core.domain.room import Room


@dataclass
class Home:
    """Represents the full home known to HomeSteadOS."""

    id: str
    name: str
    floors: dict[str, Floor] = field(default_factory=dict)

    def add_floor(self, floor: Floor) -> None:
        """Add a floor to the home."""

        self.floors[floor.id] = floor

    def get_floor(self, floor_id: str) -> Floor | None:
        """Return a floor by ID."""

        return self.floors.get(floor_id)

    def list_floors(self) -> list[Floor]:
        """Return all floors in the home."""

        return list(self.floors.values())

    def find_room(self, room_id: str) -> Room | None:
        """Find a room anywhere in the home."""

        for floor in self.floors.values():
            room = floor.get_room(room_id)
            if room is not None:
                return room

        return None

    def list_rooms(self) -> list[Room]:
        """Return all rooms across all floors."""

        rooms: list[Room] = []

        for floor in self.floors.values():
            rooms.extend(floor.list_rooms())

        return rooms