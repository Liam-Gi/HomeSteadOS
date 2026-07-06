"""Application settings for HomeSteadOS."""

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DEMO_CONFIG_PATH = PROJECT_ROOT / "configs" / "demo_home.json"


@dataclass(frozen=True)
class HomeAssistantSettings:
    """Settings for Home Assistant integration."""

    enabled: bool
    base_url: str | None
    access_token: str | None


@dataclass(frozen=True)
class AppSettings:
    """Application settings for HomeSteadOS."""

    environment: str
    log_level: str
    demo_config_path: Path
    home_assistant: HomeAssistantSettings


def get_settings() -> AppSettings:
    """Load application settings from environment variables."""

    demo_config_path = os.getenv("HOMESTEADOS_DEMO_CONFIG")

    home_assistant_enabled = os.getenv(
        "HOMESTEADOS_HOME_ASSISTANT_ENABLED",
        "false",
    ).lower() in {"true", "1", "yes"}

    return AppSettings(
        environment=os.getenv("HOMESTEADOS_ENV", "development"),
        log_level=os.getenv("HOMESTEADOS_LOG_LEVEL", "INFO").upper(),
        demo_config_path=(
            Path(demo_config_path)
            if demo_config_path
            else DEFAULT_DEMO_CONFIG_PATH
        ),
        home_assistant=HomeAssistantSettings(
            enabled=home_assistant_enabled,
            base_url=os.getenv("HOMESTEADOS_HOME_ASSISTANT_URL"),
            access_token=os.getenv("HOMESTEADOS_HOME_ASSISTANT_TOKEN"),
        ),
    )