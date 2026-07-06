



# Changelog

All notable changes to HomeSteadOS will be documented in this file.

This project currently uses simple early-stage versioning.

---

## v0.1 - Foundation

Status: In progress

### Added

- Clean Python `src` project layout
- `homesteados` source package
- Placeholder modules for core, adapters, interfaces, AI, and config
- Initial tests folder
- Documentation folder structure
- Product Requirements Document
- System Architecture Document
- Development Standards document
- Version Roadmap document
- Initial `.gitignore`
- Initial `pyproject.toml`

### Notes

This version focuses on project structure, documentation, and architecture. No functional home automation features have been implemented yet.

## v0.2 - Core Domain

Status: In progress

### Added

- Shared domain enums
- Capability model
- Device model
- Room model
- Floor model
- Home model
- Action model
- Basic domain model tests

## v0.3 - Registries

Status: In progress

### Added

- DeviceRegistry
- RoomRegistry
- Device lookup by ID, name, room, type, and capability
- Room lookup by ID and name
- Registry unit tests

## v0.4 - Services

Status: In progress

### Added

- ActionResult model
- Basic SafetyEngine
- LightingService
- Lighting service tests
- Safety engine tests

## v0.5 - Simulation

Status: In progress

### Added

- CLI prototype
- Demo in-memory devices
- Friendly command parser
- Device listing command
- Device status command
- CLI command parser tests

### Changed

- Refactored LightingService so device state changes are executed through a device adapter instead of directly inside the service.

### Added

- Core device adapter port
- SimulatedDeviceAdapter
- Simulated adapter tests
### Added

- AdapterRegistry
- Dynamic adapter lookup for device execution
- Adapter registry tests

### Changed

- LightingService now resolves the correct adapter using AdapterRegistry instead of receiving a single adapter directly.

## v0.6 - Events

Status: In progress

### Added

- EventType definitions
- Event model
- EventBus
- Action requested events
- Action completed events
- Action failed events
- Action blocked events
- Device state changed events
- EventBus tests
- Lighting event tests

## v0.6.1 - Application Runtime

Status: In progress

### Added

- HomeSteadOSRuntime
- Runtime factory
- Demo runtime factory
- CLI event log command
- Runtime tests

### Changed

- CLI now uses the central HomeSteadOS runtime instead of manually wiring registries, adapters, services, and events.

## v0.7 - API

Status: In progress

### Added

- FastAPI HTTP API
- API app factory
- System status endpoint
- Device listing endpoint
- Single device endpoint
- Action request endpoint
- Event log endpoint
- API tests

## v0.7.1 - Room Awareness

Status: In progress

### Added

- RoomService
- Demo room registration
- Room/device linking
- CLI room commands
- API room endpoints
- Room service tests

## v0.7.2 - System Modes

Status: In progress

### Added

- SystemMode enum
- SystemState model
- SystemService
- System mode change event
- CLI system mode commands
- API system mode endpoints
- System service tests

## v0.7.3 - Mode-Aware Safety

Status: In progress

### Added

- ActionRisk enum
- Action risk level support
- Mode-aware SafetyEngine
- High-risk confirmation rule
- Critical-risk block rule
- AI confirmation rule for Away and Vacation modes
- Runtime safety engine wiring
- Additional safety tests

## v0.7.4 - Action Dispatcher

Status: In progress

### Added

- ActionTargetType enum
- Action target type support
- ActionDispatcher
- Device action routing
- Room action routing
- System action routing
- Action dispatcher tests

### Changed

- API action endpoint now submits structured actions through ActionDispatcher instead of manually calling services.

## v0.7.5 - Config-Driven Runtime

Status: In progress

### Added

- Demo home JSON configuration file
- Home config loader
- Config-based room registration
- Config-based device registration
- Config loader tests

### Changed

- Demo runtime now loads rooms and devices from `configs/demo_home.json` instead of hard-coded Python objects.

## v0.7.6 - Settings and Logging

Status: In progress

### Added

- AppSettings model
- Environment-based settings loading
- Configurable demo config path
- Logging configuration
- Settings tests
- Logging tests

### Changed

- CLI now loads runtime configuration through application settings.
- API app factory now loads runtime configuration through application settings when no runtime is supplied.

## v0.7.7 - Diagnostics and Health

Status: In progress

### Added

- HealthStatus enum
- HealthCheck model
- SystemHealthReport model
- DiagnosticsService
- CLI health command
- API health endpoint
- Diagnostics tests

## v0.8 - Home Assistant Adapter Skeleton

Status: In progress

### Added

- Home Assistant settings
- Optional Home Assistant adapter registration
- HomeAssistantAdapter
- Home Assistant turn_on service call support
- Home Assistant turn_off service call support
- Home Assistant adapter tests

### Changed

- Runtime can now register the Home Assistant adapter when Home Assistant settings are enabled.

## v0.8.1 - Home Assistant Device Configuration

Status: In progress

### Added

- Home Assistant sample home configuration
- Support for Home Assistant-backed device definitions
- Tests for loading Home Assistant-backed devices
- Home Assistant setup documentation