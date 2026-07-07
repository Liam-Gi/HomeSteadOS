# HomeSteadOS Architecture

## 1. Architecture Overview

HomeSteadOS is designed as a local-first AI home operating system with a stable core, replaceable adapters, controlled interfaces, and a safety boundary between user intent, AI reasoning, and physical device execution.

The system is intentionally not built as a Home Assistant configuration project. Home Assistant may become an important integration layer, but it is not the central brain of the system.

HomeSteadOS owns:

- The home model
- The device registry
- System state
- Service orchestration
- Safety checks
- AI action review
- User-facing interfaces

External systems such as Home Assistant, MQTT, Zigbee, simulated devices, APIs, and future hardware platforms should connect through adapters.

## 2. High-Level System Flow

```text
User
  |
  | Voice / CLI / API
  v
Interfaces
  |
  | User request
  v
AI Planner or Command Parser
  |
  | Proposed action
  v
HomeSteadOS Core
  |
  | Validated action request
  v
Safety Engine
  |
  | Approved action
  v
Services
  |
  | Platform-independent command
  v
Adapters
  |
  | Platform-specific command
  v
Hardware / Simulated Devices / Home Assistant / MQTT
```
## Application Runtime

HomeSteadOS uses a runtime composition layer to wire together registries, adapters, services, and the event bus.

This prevents each interface from manually creating system components in a different way.

The runtime is responsible for constructing:

- DeviceRegistry
- RoomRegistry
- AdapterRegistry
- EventBus
- Core services
- Demo devices during development

Interfaces such as CLI, API, voice, and future AI components should use the runtime instead of manually constructing HomeSteadOS dependencies.


3. Core Design Principle

The core rule of the architecture is:

The HomeSteadOS core must not depend on any single smart home platform, device brand, AI model, or communication protocol.

This means:

Devices should be represented internally using HomeSteadOS domain models.
Device control should happen through services.
Hardware-specific logic should live in adapters.
AI should propose actions, not directly execute them.
Safety checks should happen before any physical action is taken.
4. Main Layers

HomeSteadOS is divided into the following major layers:

homesteados/
  core/
  adapters/
  interfaces/
  ai/
  config/

Each layer has a specific responsibility.

5. Core Layer

The core layer contains the central business logic of HomeSteadOS.

src/homesteados/core/
  domain/
  registry/
  services/
  events/
  safety/
  results/

The core layer should be as independent as possible. It should not know whether a device is simulated, controlled by Home Assistant, connected through MQTT, or eventually connected through another platform.

5.1 Domain
src/homesteados/core/domain/

The domain layer models the concepts HomeSteadOS understands.

Planned models include:

Home
Floor
Room
Device
Action
Capability
Shared enums

The domain layer represents the structure and state of the home.

Example:

Home
  |
  Floor
    |
    Room
      |
      Device

A device should have stable internal properties such as:

id
name
device_type
room_id
state
online
capabilities
attributes
adapter_id

The adapter_id tells the system which adapter is responsible for executing actions against the device.

5.2 Registry
src/homesteados/core/registry/

The registry layer stores and retrieves known objects.

Planned registries include:

DeviceRegistry
RoomRegistry

The DeviceRegistry should support queries such as:

Find device by ID
Find device by name
Find devices by room
Find devices by type
Find devices by capability
List all devices

The registry is the single source of truth for what devices HomeSteadOS knows about.

The `AdapterRegistry` stores available device adapters and allows services to resolve the correct adapter based on a device's `adapter_id`.

This allows the system to support multiple execution backends, such as simulated devices, Home Assistant, MQTT, and future integrations.

5.3 Services
src/homesteados/core/services/

Services provide controlled operations for the rest of the system.

Planned services include:

LightingService
RoomService
AutomationService
SystemService

Services should not contain hardware-specific code.

For example, the LightingService may expose:

turn_on_light(device_id)
turn_off_light(device_id)
set_brightness(device_id, brightness)

But it should not know whether the light is a Philips Hue bulb, a Zigbee switch, a simulated device, or a Home Assistant entity.

5.4 Events
src/homesteados/core/events/

The event system will allow HomeSteadOS components to communicate without being tightly coupled.

Example events:

Device registered
Device state changed
Motion detected
Room became occupied
Automation triggered
AI action proposed
Safety check failed

The Event Bus will become important once the system starts reacting to sensor data and automation triggers.

The first Event Bus implementation is synchronous and in-memory.

