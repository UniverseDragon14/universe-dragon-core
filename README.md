# Universal Dragon Core

Universal Dragon Core is the small, auditable foundation repository for the Universal Dragon system architecture.

It is intentionally separated from private keys, backend secrets, device credentials, and unstable experiments.

## Current Scope

This repository now implements a real foundation API for:

- NOVA / EVE / DRAGON request routing
- bounded input validation
- policy evaluation
- explicit approval gating for risky or externally-visible actions
- action receipts
- safe server error handling
- health and capability endpoints
- automated backend tests in GitHub Actions

It does **not** claim to be a complete autonomous operating system or a configured LLM provider. External execution remains disabled in this foundation layer.

## Safety Boundary

```text
request
  -> validate
  -> route
  -> plan action
  -> classify risk
  -> policy decision
  -> approval when required
  -> tool execution (future authorized layer)
  -> verify
  -> receipt
```

The current repository stops before tool execution.

### Policy behavior

- **Low risk + no external effect** -> `ready`
- **Medium risk** -> `waiting_policy`
- **High risk** -> `waiting_approval`
- **Any external effect** -> `waiting_approval`

No action-planning API call executes the requested action.

## API

### Health

```http
GET /api/health
```

### Capabilities

```http
GET /api/capabilities
```

### Core routing

```http
POST /api/chat
Content-Type: application/json

{
  "mode": "nova",
  "message": "Check the system architecture"
}
```

Supported modes are `nova`, `eve`, and `dragon`.

### Action planning

```http
POST /api/actions/plan
Content-Type: application/json

{
  "action_type": "send_message",
  "description": "Send a message to an external recipient",
  "risk": "high",
  "external_effect": true
}
```

The response contains a receipt and policy state. It does not execute the action.

## Local Development

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Run tests:

```bash
pytest -q backend/tests
```

## Core Workflow

```text
doctor -> backup -> patch -> test -> approval -> deploy -> rollback ready
```

The doctor, backup, patch, rollback, model-provider, and authorized tool-execution layers remain separate implementation stages. They should be added only with tests and clear evidence.

## Security Rules

- no API keys or tokens in the repository
- no private IP addresses in public configuration
- no silent destructive commands
- no raw upstream/provider errors returned to clients
- CORS origins must be explicitly configured with `FRONTEND_ORIGINS`
- risky or externally-visible actions require approval
- security work remains defensive and authorized

## Project Identity

- **Universal Dragon**: main project identity
- **Aslam**: creator / founder identity
- **NOVA / EVE**: reasoning and assistant layer
- **DRAGON**: action-oriented mode, still subject to policy and approval

## Status

**Foundation v0.2 is implemented on the continuation branch.**

Next stages should connect an approved model/provider, persistent audit storage, authenticated approvals, verification, and bounded tool adapters without weakening the safety boundary above.
