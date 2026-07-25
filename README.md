<div align="center">

# Prompt Experiment Platform

### Version prompts, split traffic, and select statistically supported winners

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

## Overview

Treats prompts as versioned production artifacts, supports template variables and rollback, assigns users consistently across multiple variants, records custom metrics, and reports whether observed differences are statistically significant.

## Core capabilities

| Capability | Implementation |
|---|---|
| Prompt registry | Version history, commit messages, diffs, and activation audit. |
| Template validation | Runtime variable substitution for versioned templates. |
| Experiments | Two or more variants with configurable traffic splits. |
| Consistent assignment | Stable SHA-256 user bucketing. |
| Metrics | Quality, error, and custom numeric observations. |
| Decision engine | Z-score significance and winner declaration. |

## Architecture

```mermaid
flowchart LR
P[Prompt registry] --> V[Versioned templates]
V --> E[Active experiment]
U[User ID] --> H[Consistent hash]
H --> A[Variant assignment]
A --> L[LLM serving adapter]
L --> M[Metric events]
M --> S[Significance analysis]
S --> W[Winner or continue]
```

## Quick start on Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev,dashboard]"
Copy-Item .env.example .env
pytest -q
prompt-lab seed
prompt-lab serve
```

API documentation: `http://localhost:8609/docs`

## Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

## Repository layout

```text
src/        application and domain logic
tests/      automated tests
data/       safe sample inputs and seed data
dashboard/  Streamlit review and analytics UI
scripts/    seed, evaluation, and demo commands
docs/       architecture notes
```

## Configuration and safety

- The default mode is offline and uses deterministic demo adapters.
- Cloud providers are optional and require keys placed only in `.env` or repository secrets.
- Sample data is synthetic. Do not upload private production logs or documents.
- Run `pytest -q` before every push.

Run `prompt-lab seed` to create a completed sample experiment. The platform uses a deterministic demo response so experimentation logic can be tested without an API key.

## License

[MIT](LICENSE)
