"""Command-line interface entry point for HomeSteadOS."""

from homesteados.config.logging_config import configure_logging
from homesteados.config.settings import get_settings
from homesteados.interfaces.cli.command_parser import CommandParser
from homesteados.runtime import create_demo_runtime


def main() -> None:
    """Run the HomeSteadOS CLI."""

    settings = get_settings()
    configure_logging(settings.log_level)

    runtime = create_demo_runtime(
        config_path=settings.demo_config_path,
        settings=settings,
    )

    command_parser = CommandParser(
        device_registry=runtime.device_registry,
        lighting_service=runtime.lighting_service,
        room_service=runtime.room_service,
        system_service=runtime.system_service,
        scene_service=runtime.scene_service,
        text_command_service=runtime.text_command_service,
        action_description_service=runtime.action_description_service,
        diagnostics_service=runtime.diagnostics_service,
        audit_log_service=runtime.audit_log_service,
        confirmation_service=runtime.confirmation_service,
        automation_service=runtime.automation_service,
        event_bus=runtime.event_bus,
    )


    print("HomeSteadOS CLI Prototype")
    print(f"Environment: {settings.environment}")
    print(f"Config: {settings.demo_config_path}")
    print("Type 'help' for commands.")
    print("Type 'exit' to quit.\n")

    while True:
        command = input("> ").strip()

        if command.lower() in {"exit", "quit"}:
            print("Shutting down HomeSteadOS.")
            break

        response = command_parser.handle(command)
        print(response)


if __name__ == "__main__":
    main()