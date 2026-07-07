# Sprint 0
### Progress


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

---

## Sprint 12 - Mode-Aware Safety

### Goal

Improve the Safety Engine so it can consider system mode, action risk, and requester source before allowing an action.

### Planned Work

- Add ActionRisk enum
- Add risk level to Action model
- Update SafetyEngine to use SystemState
- Add high-risk and critical-risk safety rules
- Add AI-request safety rules for Away and Vacation modes
- Wire SafetyEngine into the runtime
- Add safety policy tests

### Out of Scope

- Full permission system
- User authentication
- Confirmation workflow
- Real locks, cameras, alarms, or garage doors
- AI planner implementation

### Progress

- Added ActionRisk enum
- Added risk level to Action model
- Updated SafetyEngine to use SystemState
- Added high-risk confirmation rule
- Added critical-risk block rule
- Added AI confirmation rule for Away and Vacation modes
- Wired SafetyEngine into runtime
- Added safety policy tests

---

## Sprint 13 - Action Dispatcher

### Goal

Create a central dispatcher for structured HomeSteadOS actions.

The Action Dispatcher allows CLI, API, future AI, and automation systems to submit actions through one controlled execution path.

### Planned Work

- Create ActionDispatcher
- Route device light actions through LightingService
- Route room light actions through RoomService
- Update runtime wiring
- Update API to use ActionDispatcher
- Add action dispatcher tests
- Update API action tests

### Out of Scope

- AI planner
- Voice control
- Real hardware
- Confirmation workflow
- Scheduling

### Progress

- Added ActionTargetType enum
- Added target type support to Action
- Created ActionDispatcher
- Added routing for device actions
- Added routing for room actions
- Added routing for system actions
- Wired ActionDispatcher into runtime
- Refactored API action endpoint to use ActionDispatcher
- Added action dispatcher tests

---

## Sprint 14 - Config-Driven Runtime

### Goal

Move demo rooms and devices out of Python code and into a JSON configuration file.

This makes HomeSteadOS easier to configure, test, and eventually adapt to real homes.

### Planned Work

- Add demo home JSON config
- Create home config loader
- Register rooms and devices from config
- Link devices to rooms during config load
- Refactor demo runtime to use config file
- Add config loader tests
- Update runtime tests

### Out of Scope

- Database persistence
- User-created config UI
- Home Assistant sync
- MQTT discovery
- Real hardware

### Progress

- Added demo home JSON config
- Created home config loader
- Added config-based room registration
- Added config-based device registration
- Linked devices to rooms during config registration
- Refactored demo runtime to load config file
- Added config loader tests

---

## Sprint 15 - Settings and Logging

### Goal

Create a central application settings and logging system.

This prepares HomeSteadOS for configurable runtime behaviour, custom config paths, future Home Assistant credentials, API tokens, and better debugging.

### Planned Work

- Create AppSettings model
- Load settings from environment variables
- Add logging configuration
- Update CLI to use settings and logging
- Update API app factory to use settings and logging
- Add settings tests
- Add logging tests

### Out of Scope

- `.env` file loading
- Secret management
- Home Assistant integration
- Authentication
- Database configuration

### Progress

- Created AppSettings model
- Added environment variable based settings loading
- Added configurable demo config path
- Added logging configuration
- Updated CLI to use settings and logging
- Updated API app factory to use settings and logging
- Added settings tests
- Added logging tests

---

## Sprint 16 - Diagnostics and Health

### Goal

Add system diagnostics and health reporting to HomeSteadOS.

Diagnostics allow the system to report whether core components are configured correctly and whether devices, rooms, adapters, and events are in a healthy state.

### Planned Work

- Add HealthStatus enum
- Add system health result models
- Create DiagnosticsService
- Wire DiagnosticsService into runtime
- Add CLI health command
- Add API health endpoint
- Add diagnostics tests

### Out of Scope

- Hardware health checks
- Home Assistant status checks
- MQTT connection status
- Database health checks
- Production monitoring

### Progress

- Added HealthStatus enum
- Created health result models
- Created DiagnosticsService
- Wired DiagnosticsService into runtime
- Added CLI health command
- Added API health endpoint
- Added diagnostics tests

---

## Sprint 17 - Home Assistant Adapter Skeleton

### Goal

Create the first Home Assistant adapter structure.

This sprint prepares HomeSteadOS for real hardware integration without requiring a running Home Assistant instance yet.

### Planned Work

- Add Home Assistant settings
- Create HomeAssistantAdapter
- Support Home Assistant service calls for turn_on and turn_off
- Add adapter tests using a fake HTTP client
- Add optional Home Assistant adapter registration in runtime
- Update diagnostics to detect registered adapters
- Update documentation

### Out of Scope

- Real Home Assistant server setup
- Real device control
- Device discovery
- Authentication UI
- MQTT
- Voice
- AI

