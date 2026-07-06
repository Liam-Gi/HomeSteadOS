"""Tests for HomeSteadOS application settings."""

from pathlib import Path

from homesteados.config.settings import (
    DEFAULT_DEMO_CONFIG_PATH,
    get_settings,
)


def test_get_settings_uses_defaults(monkeypatch):
    monkeypatch.delenv("HOMESTEADOS_ENV", raising=False)
    monkeypatch.delenv("HOMESTEADOS_LOG_LEVEL", raising=False)
    monkeypatch.delenv("HOMESTEADOS_DEMO_CONFIG", raising=False)

    settings = get_settings()

    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.demo_config_path == DEFAULT_DEMO_CONFIG_PATH


def test_get_settings_reads_environment_variables(monkeypatch, tmp_path):
    custom_config_path = tmp_path / "custom_home.json"

    monkeypatch.setenv("HOMESTEADOS_ENV", "test")
    monkeypatch.setenv("HOMESTEADOS_LOG_LEVEL", "debug")
    monkeypatch.setenv(
        "HOMESTEADOS_DEMO_CONFIG",
        str(custom_config_path),
    )

    settings = get_settings()

    assert settings.environment == "test"
    assert settings.log_level == "DEBUG"
    assert settings.demo_config_path == Path(custom_config_path)