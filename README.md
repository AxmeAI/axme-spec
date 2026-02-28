# axme-spec

AXP protocol specifications, schemas, and compatibility notes.

## Status

Wave 1 extraction in progress.

## Included in Wave 1

- `schemas/protocol/message.envelope.v2.json`
- `schemas/protocol/message.delivery.v1.json`
- schema validation script and CI gate

## Development

```bash
python -m pip install -e ".[dev]"
python scripts/validate_schemas.py
pytest
```
