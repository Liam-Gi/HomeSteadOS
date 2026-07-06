


# HomeSteadOS Roadmap

This file provides a high-level summary of the project roadmap.

For the detailed version plan, see:


docs/product/VERSION_ROADMAP.md

Current Version
v0.1 - Foundation

Status: In progress

Goal:

Create the clean project foundation, product documents, architecture documents, and development standards.

Deliverables:

 Clean Python src layout
 Product Requirements Document
 System Architecture Document
 Development Standards
 Version Roadmap
 Root README updated
 Vision document updated
 Root roadmap updated
 Changelog updated
 ADR-0001 completed
Upcoming Versions
Version	Name	Goal
v0.2	Core Domain	Create home, floor, room, device, action, and capability models
v0.3	Registries	Create device and room registries
v0.4	Services	Add controlled service operations
v0.5	Simulation	Control simulated devices through services
v0.6	Events	Add internal event bus
v0.7	API	Add HTTP API
v0.8	Home Assistant	Control first real device
v0.9	AI Planner	Convert natural language into proposed actions
v1.0	Voice Prototype	Add basic local voice interaction
Development Rule

HomeSteadOS should be developed in this order:

Architecture
  ↓
Core models
  ↓
Registries
  ↓
Services
  ↓
Simulation
  ↓
Events
  ↓
API
  ↓
Real hardware
  ↓
AI
  ↓
Voice

The goal is to build the operating system before automating the house.

## v0.2 - Core Domain

Status: In progress

Deliverables:

- [x] Shared enums
- [x] Capability model
- [x] Device model
- [x] Room model
- [x] Floor model
- [x] Home model
- [x] Action model
- [x] Basic domain tests

## v0.3 - Registries

Status: In progress

Deliverables:

- [x] DeviceRegistry
- [x] RoomRegistry
- [x] Register devices
- [x] Remove devices
- [x] Find devices by ID
- [x] Find devices by name
- [x] Find devices by room
- [x] Find devices by type
- [x] Find devices by capability
- [x] Register rooms
- [x] Remove rooms
- [x] Find rooms by ID
- [x] Find rooms by name
- [x] Basic registry tests

## v0.4 - Services

Status: In progress

Deliverables:

- [x] ActionResult
- [x] Basic SafetyEngine
- [x] LightingService
- [x] Lighting service tests
- [x] Safety engine tests

## v0.5 - Simulation

Status: In progress

Deliverables:

- [x] CLI prototype
- [x] Demo in-memory devices
- [x] Friendly light command parsing
- [x] Device listing command
- [x] Device status command
- [ ] Base adapter interface
- [ ] Simulated device adapter
- [ ] Route actions through adapters


In `ROADMAP.md`, update v0.5:


## v0.5 - Simulation

Status: In progress

Deliverables:

- [x] CLI prototype
- [x] Demo in-memory devices
- [x] Friendly light command parsing
- [x] Device listing command
- [x] Device status command
- [x] Core device adapter port
- [x] Simulated device adapter
- [x] Route lighting actions through adapters
- [x] AdapterRegistry
- [x] Dynamic adapter lookup by adapter ID

## v0.6 - Events

Status: In progress

Deliverables:

- [x] EventType definitions
- [x] Event model
- [x] EventBus
- [x] Event publishing from LightingService
- [x] Action requested events
- [x] Action completed events
- [x] Action failed events
- [x] Action blocked events
- [x] Device state changed events
- [x] EventBus tests
- [x] Lighting event tests

## v0.6.1 - Application Runtime

Status: In progress

Deliverables:

- [x] HomeSteadOSRuntime
- [x] Runtime factory
- [x] Demo runtime factory
- [x] CLI runtime integration
- [x] CLI event log command
- [x] Runtime tests

## v0.7 - API

Status: In progress

Deliverables:

- [x] FastAPI dependency
- [x] API app factory
- [x] System status endpoint
- [x] Device listing endpoint
- [x] Single device endpoint
- [x] Action request endpoint
- [x] Event log endpoint
- [x] API tests

## v0.7.1 - Room Awareness

Status: In progress

Deliverables:

- [x] RoomService
- [x] Demo room registration
- [x] Room/device linking
- [x] CLI room listing
- [x] CLI room status
- [x] CLI room-level light commands
- [x] API room endpoints
- [x] Room service tests

## v0.7.2 - System Modes

Status: In progress

Deliverables:

- [x] SystemMode enum
- [x] SystemState model
- [x] SystemService
- [x] System mode change events
- [x] CLI system mode commands
- [x] API system mode endpoints
- [x] System service tests

## v0.7.3 - Mode-Aware Safety

Status: In progress

Deliverables:

- [x] ActionRisk enum
- [x] Risk level on Action model
- [x] Mode-aware SafetyEngine
- [x] High-risk action confirmation rule
- [x] Critical-risk action block rule
- [x] AI confirmation rule for Away and Vacation modes
- [x] Runtime SafetyEngine wiring
- [x] Safety tests

## v0.7.4 - Action Dispatcher

Status: In progress

Deliverables:

- [x] ActionTargetType enum
- [x] Action target type support
- [x] ActionDispatcher
- [x] Device action routing
- [x] Room action routing
- [x] System action routing
- [x] Runtime dispatcher wiring
- [x] API action endpoint refactor
- [x] Action dispatcher tests

## v0.7.5 - Config-Driven Runtime

Status: In progress

Deliverables:

- [x] Demo home JSON config
- [x] Home config loader
- [x] Room registration from config
- [x] Device registration from config
- [x] Device-to-room linking from config
- [x] Demo runtime loads config file
- [x] Config loader tests

## v0.7.6 - Settings and Logging

Status: In progress

Deliverables:

- [x] AppSettings model
- [x] Environment-based settings loading
- [x] Configurable demo config path
- [x] Logging configuration
- [x] CLI settings integration
- [x] API settings integration
- [x] Settings tests
- [x] Logging tests

## v0.7.7 - Diagnostics and Health

Status: In progress

Deliverables:

- [x] HealthStatus enum
- [x] HealthCheck model
- [x] SystemHealthReport model
- [x] DiagnosticsService
- [x] Runtime diagnostics wiring
- [x] CLI health command
- [x] API health endpoint
- [x] Diagnostics tests

## v0.8 - Home Assistant Adapter Skeleton

Status: In progress

Deliverables:

- [x] Home Assistant settings
- [x] Optional Home Assistant adapter registration
- [x] HomeAssistantAdapter
- [x] Home Assistant turn_on service call support
- [x] Home Assistant turn_off service call support
- [x] Home Assistant adapter tests
- [x] Runtime Home Assistant registration test


---




## v0.8.1 - Home Assistant Device Configuration

Status: In progress

Deliverables:

- [x] Home Assistant sample config
- [x] Home Assistant-backed device config support
- [x] Config loader test for Home Assistant devices
- [x] Runtime test for Home Assistant sample config
- [x] Home Assistant setup documentation

## v0.8.2 - Home Assistant Connection Check

Status: In progress

Deliverables:

- [x] Home Assistant connection check
- [x] Connection check tests
- [x] Manual connection check script
- [x] Home Assistant connection documentation

## v0.8.3 - Config Validation

Status: In progress

Deliverables:

- [x] HomeConfigValidationError
- [x] Duplicate room ID validation
- [x] Duplicate device ID validation
- [x] Required room field validation
- [x] Required device field validation
- [x] Unknown room reference validation
- [x] Home Assistant entity ID validation
- [x] Config validation tests