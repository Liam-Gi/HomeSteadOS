# HomeSteadOS Version Roadmap

## 1. Purpose

This document defines the planned version roadmap for HomeSteadOS.

The roadmap exists to keep development focused, incremental, and measurable. HomeSteadOS is a long-term project, so each version should deliver a clear capability without trying to solve the entire system at once.

The roadmap may change as the project evolves, but major changes should be documented in `SPRINTS.md`, `CHANGELOG.md`, and relevant Architecture Decision Records.

---

## 2. Roadmap Philosophy

HomeSteadOS will be developed in small, deliberate versions.

The order of development is important:

```text
Documentation
  ↓
Core domain
  ↓
Registries
  ↓
Services
  ↓
Simulated devices
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

```

This prevents the project from becoming dependent on hardware or AI before the foundation is stable.

The guiding principle is:

Build the operating system before automating the house.

3. Version Summary
Version	Name	Focus
v0.1	Foundation	Project structure and foundation documents
v0.2	Core Domain	Home, floor, room, device, action, and capability models
v0.3	Registries	Device and room registries
v0.4	Services	Controlled operations through core services
v0.5	Simulation	Simulated device adapter and fake device control
v0.6	Events	Event bus and state change events
v0.7	API	HTTP API for external access
v0.8	Home Assistant	First real hardware integration
v0.9	AI Planner	Natural language to proposed actions
v1.0	Voice Prototype	Local voice interaction prototype
v0.1 - Foundation
Goal

Create the clean project foundation for HomeSteadOS.

Scope

This version focuses on structure and documentation, not functionality.

Deliverables
Clean Python src layout
Root documentation files
Product Requirements Document
System Architecture Document
Development Standards
Version Roadmap
Architecture Decision Record for core architecture
Initial pyproject.toml
Initial .gitignore
Placeholder modules for future development
Out of Scope
Device control
AI
Voice
Home Assistant
MQTT
Database
Web dashboard
Success Criteria

v0.1 is complete when another developer can open the repository and understand:

What HomeSteadOS is
Why it exists
How the system is intended to be structured
What the development standards are
What the next versions will build
v0.2 - Core Domain
Goal

Create the first real internal models used by HomeSteadOS.

Scope

This version defines how the system represents the home.

Deliverables
Home model
Floor model
Room model
Device model
Action model
Capability model
Shared enums
Basic unit tests for domain models
Key Questions
How should HomeSteadOS represent the physical structure of a house?
Should rooms store device IDs or full device objects?
How should device capabilities be represented?
What should a standard action request look like?
Out of Scope
Device registry
Device control
Adapter execution
AI
Real hardware
Success Criteria

v0.2 is complete when HomeSteadOS can represent a home structure in code and tests can confirm that homes, floors, rooms, devices, actions, and capabilities behave as expected.

v0.3 - Registries
Goal

Create central registries for known rooms and devices.

Scope

This version introduces lookup and management of known objects.

Deliverables
DeviceRegistry
RoomRegistry
Register device
Remove device
Find device by ID
Find device by name
Find devices by room
Find devices by type
Find devices by capability
Register room
Find room by ID
Unit tests for registry behaviour
Key Questions
Should registries store objects in memory only at first?
How should duplicate IDs be handled?
What errors or results should registry methods return?
How should searching by display name behave?
Out of Scope
Database persistence
Hardware discovery
Home Assistant sync
AI device discovery
Success Criteria

v0.3 is complete when devices and rooms can be registered, queried, and removed reliably through tested registry classes.

v0.4 - Services
Goal

Introduce controlled service operations.

Scope

This version moves behaviour into services rather than allowing interfaces to manipulate domain objects directly.

Deliverables
LightingService
RoomService
AutomationService
SystemService
ActionResult
Basic safety check integration placeholder
Unit tests for service behaviour
Example Service Operations
turn_on_light(device_id)
turn_off_light(device_id)
turn_off_room(room_id)
get_system_status()
Key Questions
What should a service return after an action?
Should services call adapters directly or go through an action executor?
What level of validation belongs in services versus the Safety Engine?
Out of Scope
Real hardware execution
AI planning
Voice
Persistent automation scheduling
Success Criteria

v0.4 is complete when actions can be requested through services and return consistent result objects.

v0.5 - Simulation
Goal

Control simulated devices through the HomeSteadOS service layer.

Scope

This version proves the architecture works without real hardware.

Deliverables
Base adapter interface
SimulatedDeviceAdapter
Simulated device state storage
Service-to-adapter execution path
CLI command support for simulated lights
Tests for simulated control
Example Flow
CLI command
  ↓
Command parser
  ↓
LightingService
  ↓
SafetyEngine
  ↓
SimulatedDeviceAdapter
  ↓
Simulated device state updated
Out of Scope
Home Assistant
MQTT
Real devices
AI
Success Criteria

