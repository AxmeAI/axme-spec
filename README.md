# axme-spec

AXP protocol specifications, schemas, and compatibility notes.

## Status

Wave 2 extraction in progress.

## Included through Wave 2

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
- Schema validation script, tests, and CI gate

## Development

```bash
python -m pip install -e ".[dev]"
python scripts/validate_schemas.py
pytest
```
