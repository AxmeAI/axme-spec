# Schema Versioning Rules

## Scope

Rules apply to:

- `schemas/protocol/`
- `schemas/public_api/`

## Naming

- Protocol filename format: `intent.<name>.v<version>.json`
- Public API filename format: `api.<domain>.<action>.<request|response>.v<version>.json`
- Current stable major for MVP: `v1`

## Compatibility

- Backward-compatible additions (optional fields, relaxed constraints) may remain in the same major version.
- Breaking changes (required fields, stricter constraints, enum removals/renames, semantic behavior changes) require a new major version file (`v2`, `v3`, ...).

## Change Policy

- Never overwrite the behavior of an existing released major version.
- New major version is introduced as a new file.
- Keep old major versions available while clients migrate.

## Validation Gate

- All schema files must pass `python scripts/validate_schemas.py`.
- CI workflow `Schema Validation` must stay green before merge.
- Contract tests for valid/invalid payload behavior must pass:
  - `pytest -q tests/test_schema_contracts.py`
  - `pytest -q tests/test_public_api_schema_contracts.py`

## Required Protocol Schemas (v1 line)

- `intent.envelope.v1.json`
- `intent.ask.v1.json`
- `intent.reply.v1.json`
- `intent.status.v1.json`
- `intent.error.v1.json`

## Required Public API Schemas (v1 line)

- `api.intents.create.request.v1.json`
- `api.intents.create.response.v1.json`
- `api.intents.get.response.v1.json`
- `api.approvals.decision.request.v1.json`
- `api.approvals.decision.response.v1.json`
- `api.webhooks.events.request.v1.json`
- `api.webhooks.events.response.v1.json`
- `api.capabilities.get.response.v1.json`
- `api.inbox.list.response.v1.json`
- `api.inbox.thread.response.v1.json`
- `api.inbox.reply.request.v1.json`
- `api.inbox.delegate.request.v1.json`
- `api.inbox.decision.request.v1.json`
