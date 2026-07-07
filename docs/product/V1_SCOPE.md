# HomeSteadOS v1.0 Scope

## Purpose

HomeSteadOS v1.0 is a local-first home automation orchestration backend.

It models a home, accepts structured and text-based commands, routes actions through safety checks, executes actions through services and adapters, and exposes functionality through a CLI and HTTP API.

## v1.0 Goal

The goal of v1.0 is to provide a stable backend foundation that can support a frontend control panel, future Home Assistant integration, and future AI/voice interfaces.

## Current v1.0 Capabilities

HomeSteadOS currently supports:

- Config-driven rooms and devices
- Simulated device adapter
- Device and room registries
- System modes
- Safety engine
- Confirmation workflow
- Event bus
- Audit logging
- Diagnostics and health checks
- HTTP API
- CLI interface
- Text command parsing
- Command preview
- Command suggestions
- Command history
- Behaviour insights
- Scenes
- Shortcuts
- Automation rules
- System snapshots
- GitHub Actions test workflow

## Primary Control Paths

### CLI

Users can interact with HomeSteadOS through the command line.

Example commands:

```text
devices
rooms
snapshot
turn on office light
preview run good night
run good night
run shortcut bedtime
set mode night
history
audit

```
API

External clients can interact with HomeSteadOS through the FastAPI HTTP API.

Main API areas:

System status
System mode
System snapshot
Devices
Rooms
Actions
Text commands
Scenes
Shortcuts
Automations
Audit log
Command history
Behaviour insights
v1.0 Design Principles
Local first
Privacy first
Safety before convenience
AI should propose actions, not directly control devices
All control paths should use structured Actions
Services should not bypass the Safety Engine
Runtime state should be inspectable through safe read-only services
Features should be testable and explainable
Explicitly Out of Scope for v1.0

The following are intentionally not part of v1.0:

Full AI planner
Voice control
Mobile app
User accounts
Role-based permissions
Database persistence
Complex automation condition logic
Scheduling engine
Real-time Home Assistant state sync
MQTT integration
Cloud deployment
Notifications
Advanced analytics
Machine learning