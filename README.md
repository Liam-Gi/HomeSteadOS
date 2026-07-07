# HomeSteadOS

![Tests](https://github.com/Liam-Gi/HomeSteadOS/actions/workflows/tests.yml/badge.svg)

**HomeSteadOS** is a local-first AI home operating system designed to model, understand, and automate a residential environment.

## Current Status

HomeSteadOS is currently a backend MVP.

It includes:

- A Python domain model for rooms, devices, actions, scenes, shortcuts, and automations
- A CLI interface
- A FastAPI HTTP API
- A simulated device adapter
- Safety checks and confirmation workflows
- Audit logging and event tracking
- Text command parsing, previewing, suggestions, and history
- System snapshots for dashboard/frontend use
- Automated tests through GitHub Actions

The next major phase is a frontend control panel that uses the existing API.

## Project Scope

HomeSteadOS v1.0 is focused on the backend orchestration layer.

It is not currently trying to be:

- A full Home Assistant replacement
- A mobile app
- A production smart-home platform
- A voice assistant
- A cloud service
- A full AI agent

Future phases may add some of these, but the current goal is to stabilise the backend and build a simple frontend control panel.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/Liam-Gi/HomeSteadOS.git
cd HomeSteadOS

```

Create and activate a virtual environment:

python -m venv .venv

On Windows PowerShell:

.venv\Scripts\Activate.ps1

Install the project with development dependencies:

pip install -e ".[dev]"

Run the test suite:

pytest

Run the CLI:

homesteados

Run the API:

uvicorn homesteados.interfaces.api.app:app --reload