v0.5 is complete when a user can control simulated devices through the CLI using the same service path that real devices will eventually use.

v0.6 - Events
Goal

Add event-driven communication inside HomeSteadOS.

Scope

This version introduces the Event Bus.

Deliverables
Event model
EventBus
Event type definitions
Device registered event
Device state changed event
Action requested event
Action completed event
Unit tests for event publishing and subscriptions
Key Questions
Should events be synchronous or asynchronous initially?
What metadata should every event include?
Should events be persisted later?
Out of Scope
MQTT events
Database event store
Complex automations
Success Criteria

v0.6 is complete when components can publish and subscribe to internal events without being tightly coupled.

v0.7 - API
Goal

Expose HomeSteadOS through an HTTP API.

Scope

This version creates the first external programmatic interface.

Deliverables
API application entry point
Device endpoints
Room endpoints
Action endpoints
System status endpoint
Request and response schemas
API tests
Possible Endpoints
GET /devices
GET /devices/{device_id}
GET /rooms
POST /actions
GET /system/status
Key Questions
Should the API use FastAPI or Flask?
How should action requests be validated?
How should API responses map to ActionResult?
Out of Scope
Authentication
Public remote access
Web dashboard
Mobile app
Success Criteria

v0.7 is complete when an external tool can list known devices and request actions through an HTTP API.

v0.8 - Home Assistant Integration
Goal

Control the first real device through Home Assistant.

Scope

This version introduces the first real hardware integration path.

Deliverables
Home Assistant adapter
Local configuration for Home Assistant URL
Token-based authentication
Device mapping between Home Assistant and HomeSteadOS
Control one smart plug or light
Documentation for Home Assistant setup
Key Questions
Should HomeSteadOS manually register Home Assistant devices or sync them automatically?
How should Home Assistant entity IDs map to HomeSteadOS device IDs?
How should unavailable Home Assistant entities be represented?
Out of Scope
Full Home Assistant replacement
Automatic discovery of every device type
Complex two-way sync
Voice control
Success Criteria

v0.8 is complete when HomeSteadOS can control at least one real device through Home Assistant while preserving the core service and safety flow.

v0.9 - AI Planner
Goal

Allow AI to convert user intent into proposed HomeSteadOS actions.

Scope

This version introduces basic AI reasoning without direct hardware control.

Deliverables
AI planner
Model client
Prompt templates
Tool/action schema
Natural language to structured action proposal
Safety review before execution
AI explanation for proposed actions
Tests for action proposal parsing where practical
Example

User says:

I'm going to bed.

AI proposes:

- Turn off living room lights
- Turn off kitchen lights
- Set bedroom lamp to dim

HomeSteadOS then reviews and executes approved actions.

Key Questions
Which local model should be used first?
What should the action schema look like?
How should uncertain AI outputs be handled?
When should the system ask for clarification?
Out of Scope
Fully autonomous decision-making
Long-term memory
Voice input
Security-critical actions without confirmation
Success Criteria

v0.9 is complete when a text request can be interpreted by AI into structured proposed actions that pass through HomeSteadOS safety and service layers.

v1.0 - Voice Prototype
Goal

Create the first local voice-controlled HomeSteadOS prototype.

Scope

This version connects speech input and output to the AI and service flow.

Deliverables
Speech-to-text experiment
Text-to-speech experiment
Voice interface
Basic wake word experiment
Voice command to AI planner
AI planner to action proposal
Safety confirmation path
Spoken response
Example Flow
User says:
"Turn on the office light."

Speech-to-text:
turn on the office light

AI or command parser:
proposes light.office.ceiling on

Safety Engine:
approves

LightingService:
executes

Text-to-speech:
"The office light is now on."
Out of Scope
Whole-home microphone system
Production-grade wake word detection
Multi-user voice identification
Fully offline polished assistant
Mobile app
Success Criteria

v1.0 is complete when a user can use voice to control at least one simulated or real device through the complete HomeSteadOS architecture.

4. Beyond v1.0

Possible future versions may include:

Persistent database storage
Web dashboard
Mobile app
Multi-user support
Role-based permissions
Advanced safety policies
Long-term AI memory
Routine learning
Energy monitoring
Security monitoring
Camera integration
Presence detection
Plugin system
Multi-home support
Local server deployment guide
Docker Compose deployment
Backup and restore tools
5. Versioning Notes

HomeSteadOS will use simple semantic-style versioning during early development.

Example:

v0.1
v0.2
v0.3
...
v1.0

Before v1.0, breaking changes are acceptable if they improve the architecture.

After v1.0, breaking changes should be documented more carefully.

6. Roadmap Maintenance

This roadmap should be updated when:

Version goals change
Major architectural decisions change
Features are moved between versions
New risks are discovered
Real hardware constraints affect the plan

Any major roadmap change should also be mentioned in:

SPRINTS.md
CHANGELOG.md
Relevant ADRs if architectural