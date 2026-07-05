


```markdown
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