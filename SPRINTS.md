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

---

## Sprint 4 - CLI Prototype

### Goal

Create a simple command-line interface that allows HomeSteadOS to control in-memory devices through the service layer.

### Planned Work

- Add CLI command parser
- Add demo in-memory devices
- Allow lights to be turned on and off by friendly command
- Add device listing and status commands
- Add CLI command parser tests

### Out of Scope

- AI
- Voice
- Home Assistant
- MQTT
- Real hardware
- Persistent storage

### Progress

- Created CLI command parser
- Created CLI entry point
- Added demo in-memory devices
- Added commands for help, devices, status, turn on, and turn off
- Added CLI command parser tests

---

## Sprint 5 - Adapter Execution

### Goal

Refactor device execution so services use adapters instead of directly changing device state.

This completes the first simulated device control path and prepares the architecture for future Home Assistant and MQTT integrations.

### Planned Work

- Add core adapter port
- Add simulated device adapter
- Refactor LightingService to use adapter execution
- Update CLI to use simulated adapter
- Add simulated adapter tests
- Update architecture documentation

### Out of Scope

- Home Assistant
- MQTT
- Real hardware
- AI
- Voice

### Progress

- Created core DeviceAdapter port
- Created SimulatedDeviceAdapter
- Refactored LightingService to execute actions through adapters
- Updated CLI to use the simulated adapter
- Added simulated adapter tests

---

## Sprint 6 - Adapter Registry

### Goal

Create an adapter registry so HomeSteadOS can support multiple device adapters.

This prepares the system for future simulated, Home Assistant, MQTT, and other hardware integrations.

### Planned Work

- Create AdapterRegistry
- Register adapters by adapter ID
- Refactor LightingService to resolve adapters dynamically
- Update CLI to use AdapterRegistry
- Add adapter registry tests
- Update existing service and CLI tests

### Out of Scope

- Home Assistant implementation
- MQTT implementation
- Real hardware
- AI
- Voice

### Progress

- Created AdapterRegistry
- Refactored LightingService to resolve adapters dynamically
- Updated CLI to register the simulated adapter
- Updated lighting service tests
- Updated CLI command parser tests
- Added adapter registry tests

---

## Sprint 7 - Event Bus

### Goal

Create an internal event system for HomeSteadOS.

The Event Bus allows the system to publish important events such as action requests, action completions, action failures, and device state changes.

### Planned Work

- Create EventType definitions
- Create Event model
- Create EventBus
- Add event publishing to LightingService
- Add tests for event publishing and subscription
- Add tests for lighting state change events

### Out of Scope

- MQTT events
- Persistent event storage
- Automation triggers
- Notifications
- AI memory
- Real hardware

### Progress

- Created EventType definitions
- Created Event model
- Created EventBus
- Added event publishing to LightingService
- Added EventBus tests
- Added lighting service event tests