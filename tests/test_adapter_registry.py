"""Tests for the adapter registry."""

import pytest

from homesteados.adapters.simulated.simulated_device_adapter import (
    SimulatedDeviceAdapter,
)
from homesteados.core.registry.adapter_registry import AdapterRegistry


def test_register_adapter_adds_adapter_to_registry():
    registry = AdapterRegistry()
    adapter = SimulatedDeviceAdapter()

    registry.register_adapter(adapter)

    assert registry.get_adapter("simulated") == adapter


def test_registering_duplicate_adapter_id_raises_error():
    registry = AdapterRegistry()
    adapter = SimulatedDeviceAdapter()

    registry.register_adapter(adapter)

    with pytest.raises(ValueError):
        registry.register_adapter(adapter)


def test_get_unknown_adapter_returns_none():
    registry = AdapterRegistry()

    adapter = registry.get_adapter("missing")

    assert adapter is None


def test_list_adapters_returns_registered_adapters():
    registry = AdapterRegistry()
    adapter = SimulatedDeviceAdapter()

    registry.register_adapter(adapter)

    assert adapter in registry.list_adapters()