### Progress

- Added Home Assistant settings
- Created HomeAssistantAdapter
- Added Home Assistant service call support for turn_on and turn_off
- Added optional Home Assistant adapter registration in runtime
- Added Home Assistant adapter tests
- Added runtime Home Assistant adapter registration test

---

## Sprint 18 - Home Assistant Device Configuration

### Goal

Allow HomeSteadOS device configuration files to define Home Assistant-backed devices.

This prepares the system for real device control through Home Assistant while keeping simulated devices available for development.

### Planned Work

- Add sample Home Assistant config file
- Add Home Assistant device config fields
- Add tests for loading Home Assistant-backed devices
- Add diagnostics test for missing Home Assistant adapter
- Add documentation for Home Assistant device configuration

### Out of Scope

- Real Home Assistant connection testing
- Automatic device discovery
- Entity state sync
- Real hardware control
- Authentication UI

### Progress

- Added Home Assistant sample config
- Added tests for Home Assistant-backed device config loading
- Added runtime test for Home Assistant sample config
- Added Home Assistant setup documentation

---

## Sprint 19 - Home Assistant Connection Check

### Goal

Add a safe Home Assistant connection check before attempting real hardware control.

This allows HomeSteadOS to verify that the Home Assistant URL and access token are valid.

### Planned Work

- Add connection check to HomeAssistantAdapter
- Add tests for successful and failed connection checks
- Add documentation for manually testing Home Assistant connectivity
- Prepare for first real smart plug or light test

### Out of Scope

- Real device control
- Device discovery
- State synchronisation
- MQTT
- AI
- Voice

### Progress

- Added Home Assistant connection check
- Added tests for successful and failed connection checks
- Added manual Home Assistant connection script
- Updated Home Assistant setup documentation

---

## Sprint 20 - Config Validation

### Goal

Improve validation for HomeSteadOS home configuration files.

This sprint makes configuration errors clearer before real hardware integrations are added.

### Planned Work

- Add HomeConfigValidationError
- Validate duplicate room IDs
- Validate duplicate device IDs
- Validate required room fields
- Validate required device fields
- Validate devices reference known rooms
- Validate Home Assistant devices include entity IDs
- Add config validation tests

### Out of Scope

- Full JSON schema validation
- Config editor UI
- Home Assistant discovery
- Real hardware control

### Progress

- Added HomeConfigValidationError
- Added room config validation
- Added device config validation
- Added duplicate ID validation
- Added unknown room reference validation
- Added Home Assistant entity ID validation
- Added config validation tests

---

## Sprint 21 - Audit Logging

### Goal

Create an audit logging layer for HomeSteadOS.

The audit log records important system events so users and developers can inspect what happened, when it happened, and which component caused it.

### Planned Work

- Create AuditLogEntry model
- Create AuditLogService
- Subscribe AuditLogService to EventBus
- Wire audit logging into runtime
- Add CLI audit command
- Add API audit endpoint
- Add audit log tests

### Out of Scope

- Database persistence
- File-based audit logs
- User authentication
- Security-grade audit trails
- Log retention policies

### Progress

- Created AuditLogEntry model
- Created AuditLogService
- Subscribed audit logging to EventBus
- Wired audit logging into runtime
- Added CLI audit command
- Added API audit endpoint
- Added audit log tests

---

## Sprint 22 - Preserve Action Metadata

### Goal

Ensure structured Action metadata is preserved through the execution path.

This sprint prevents ActionDispatcher from losing important safety metadata such as risk level, confirmation requirements, and requester source when routing actions to services.

### Planned Work

- Add LightingService.execute_action()
- Refactor LightingService to review the original Action
- Update ActionDispatcher to pass device actions directly to LightingService
- Add tests for high-risk device actions through ActionDispatcher
- Add tests for API risk handling
- Update architecture documentation

### Out of Scope

- Confirmation workflow
- AI planner
- Voice control
- Real hardware

### Progress

- Added LightingService.execute_action()
- Refactored LightingService to preserve original Action metadata
- Updated ActionDispatcher to pass original device actions to LightingService
- Added tests for high-risk device actions
- Added tests for confirmation-required device actions
- Added tests for AI-requested actions in Away mode

---

## Sprint 23 - Pending Action Confirmation

### Goal

Create the first confirmation workflow for actions that require user approval.

When the Safety Engine requires confirmation, HomeSteadOS should store the original Action as pending so it can be confirmed and executed later.

### Planned Work

- Create PendingActionStore
- Create ConfirmationService
- Store confirmation-required actions
- Confirm pending actions
- Cancel pending actions
- Add CLI pending/confirm/cancel commands
- Add API pending/confirm/cancel endpoints
- Add tests for confirmation workflow

### Out of Scope

- Authentication
- Role-based permissions
- Expiring pending actions
- Persistent pending action storage
- Voice confirmation

