"""Command-line interface entry point for HomeSteadOS."""

from homesteados.interfaces.cli.command_parser import CommandParser
from homesteados.runtime import create_demo_runtime


def main() -> None:
    """Run the HomeSteadOS CLI."""

    runtime = create_demo_runtime()

    command_parser = CommandParser(
        device_registry=runtime.device_registry,
        lighting_service=runtime.lighting_service,
        room_service=runtime.room_service,
        system_service=runtime.system_service,
        event_bus=runtime.event_bus,
    )

    print("HomeSteadOS CLI Prototype")
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