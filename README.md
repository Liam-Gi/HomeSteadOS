# HomeSteadOS

![Tests](https://github.com/Liam-Gi/HomeSteadOS/actions/workflows/tests.yml/badge.svg)

**HomeSteadOS** is a local-first AI home operating system designed to model, understand, and automate a residential environment.

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