### Progress

- Created PendingActionStore
- Created ConfirmationService
- Stored confirmation-required actions
- Added pending action confirmation
- Added pending action cancellation
- Added CLI pending/confirm/cancel commands
- Added API pending/confirm/cancel endpoints
- Added confirmation workflow tests

---

## Sprint 24 - GitHub CI and Repo Hygiene

### Goal

Add GitHub Actions so the HomeSteadOS test suite runs automatically on every push and pull request.

This improves reliability and makes the repository look more professional as a portfolio project.

### Planned Work

- Add GitHub Actions test workflow
- Run tests on Python 3.12
- Install project in editable mode with dev dependencies
- Run pytest automatically
- Add CI badge to README
- Add development setup instructions to README
- Update roadmap and changelog

### Out of Scope

- Deployment
- Docker build pipeline
- Linting
- Formatting enforcement
- Release automation

### Progress

- Added GitHub Actions test workflow
- Configured Python 3.12 test environment
- Configured editable install with development dependencies
- Configured automatic pytest run
- Added README CI badge
- Added README development setup instructions

---

## Sprint 25 - Automation Rules Engine

### Goal

Create the first event-driven automation system for HomeSteadOS.

Automation rules should listen to system events and execute structured Actions through the existing ActionDispatcher.

### Planned Work

- Create AutomationRule domain model
- Create AutomationRuleRegistry
- Create AutomationService
- Subscribe automation service to EventBus
- Add demo automation rule for Night mode
- Add CLI automation commands
- Add API automation endpoints
- Add automation tests

### Out of Scope

- Persistent automation storage
- Config-driven automation loading
- User-created automation rules through the API
- Time-based scheduling
- Complex condition logic

### Progress

- Created AutomationRule domain model
- Created AutomationRuleRegistry
- Created AutomationService
- Subscribed AutomationService to EventBus
- Added demo Night mode automation
- Added CLI automation listing and enable/disable commands
- Added API automation listing and enable/disable endpoints
- Added automation tests

---

## Sprint 26 - Config-Driven Automation Rules

### Goal

Move demo automation rules out of runtime code and into a JSON configuration file.

This allows HomeSteadOS to load automation rules in the same way it already loads rooms and devices.

### Planned Work

- Create demo automation config file
- Create automation config loader
- Validate automation config structure
- Parse automation rules into AutomationRule objects
- Load automation rules during demo runtime creation
- Remove hardcoded demo automation rule creation from runtime
- Add config loader tests
- Update documentation

### Out of Scope

- API-created automation rules
- Saving automation rules back to config files
- Database persistence
- Advanced condition logic
- Time-based schedules

### Progress

- Created demo automation config file
- Created automation config loader
- Added automation config validation
- Added automation rule parsing
- Updated demo runtime to load automation config
- Removed hardcoded demo automation rule registration
- Added automation config loader tests

---

## Sprint 27 - Scenes

### Goal

Add support for saved scenes that execute groups of actions through the existing ActionDispatcher.

Scenes allow HomeSteadOS to perform common home routines such as Good Night, Movie Time, or Leaving Home.

### Planned Work

- Create Scene domain model
- Create SceneRegistry
- Create SceneService
- Create demo scene config
- Load scenes from JSON config
- Add CLI scene commands
- Add API scene endpoints
- Add scene tests

### Out of Scope

- User-created scenes through the API
- Saving scenes back to config files
- Scene scheduling
- Scene conditions
- Advanced rollback if one action fails

### Progress

- Created Scene domain model
- Created SceneRegistry
- Created SceneService
- Created demo scene config
- Created scene config loader
- Loaded scenes during demo runtime startup
- Added CLI scene commands
- Added API scene endpoints
- Added scene tests

---

## Sprint 28 - Run Scenes Through ActionDispatcher

### Goal

Allow scenes to be executed as normal structured Actions through the ActionDispatcher.

This lets CLI, API, automation rules, and future AI planners trigger scenes through the same central execution path.

### Planned Work

- Add RUN_SCENE action type
- Add SCENE action target type
- Update ActionDispatcher to route scene actions
- Wire SceneService into ActionDispatcher
- Update automation config to run the Good Night scene
- Add ActionDispatcher scene tests
- Add API scene action tests
- Update documentation

### Out of Scope

- Nested scene loop detection beyond basic protection
- User-created scenes through API
- Scene rollback
- Scene scheduling

### Progress

- Added RUN_SCENE action type
- Added SCENE action target type
- Updated ActionDispatcher to route scene actions
- Wired SceneService back into ActionDispatcher
- Updated Night mode automation to run the Good Night scene
- Added tests for scene actions through ActionDispatcher
- Added tests for scene actions through the API

---

## Sprint 29 - Text Command Service

### Goal

Create a text command service that converts simple natural-language commands into structured Actions.

