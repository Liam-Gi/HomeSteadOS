# Sprint 0
### Progress
```markdown

- Created clean project structure
- Added initial Python package layout
- Added placeholder modules
- Created Product Requirements Document
- Created System Architecture Document
- Created Development Standards document
- Created Version Roadmap
- Updated README
- Updated Vision document
- Updated root Roadmap
- Updated Changelog
- Completed ADR-0001 Core Architecture

---

## Sprint 1 - Core Domain Models

### Goal

Create the first real domain models for HomeSteadOS.

This sprint defines how the system represents homes, floors, rooms, devices, capabilities, and actions.

### Planned Work

- Create shared enums
- Create Capability model
- Create Device model
- Create Room model
- Create Floor model
- Create Home model
- Create Action model
- Add unit tests for core domain behaviour

### Out of Scope

- Device registry
- Device control
- Services
- Adapters
- AI
- Voice
- Home Assistant

### Progress

- Created shared domain enums
- Created Capability model
- Created Device model
- Created Room model
- Created Floor model
- Created Home model
- Created Action model
- Added initial domain tests

---

## Sprint 2 - Registries

### Goal

Create central registries for rooms and devices.

Registries allow HomeSteadOS to register, remove, find, and list known objects without spreading lookup logic across the system.

### Planned Work

- Create DeviceRegistry
- Create RoomRegistry
- Add tests for registering devices
- Add tests for finding devices by ID
- Add tests for finding devices by room
- Add tests for finding devices by type
- Add tests for finding devices by capability
- Add tests for registering and finding rooms

### Out of Scope

- Device control
- Services
- Adapters
- AI
- Voice
- Home Assistant

### Progress

- Created DeviceRegistry
- Created RoomRegistry
- Added device registration tests
- Added room registration tests
- Added lookup tests for devices and rooms

---

## Sprint 3 - Core Services

### Goal

Create controlled service operations for HomeSteadOS.

Services provide the official way for interfaces, APIs, and future AI systems to request actions.

### Planned Work

- Create ActionResult model
- Create basic SafetyEngine
- Create LightingService
- Add tests for lighting service behaviour
- Add tests for safety engine behaviour

### Out of Scope

- Hardware adapters
- Home Assistant
- MQTT
- AI planning
- Voice control

### Progress

- Created ActionResult model
- Created basic SafetyEngine
- Created LightingService
- Added lighting service tests
- Added safety engine tests