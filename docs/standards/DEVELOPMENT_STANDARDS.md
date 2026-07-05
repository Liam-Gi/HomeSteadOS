# HomeSteadOS Development Standards

## 1. Purpose

This document defines the development standards for HomeSteadOS.

The goal is to keep the project clean, understandable, maintainable, and scalable as it grows from an early prototype into a complete local-first AI home operating system.

These standards apply to:

- Code structure
- Naming
- Documentation
- Testing
- Architecture
- Git commits
- Future integrations
- AI safety boundaries

## 2. Core Development Philosophy

HomeSteadOS should be built like a professional software product, not a collection of scripts.

Every feature should be:

- Purposeful
- Documented
- Testable
- Modular
- Safe
- Easy to understand
- Able to scale as the system grows

The project should still make sense if it eventually controls hundreds of devices across multiple rooms, floors, adapters, and interfaces.

## 3. Architectural Principles

### 3.1 Core First

The core domain should be designed before hardware integrations.

The system should understand homes, rooms, devices, actions, events, and safety rules before it controls real hardware.

### 3.2 Adapters at the Edge

Hardware-specific logic belongs in adapters.

The core should not directly depend on:

- Home Assistant
- MQTT
- Zigbee
- Wi-Fi devices
- Specific brands
- Specific AI providers

### 3.3 AI Does Not Directly Execute Actions

The AI layer may propose actions, but it must not directly control hardware.

Correct flow:

```text
AI proposes action
  ↓
Core validates request
  ↓
Safety Engine reviews action
  ↓
Service executes approved action
  ↓
Adapter talks to external system

```
3.4 Safety Before Convenience

Risky or ambiguous actions must be blocked or require confirmation.

Examples:

Unlocking doors
Opening garage doors
Disabling cameras
Turning off alarms
Running high-power devices
Executing unclear AI-generated commands
3.5 Interfaces Must Not Bypass Services

CLI, API, voice, and future dashboard interfaces must call core services.

They should not directly modify device state or call adapters.

4. Project Structure

HomeSteadOS uses a Python src layout.

HomeSteadOS/
  docs/
  src/
    homesteados/
      core/
      adapters/
      interfaces/
      ai/
      config/
  tests/
  scripts/
4.1 core

Contains the main HomeSteadOS logic.

core/
  domain/
  registry/
  services/
  events/
  safety/
  results/
4.2 adapters

Contains external integrations.

Examples:

Simulated devices
Home Assistant
MQTT
4.3 interfaces

Contains ways users or systems interact with HomeSteadOS.

Examples:

CLI
API
Voice
4.4 ai

Contains AI planning, prompts, model clients, memory, and tools.

4.5 config

Contains settings and logging configuration.

4.6 tests

Contains automated tests.

4.7 scripts

Contains developer scripts, setup scripts, and maintenance utilities.

5. Naming Standards
5.1 Python Files

Use lowercase with underscores.

Good:

device_registry.py
lighting_service.py
safety_engine.py

Bad:

DeviceRegistry.py
lightingService.py
safetyengine.py
5.2 Classes

Use PascalCase.

Good:

DeviceRegistry
LightingService
SafetyEngine
ActionResult
5.3 Functions and Methods

Use lowercase with underscores.

Good:

register_device()
find_device_by_id()
turn_on_light()
requires_confirmation()
5.4 Variables

Use clear names.

Good:

device_id
room_id
action_request
safety_result

Bad:

x
data
thing
obj
5.5 Constants

Use uppercase with underscores.

DEFAULT_ADAPTER_ID = "simulated"
MAX_ACTION_RETRIES = 3
6. Device ID Standards

Device IDs should be stable, predictable, and human-readable.

Recommended format:

device_type.room.device_name

Examples:

light.office.ceiling
light.kitchen.bench
sensor.hallway.motion
switch.bedroom.fan
camera.driveway.main
lock.front_door.primary

Device IDs should not change just because the display name changes.

Good:

id: light.office.ceiling
name: Office Ceiling Light

Bad:

id: Office Ceiling Light
7. Room ID Standards

Room IDs should be lowercase with underscores.

Examples:

office
kitchen
main_bedroom
living_room
garage
front_yard

Display names can use normal formatting.

Example:

id: main_bedroom
name: Main Bedroom
8. Code Style
8.1 Type Hints

Use type hints for function arguments and return values.

Good:

def find_device_by_id(device_id: str) -> Device | None:
    ...
8.2 Keep Functions Small

Functions should do one clear thing.

If a function becomes difficult to explain in one sentence, it may need to be split.

8.3 Avoid Hidden Side Effects

Functions should not unexpectedly modify unrelated state.

Example:

A function called:

find_device_by_id()

should not also register a new device.

8.4 Prefer Explicit Code

Readable code is more valuable than clever code.

Good:

if device is None:
    return ActionResult.failure("Device not found")

Bad:

return device and action(device) or fail()
9. Comments

