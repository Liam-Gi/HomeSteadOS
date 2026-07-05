"""Tests for the home, floor, and room domain models."""

from homesteados.core.domain.floor import Floor
from homesteados.core.domain.home import Home
from homesteados.core.domain.room import Room


def test_home_can_add_and_find_room():
    home = Home(id="home.primary", name="Primary Home")
    ground_floor = Floor(id="ground_floor", name="Ground Floor")
    office = Room(id="office", name="Office", floor_id="ground_floor")

    ground_floor.add_room(office)
    home.add_floor(ground_floor)

    found_room = home.find_room("office")

    assert found_room is not None
    assert found_room.name == "Office"


def test_room_can_add_device_id():
    room = Room(id="office", name="Office", floor_id="ground_floor")

    room.add_device("light.office.ceiling")

    assert "light.office.ceiling" in room.device_ids


def test_room_does_not_duplicate_device_ids():
    room = Room(id="office", name="Office", floor_id="ground_floor")

    room.add_device("light.office.ceiling")
    room.add_device("light.office.ceiling")

    assert room.device_ids.count("light.office.ceiling") == 1