This is intentional for early development. It allows HomeSteadOS to publish and test events without introducing databases, queues, MQTT, or background workers too early.

Future versions may add persistent event storage or external event publishing.

5.5 Safety
src/homesteados/core/safety/

The Safety Engine reviews actions before they are executed.

Its responsibilities include:

Allowing safe actions
Blocking unsafe actions
Requiring confirmation for risky actions
Applying rules based on system mode
Preventing AI from bypassing system controls

Example rules:

Do not unlock doors from an ambiguous command.
Do not turn off cameras while the house is in Away mode.
Do not open the garage door without confirmation.
Do not execute AI-generated actions without validation.

The Safety Engine is a key boundary in the architecture.

5.6 Results
src/homesteados/core/results/

Result objects standardise how actions report success, failure, warnings, and required confirmations.

Example:

ActionResult
  success
  message
  action_id
  requires_confirmation
  reason

This will make it easier for CLI, API, voice, and AI interfaces to understand what happened.

6. Adapters Layer
src/homesteados/adapters/

Adapters translate HomeSteadOS actions into platform-specific commands.

Planned adapters include:

SimulatedDeviceAdapter
HomeAssistantAdapter
MqttAdapter

The adapter layer is where external system logic belongs.

6.1 Simulated Adapter

The simulated adapter allows HomeSteadOS to control fake devices during development.

This is important because it lets the core system be tested before any hardware is purchased.

6.2 Home Assistant Adapter

The Home Assistant adapter will eventually allow HomeSteadOS to control real devices through Home Assistant.

Home Assistant will act as a hardware integration platform, not as the HomeSteadOS brain.

6.3 MQTT Adapter

The MQTT adapter will support message-based communication for sensors, devices, and events.

MQTT will become useful for custom IoT devices, sensor data, and event-driven automation.

7. Interfaces Layer
src/homesteados/interfaces/

Interfaces allow users and external systems to communicate with HomeSteadOS.

Planned interfaces include:

CLI
HTTP API
Voice interface
7.1 CLI

The CLI is the first development interface.

It allows early testing without a web app, mobile app, or voice assistant.

Example command:

turn on office light
7.2 API

The API will eventually allow dashboards, mobile apps, external tools, or other systems to interact with HomeSteadOS.

Possible endpoints:

GET /devices
GET /rooms
POST /actions
GET /system/status
7.3 Voice

The voice interface will eventually connect:

Wake word detection
Speech-to-text
AI planner
Text-to-speech
Action confirmation

Voice should remain an interface. It should not bypass core services or safety checks.

8. AI Layer
src/homesteados/ai/

The AI layer will eventually interpret natural language, reason about user intent, and propose actions.

Planned components include:

planner.py
memory.py
tools.py
model_client.py
prompts.py

The AI layer should not directly control devices.

Instead, it should produce structured action proposals.

Example:

User request:
"I'm going to bed."

AI proposed actions:
- Turn off downstairs lights
- Lock external doors
- Set bedroom lamp to dim
- Check garage door status

Those actions must then pass through HomeSteadOS services and the Safety Engine.

9. AI Safety Boundary

The AI boundary is one of the most important architectural decisions.

AI Planner
  |
  | Proposed actions only
  v
Safety Engine
  |
  | Approved actions only
  v
Services
  |
  v
Adapters

The AI is allowed to:

Interpret requests
Suggest actions
Explain reasoning
Use context
Ask for clarification

The AI is not allowed to:

Directly execute hardware commands
Bypass safety checks
Unlock doors without confirmation
Disable security systems without authorisation
Hide its reasoning for important actions
10. Configuration Layer
src/homesteados/config/

The configuration layer will eventually manage:

Application settings
Logging configuration
Environment variables
Adapter credentials
Local server settings

Sensitive values should not be committed to Git.

Secrets should be stored in environment variables or local configuration files excluded by .gitignore.

11. Testing Strategy

Testing should begin early.

Initial tests should focus on:

Domain models
Registries
Services
Safety checks

Hardware integration tests should come later.

The goal is to make sure the core logic works even when there are no real devices connected.

12. Initial Project Structure
HomeSteadOS/
  docs/
    decisions/
    diagrams/
    research/
    hardware/
    product/
    standards/

  src/
    homesteados/
      core/
        domain/
        registry/
        services/
        events/
        safety/
        results/

      adapters/
        simulated/
        home_assistant/
        mqtt/

      interfaces/
        cli/
        api/
        voice/

      ai/
      config/

  tests/
  scripts/
13. Architectural Rules

