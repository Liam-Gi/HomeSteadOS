"""Tests for the room registry."""

import pytest

from homesteados.core.domain.room import Room
from homesteados.core.registry.room_registry import RoomRegistry


def create_office() -> Room:
    return Room(
        id="office",
        name="Office",
        floor_id="ground_floor",
    )


def test_register_room_adds_room_to_registry():
    registry = RoomRegistry()
    room = create_office()

    registry.register_room(room)

    assert registry.get_room_by_id("office") == room


def test_registering_duplicate_room_id_raises_error():
    registry = RoomRegistry()
    room = create_office()

    registry.register_room(room)

    with pytest.raises(ValueError):
        registry.register_room(room)


def test_remove_room_removes_room_from_registry():
    registry = RoomRegistry()
    room = create_office()

    registry.register_room(room)
    removed_room = registry.remove_room("office")

    assert removed_room == room
    assert registry.get_room_by_id("office") is None


def test_find_room_by_name_is_case_insensitive():
    registry = RoomRegistry()
    room = create_office()

    registry.register_room(room)

    found_room = registry.find_room_by_name("office")

    assert found_room == room


def test_list_rooms_returns_registered_rooms():
    registry = RoomRegistry()
    office = create_office()
    kitchen = Room(
        id="kitchen",
        name="Kitchen",
        floor_id="ground_floor",
    )

    registry.register_room(office)
    registry.register_room(kitchen)

    rooms = registry.list_rooms()

    assert office in rooms
    assert kitchen in rooms