"""Registry for rooms known to HomeSteadOS."""

from homesteados.core.domain.room import Room


class RoomRegistry:
    """Stores and retrieves rooms known to HomeSteadOS."""

    def __init__(self) -> None:
        self._rooms: dict[str, Room] = {}

    def register_room(self, room: Room) -> None:
        """Register a room.

        Room IDs must be unique.
        """

        if room.id in self._rooms:
            raise ValueError(f"Room with ID '{room.id}' is already registered.")

        self._rooms[room.id] = room

    def remove_room(self, room_id: str) -> Room | None:
        """Remove a room by ID."""

        return self._rooms.pop(room_id, None)

    def get_room_by_id(self, room_id: str) -> Room | None:
        """Return a room by ID."""

        return self._rooms.get(room_id)

    def find_room_by_name(self, name: str) -> Room | None:
        """Find a room by display name.

        Name matching is case-insensitive.
        """

        normalised_name = name.lower()

        for room in self._rooms.values():
            if room.name.lower() == normalised_name:
                return room

        return None

    def list_rooms(self) -> list[Room]:
        """Return all registered rooms."""

        return list(self._rooms.values())

    def clear(self) -> None:
        """Remove all registered rooms."""

        self._rooms.clear()