Comments should explain why something exists, not repeat what the code already says.

Bad:

# Turn on the light
light.turn_on()

Good:

# Lights should not be controlled directly from interfaces.
# All actions must pass through the lighting service so safety checks can be applied.
lighting_service.turn_on_light(device_id)
10. Documentation Standards

Documentation should be updated when major decisions or architecture changes occur.

Important documents:

README.md
VISION.md
ROADMAP.md
ARCHITECTURE.md
SPRINTS.md
CHANGELOG.md
docs/product/PRD.md
docs/product/VERSION_ROADMAP.md
docs/standards/DEVELOPMENT_STANDARDS.md
docs/decisions/
11. Architecture Decision Records

Architecture Decision Records are stored in:

docs/decisions/

Use ADRs for major decisions such as:

Choosing the src layout
Separating core from adapters
Preventing AI from directly controlling hardware
Choosing Home Assistant as the first hardware integration
Choosing MQTT topic structure
Choosing database technology

ADR format:

# ADR-000X: Title

## Status

Proposed / Accepted / Rejected / Superseded

## Context

What problem are we solving?

## Decision

What did we decide?

## Consequences

What are the trade-offs?
12. Testing Standards

Tests should be added for core logic before hardware integrations.

Initial test focus:

Domain models
Device registry
Room registry
Services
Safety engine
Action results

Tests should not require real hardware.

12.1 Test Naming

Test files should use:

test_feature_name.py

Example:

test_device_registry.py

Test functions should describe expected behaviour.

Example:

def test_register_device_adds_device_to_registry():
    ...
12.2 Testing Goal

The goal is not to test every line immediately.

The goal is to protect important behaviour as the system grows.

13. Git Standards
13.1 Commit Often

Commits should be small and meaningful.

Good:

Add device domain model
Create device registry tests
Document AI safety boundary

Bad:

stuff
changes
update
fixed things
13.2 Commit Message Style

Use short, clear commit messages.

Recommended format:

Verb + what changed

Examples:

Add core architecture document
Create initial project structure
Implement device registry
Add safety engine placeholder
13.3 Do Not Commit Secrets

Never commit:

API keys
Tokens
Passwords
Local .env files
Home Assistant access tokens
Private network details
14. Changelog Standards

Update CHANGELOG.md for meaningful project changes.

Use sections:

## v0.x - Release Name

### Added

### Changed

### Fixed

### Removed

### Notes
15. Sprint Documentation Standards

Update SPRINTS.md at the end of each sprint.

Each sprint should include:

Goal
Planned work
Completed work
Problems encountered
Lessons learned
Next sprint

Example:

## Sprint 1 - Core Architecture

### Goal

Define the core architecture and development standards.

### Completed

- Product Requirements Document
- Architecture Document
- Development Standards

### Lessons Learned

The project needs clear boundaries between core logic, adapters, interfaces, and AI.

### Next Sprint

Create the first domain models.
16. Error Handling Standards

Errors should be clear and useful.

Bad:

Error

Good:

Device 'light.office.ceiling' was not found in the device registry.

Where practical, use result objects instead of raw strings.

Example:

ActionResult(
    success=False,
    message="Device not found",
    reason="No registered device matched the provided device ID."
)
17. Result Object Standards

Operations that perform actions should return structured results.

Example fields:

success
message
reason
action_id
requires_confirmation
data

This helps CLI, API, voice, and AI interfaces respond consistently.

18. Logging Standards

The system should eventually log important events such as:

Device registered
Device state changed
Action requested
Action approved
Action blocked
Safety rule triggered
Adapter failure
AI proposal generated

Logs should be useful for debugging and future audit trails.

19. Configuration Standards

Configuration should be separated from code.

Local secrets should use environment variables or ignored config files.

Examples:

.env
.env.local
config.local.toml

These should not be committed.

20. AI Development Standards

The AI layer must remain separate from execution logic.

AI components should:

Interpret natural language
Propose structured actions
Ask for clarification when needed
Explain reasoning where useful
Use tools through defined interfaces

AI components should not:

Directly call adapters
Directly change device state
Bypass the Safety Engine
Execute risky actions without confirmation
21. Hardware Integration Standards

Hardware should be integrated only after the core model and services are stable.

When adding hardware support:

Add or update adapter.
Register devices through the registry.
Execute actions through services.
Pass actions through safety checks.
Add tests where possible.
Document setup steps.
22. Definition of Done

A feature is considered done when:

The code works for the intended use case.
The code follows the project structure.
Naming is clear.
Core logic is separated from adapters.
Safety impact has been considered.
Tests are added where appropriate.
Relevant documentation is updated.
ROADMAP.md, SPRINTS.md, or CHANGELOG.md are updated if needed.
23. Long-Term Standard

Every major decision should support this question:

Will this still make sense when HomeSteadOS controls hundreds of devices across multiple rooms, adapters, and interfaces?

If the answer is no, the design should be reconsidered.