The following rules should guide future development:

Core logic must not depend directly on hardware platforms.
AI must not directly control devices.
Services should expose controlled use cases.
Adapters should contain platform-specific implementation details.
Safety checks must happen before physical actions.
Interfaces should not bypass services.
Domain models should remain simple and understandable.
Tests should be added for core behaviour before hardware integration.
Documentation should be updated when major architecture decisions change.
The system should still make sense if it eventually controls hundreds of devices.
14. Future Architecture Direction

As HomeSteadOS matures, the architecture may expand to include:

Persistent database storage
User accounts
Role-based permissions
Web dashboard
Mobile app
Local AI model hosting
Vector memory
Automation builder
Plugin system
Advanced event processing
Energy monitoring
Security monitoring
Multi-home support

These should be added gradually and only when the core architecture is stable.

### Core Ports


src/homesteados/core/ports/

Ports define interfaces that external adapters must implement.

Core services should depend on ports rather than concrete adapter implementations. This keeps the core independent from Home Assistant, MQTT, simulated devices, and future hardware platforms.

### HTTP API

The HTTP API exposes HomeSteadOS through standard web endpoints.

The API uses the central HomeSteadOS runtime, which prevents it from manually wiring registries, services, adapters, and events differently from the CLI.

Initial endpoints include:

- `GET /system/status`
- `GET /devices`
- `GET /devices/{device_id}`
- `GET /events`
- `POST /actions`

### RoomService

The RoomService provides room-level operations.

It allows HomeSteadOS to query devices in a room and perform room-level actions such as turning all lights in a room on or off.

This is an important step toward intent-based commands such as "I'm leaving" or "turn off the office".

### System Modes

HomeSteadOS includes a high-level system mode concept.

Initial modes include:

- Home
- Away
- Night
- Guest
- Vacation

System modes provide household context that future safety rules, AI planning, and automation logic can use.

The Safety Engine now supports mode-aware safety review.

It can evaluate:

- Explicit confirmation requirements
- Action risk level
- Current system mode
- Request source

Initial rules include:

- Low-risk actions are allowed by default.
- High-risk actions require confirmation.
- Critical-risk actions are blocked by default.
- AI-requested actions require confirmation while the system is in Away or Vacation mode.

### ActionDispatcher

The ActionDispatcher is the central routing layer for structured actions.

It allows interfaces, APIs, future AI components, and automation systems to submit actions without needing to know which service should handle them.

The dispatcher currently supports:

- Device actions
- Room actions
- System actions

This prepares HomeSteadOS for AI-generated actions because the AI can produce a structured Action and allow the core system to route it safely.

## Configuration Loading

HomeSteadOS can load room and device definitions from JSON configuration files.

The demo runtime currently loads from:

```text
configs/demo_home.json
```
## Settings and Logging

HomeSteadOS includes a central settings layer.

Settings are loaded from environment variables and currently support:

- Environment name
- Log level
- Demo home config path

The CLI and API both use the settings layer so runtime configuration is consistent across interfaces.

Logging is configured through a central logging configuration module. This prepares HomeSteadOS for better debugging, diagnostics, future file logs, and production deployment.

## Diagnostics and Health

HomeSteadOS includes a diagnostics service that reports system health.

The diagnostics service currently checks:

- Registered adapters
- Registered rooms
- Registered devices
- Offline devices
- Devices referencing missing adapters
- Event bus availability

Diagnostics are available through both the CLI and HTTP API.

## Home Assistant Integration

HomeSteadOS includes an initial Home Assistant adapter skeleton.

The Home Assistant adapter allows HomeSteadOS actions to be translated into Home Assistant service calls.

Home Assistant is treated as an adapter, not as the HomeSteadOS core.

The adapter currently supports:

- `turn_on`
- `turn_off`

Devices using the Home Assistant adapter must include a Home Assistant entity ID in their attributes:

