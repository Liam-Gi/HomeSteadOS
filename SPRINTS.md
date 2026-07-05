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

---

## Sprint 8 - Application Runtime

### Goal

Create a central application runtime that wires together HomeSteadOS core components.

This prevents each interface from manually constructing registries, services, adapters, and event systems differently.

### Planned Work

- Create HomeSteadOSRuntime
- Create empty runtime factory
- Create demo runtime factory
- Move demo device registration out of the CLI
- Update CLI to use the runtime
- Add event log command to CLI
- Add runtime tests
- Add CLI event log tests

### Out of Scope

- HTTP API
- Database persistence
- Real hardware
- AI
- Voice

### Progress

- Created HomeSteadOSRuntime
- Created runtime factory
- Created demo runtime factory
- Moved demo device registration out of the CLI
- Updated CLI to use the runtime
- Added CLI event log command
- Added runtime tests

---

## Sprint 9 - HTTP API

### Goal

Create the first HTTP API for HomeSteadOS.

The API allows external tools, dashboards, mobile apps, and future integrations to interact with HomeSteadOS through a standard interface.

### Planned Work

- Add FastAPI dependency
- Create API schemas
- Create API app factory
- Add system status endpoint
- Add device listing endpoint
- Add single device endpoint
- Add action endpoint
- Add event log endpoint
- Add API tests

### Out of Scope

- Authentication
- Web dashboard
- Mobile app
- Real hardware
- AI
- Voice

### Progress

- Added FastAPI dependency
- Created API schemas
- Created API app factory
- Added system status endpoint
- Added device listing endpoint
- Added single device endpoint
- Added action request endpoint
- Added event log endpoint
- Added API tests

---

## Sprint 10 - Room Awareness

### Goal

Make rooms a functional part of HomeSteadOS.

This sprint adds room registration, room-level device lookup, room-level lighting actions, CLI room commands, and API room endpoints.

### Planned Work

- Add demo rooms to the runtime
- Link demo devices to rooms
- Create RoomService
- Add room listing command to CLI
- Add room status command to CLI
- Add room-level lighting commands
- Add room endpoints to API
- Add room service tests
- Add API room tests

### Out of Scope

- Real hardware
- AI
- Voice
- Home Assistant
- Persistent storage

### Progress

- Created RoomService
- Added demo rooms to runtime
- Linked demo devices to rooms
- Added CLI room commands
- Added API room endpoints
- Added room service tests

---

## Sprint 11 - System Modes

### Goal

Add basic system mode support to HomeSteadOS.

System modes allow HomeSteadOS to understand broad household context such as Home, Away, Night, Guest, and Vacation modes.

### Planned Work

- Add SystemMode enum
- Create SystemState model
- Create SystemService
- Add runtime system service wiring
- Add CLI system mode commands
- Add API system mode endpoints
- Add system service tests
- Add API system mode tests

### Out of Scope

- Advanced safety policies
- User permissions
- Scheduling
- AI behaviour changes
- Persistent storage

### Progress

- Added SystemMode enum
- Created SystemState model
- Created SystemService
- Added system mode change events
- Added CLI mode commands
- Added API mode endpoints
- Added system service tests