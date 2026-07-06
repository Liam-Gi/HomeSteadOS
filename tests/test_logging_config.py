"""Tests for HomeSteadOS logging configuration."""

import logging

from homesteados.config.logging_config import configure_logging


def test_configure_logging_sets_log_level():
    configure_logging("DEBUG")

    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_falls_back_to_info_for_unknown_level():
    configure_logging("NOT_A_LEVEL")

    assert logging.getLogger().level == logging.INFO