This prepares HomeSteadOS for future AI planning and voice control by ensuring text input still passes through the normal ActionDispatcher and SafetyEngine path.

### Planned Work

- Create TextCommandParseResult
- Create TextCommandService
- Parse light commands
- Parse room light commands
- Parse system mode commands
- Parse scene commands
- Execute parsed commands through ActionDispatcher
- Add API text command endpoint
- Update CLI to use TextCommandService for action commands
- Add tests

### Out of Scope

- LLM integration
- Voice input
- Complex natural language
- Multi-step planning
- Conversation memory

### Progress

- Created TextCommandParseResult
- Created TextCommandService
- Added text parsing for light commands
- Added text parsing for room commands
- Added text parsing for system mode commands
- Added text parsing for scene commands
- Routed parsed text commands through ActionDispatcher
- Added API text command endpoint
- Updated CLI action commands to use TextCommandService
- Added text command tests

---

## Sprint 30 - Command Preview and Action Explanation

### Goal

Allow HomeSteadOS to preview text commands before executing them.

This improves safety, explainability, and prepares the project for future AI and voice interfaces.

### Planned Work

- Create ActionDescriptionService
- Describe device actions
- Describe room actions
- Describe system mode actions
- Describe scene actions
- Add CLI preview command
- Add API text command preview endpoint
- Add tests

### Out of Scope

- LLM explanations
- Multi-action AI planning
- Confirmation UI
- Persistent command history

### Progress

- Created ActionDescriptionService
- Added descriptions for device, room, system, and scene actions
- Added CLI preview command
- Added API text command preview endpoint
- Added tests for previews and descriptions

---

## Sprint 31 - Command History

### Goal

Record text command previews and executions in memory.

Command history improves debugging, explainability, and prepares HomeSteadOS for future AI and voice interfaces.

### Planned Work

- Create CommandHistoryEntry model
- Create CommandHistoryService
- Record text command executions
- Record text command previews
- Add CLI command history command
- Add API command history endpoint
- Add tests

### Out of Scope

- Persistent storage
- User accounts
- Search and filtering
- Exporting command history

### Progress

- Created CommandHistoryEntry model
- Created CommandHistoryService
- Recorded command previews
- Recorded command executions
- Added CLI history command
- Added API command history endpoint
- Added command history tests

---

## Sprint 32 - Command Suggestions

### Goal

Suggest valid text commands when user input cannot be parsed.

Command suggestions improve usability and prepare HomeSteadOS for better CLI, API, and future voice experiences.

### Planned Work

- Create CommandSuggestionService
- Suggest room light commands
- Suggest scene commands
- Suggest system mode commands
- Add suggestions to text command parse failures
- Add API suggestions response
- Add CLI suggestions output
- Add tests

### Out of Scope

- LLM-based suggestions
- Fuzzy matching libraries
- Autocomplete UI
- Personalised suggestions

### Progress

- Created CommandSuggestionService
- Added room light command suggestions
- Added scene command suggestions
- Added system mode suggestions
- Added suggestions to failed text parsing
- Added CLI suggestion output
- Added API suggestion responses
- Added command suggestion tests

---

## Sprint 33 - Behaviour Insights

### Goal

Generate simple behaviour insights from command history.

Behaviour insights help HomeSteadOS identify repeated commands that may be good candidates for scenes, automations, or shortcuts.

### Planned Work

- Create BehaviourInsight model
- Create BehaviourInsightService
- Detect repeated command executions
- Suggest scene or automation candidates
- Add CLI insights command
- Add API insights endpoint
- Add tests

### Out of Scope

- LLM-generated insights
- Automatic automation creation
- Persistent insight storage
- User-specific profiling
- Machine learning

### Progress

- Created BehaviourInsight model
- Created BehaviourInsightService
- Added repeated command detection
- Added CLI insights command
- Added API insights endpoint
- Added behaviour insight tests

---

## Sprint 34 - Command Shortcuts

### Goal

Add support for named command shortcuts.

Shortcuts allow common text commands to be saved and executed by name, preparing HomeSteadOS for user-defined routines and future AI-assisted workflow creation.

### Planned Work

- Create Shortcut domain model
- Create ShortcutRegistry
- Create ShortcutService
- Create demo shortcut config
- Create shortcut config loader
- Load shortcuts during demo runtime startup
- Add CLI shortcut commands
- Add API shortcut endpoints
- Add tests

### Out of Scope

- Creating shortcuts through the API
- Saving shortcuts back to config files
- User-specific shortcuts
- Shortcut scheduling

### Progress

- Created Shortcut domain model
- Created ShortcutRegistry
- Created ShortcutService
- Created demo shortcut config
- Created shortcut config loader
- Loaded shortcuts during demo runtime startup
- Added CLI shortcut commands
- Added API shortcut endpoints
- Added shortcut tests