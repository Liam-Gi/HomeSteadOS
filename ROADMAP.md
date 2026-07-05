

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