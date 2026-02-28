# axme-spec

AXP protocol specifications, schemas, and compatibility notes.

## Status

Wave 4 extraction in progress.

## Included through Wave 4

- Protocol schemas:
  - `schemas/protocol/intent.ask.v1.json`
  - `schemas/protocol/intent.envelope.v1.json`
  - `schemas/protocol/intent.error.v1.json`
  - `schemas/protocol/intent.reply.v1.json`
  - `schemas/protocol/intent.status.v1.json`
  - `schemas/protocol/message.delivery.v1.json`
  - `schemas/protocol/message.envelope.v2.json`
  - `schemas/protocol/message.envelope.v3.json`
- Governance docs:
  - `docs/public-api-schema-index.md`
  - `docs/schema-versioning-rules.md`
  - `docs/protocol-error-status-model.md`
  - `docs/idempotency-correlation-rules.md`
- Public API schemas (core set):
  - `schemas/public_api/api.intents.create.request.v1.json`
  - `schemas/public_api/api.intents.create.response.v1.json`
  - `schemas/public_api/api.intents.get.response.v1.json`
  - `schemas/public_api/api.approvals.decision.request.v1.json`
  - `schemas/public_api/api.approvals.decision.response.v1.json`
  - `schemas/public_api/api.capabilities.get.response.v1.json`
- Public API schemas (inbox set):
  - `schemas/public_api/api.inbox.list.response.v1.json`
  - `schemas/public_api/api.inbox.changes.response.v1.json`
  - `schemas/public_api/api.inbox.thread.response.v1.json`
  - `schemas/public_api/api.inbox.reply.request.v1.json`
  - `schemas/public_api/api.inbox.messages.delete.request.v1.json`
  - `schemas/public_api/api.inbox.messages.delete.response.v1.json`
  - `schemas/public_api/api.inbox.delegate.request.v1.json`
  - `schemas/public_api/api.inbox.decision.request.v1.json`
- Schema validation script, tests, and CI gate

## Development

```bash
python -m pip install -e ".[dev]"
python scripts/validate_schemas.py
pytest
```