```text
home_assistant_entity_id


Home Assistant-backed devices are configured through home configuration files.

A Home Assistant device uses:

```text
adapter_id = "home_assistant"
```

HomeSteadOS validates home configuration files before registering rooms and devices.

Validation currently checks:

- `rooms` is a list
- `devices` is a list
- required room fields are present
- required device fields are present
- room IDs are unique
- device IDs are unique
- devices reference known rooms
- Home Assistant devices include `attributes.home_assistant_entity_id`

Invalid configuration raises `HomeConfigValidationError` with a clear message.

## Audit Logging

HomeSteadOS includes an in-memory audit logging service.

The audit log subscribes to the EventBus and records readable entries for important system events.

The audit log currently records:

- Action requested
- Action completed
- Action failed
- Action blocked
- Device state changed
- System mode changed

Audit entries are available through both the CLI and HTTP API.

This prepares HomeSteadOS for future persistent audit trails, AI explainability, debugging, and real hardware accountability.

The ActionDispatcher preserves structured Action metadata when routing actions to services.

This ensures safety-relevant fields such as `requested_by`, `risk_level`, `requires_confirmation`, `target_type`, and `parameters` are not lost during execution.

This is especially important for future AI-generated actions, where the Safety Engine must review the original action that was proposed.


## Confirmation Workflow

HomeSteadOS includes an in-memory confirmation workflow for actions that require approval.

When the Safety Engine determines that an action requires confirmation, the original Action is stored in the PendingActionStore.

The ConfirmationService can then:

- List pending actions
- Confirm a pending action
- Cancel a pending action

Confirmed actions are executed through the ActionDispatcher so the normal service, safety, adapter, event, and audit paths are preserved.

## Automation Engine

HomeSteadOS includes an event-driven automation engine.

Automation rules listen for events on the EventBus. When a rule matches an event, the AutomationService creates a fresh Action and executes it through the ActionDispatcher.

This means automations use the same execution path as CLI, API, and future AI requests:

```text
EventBus
  ↓
AutomationService
  ↓
ActionDispatcher
  ↓
Service
  ↓
SafetyEngine
  ↓
Adapter
  ↓
Device
```

## Config-Driven Automations

HomeSteadOS can load automation rules from JSON configuration files.

Automation rules are parsed into AutomationRule domain objects and registered with the AutomationRuleRegistry.

This keeps runtime wiring clean and allows future versions of HomeSteadOS to support user-created automations, persistent automation storage, and configuration-based home behaviour.

## Scenes

HomeSteadOS supports saved scenes.

A scene is a named group of actions that can be executed together. Scenes are loaded from JSON configuration and registered with the SceneRegistry.

Scenes are executed by SceneService. SceneService does not control devices directly. Instead, it creates fresh Action objects and sends them through the ActionDispatcher.

This means scenes use the same safety, service, adapter, event, and audit paths as CLI, API, automation, and future AI-generated actions.

## Scene Actions

Scenes can be executed as structured Actions.

The ActionDispatcher supports scene-targeted actions using:

- `action_type = run_scene`
- `target_type = scene`
- `target_id = <scene_id>`

This allows CLI, API, automation rules, and future AI planners to run scenes through the same central execution path.

SceneService still executes the individual scene actions through ActionDispatcher, preserving safety review, adapter routing, events, and audit logging.

## Text Command Service

HomeSteadOS includes a TextCommandService that converts simple text commands into structured Actions.

The service does not control devices directly. It parses user text, creates an Action, and sends that Action through the ActionDispatcher.

This prepares HomeSteadOS for future AI and voice interfaces while preserving the existing safety, confirmation, event, audit, service, and adapter paths.

## Command Preview and Action Explanation

HomeSteadOS can preview text commands before executing them.

TextCommandService parses a command into a structured Action. ActionDescriptionService then converts that Action into a human-readable explanation.

Previewing does not execute the action. This gives future AI and voice interfaces a safe way to explain proposed actions before they are run.

## Command History

HomeSteadOS records text command previews and executions in memory.

Command history captures the original command text, requester, preview/execution mode, parsed action details, result status, and timestamp.

This supports debugging, auditability, and future AI or voice explainability.


## Command Suggestions

HomeSteadOS includes a command suggestion service.

When a text command cannot be parsed, CommandSuggestionService suggests valid commands based on configured rooms, scenes, and system modes.

This improves CLI and API usability and prepares HomeSteadOS for future voice and AI interfaces.


## Behaviour Insights

HomeSteadOS can generate simple behaviour insights from command history.

The BehaviourInsightService analyses in-memory command history and identifies repeated successful command executions.

This is deterministic logic, not AI. It prepares the project for future AI-assisted suggestions while keeping behaviour explainable and testable.


## Command Shortcuts

HomeSteadOS supports named command shortcuts.

Shortcuts are loaded from JSON configuration and registered with the ShortcutRegistry. A shortcut stores a text command such as `run good night` or `turn on office light`.

ShortcutService executes shortcuts through TextCommandService, so shortcut commands still pass through the normal text parsing, action dispatching, safety, service, adapter, event, and audit paths.