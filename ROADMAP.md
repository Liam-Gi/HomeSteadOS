

```markdown
# HomeSteadOS Roadmap

This file provides a high-level summary of the project roadmap.

For the detailed version plan, see:

```text
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

```markdown
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