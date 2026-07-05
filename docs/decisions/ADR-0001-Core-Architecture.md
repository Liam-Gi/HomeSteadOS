# ADR-0001: Core Architecture

## Status

Accepted

## Context

HomeSteadOS is intended to grow from an early software prototype into a local-first AI home operating system.

The system may eventually support:

- Simulated devices
- Home Assistant integration
- MQTT communication
- Real smart home hardware
- HTTP APIs
- Voice control
- Local AI models
- Safety policies
- Event-driven automation

A simple script-based structure would not scale well for this goal.

The project needs a structure that separates stable internal logic from external systems and future integrations.

## Decision

HomeSteadOS will use a layered architecture with a stable core and replaceable outer layers.

The primary layers are:

- `core`
- `adapters`
- `interfaces`
- `ai`
- `config`

The `core` layer contains the domain models, registries, services, events, safety logic, and result objects.

The `adapters` layer contains platform-specific integrations such as simulated devices, Home Assistant, and MQTT.

The `interfaces` layer contains ways users or systems interact with HomeSteadOS, such as CLI, API, and voice.

The `ai` layer contains AI planning, prompts, memory, tools, and model clients.

The `config` layer contains settings and logging configuration.

The core architecture rule is:

> The HomeSteadOS core must not depend directly on any specific hardware platform, smart home ecosystem, AI model, or communication protocol.

## Consequences

### Positive

- The core system can be tested without hardware.
- Simulated devices can be used before buying smart home equipment.
- Home Assistant can be used as an adapter rather than the system brain.
- MQTT can be added later without rewriting the core.
- AI can propose actions without directly controlling hardware.
- The system can evolve toward APIs, voice control, and real hardware without major restructuring.

### Negative

- The project has more structure before it has visible functionality.
- Early development may feel slower because architecture and documentation come first.
- Some placeholder modules will exist before they are implemented.

## Alternatives Considered

### Simple Script Structure

A simple script-based prototype would be faster initially, but would likely become difficult to maintain once devices, AI, services, safety checks, and adapters are added.

### Home Assistant-Centric Design

Building directly around Home Assistant would make real hardware integration faster, but would make HomeSteadOS less independent and less original as a software platform.

### AI-Centric Design

Letting the AI layer directly control devices would be simpler to prototype, but unsafe and difficult to audit.

## Decision Outcome

The layered architecture is accepted.

HomeSteadOS will prioritise a stable core, clear boundaries, testability, and safety before real hardware or AI features are added.