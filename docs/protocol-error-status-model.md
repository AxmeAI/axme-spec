# Protocol Error and Status Model (v1)

## Scope

Defines canonical payload models for workflow status updates and machine-readable errors.

## Schema Files

- `schemas/protocol/intent.status.v1.json`
- `schemas/protocol/intent.error.v1.json`

## Status Model (`intent.status.v1`)

Fields:

- `workflow_status` (required):
  - `planned`
  - `validated`
  - `running`
  - `blocked`
  - `done`
  - `failed`
- `updated_at` (required, RFC3339 timestamp)
- `reason` (optional, human-readable context)
- `actor` (optional, service or agent identity)

Usage:

- Emitted when workflow state changes.
- `blocked` and `failed` should include `reason` whenever possible.

## Error Model (`intent.error.v1`)

Fields:

- `code` (required, machine-readable stable code)
- `message` (required, human-readable summary)
- `category` (required):
  - `validation`
  - `auth`
  - `policy`
  - `transport`
  - `timeout`
  - `internal`
- `retryable` (required boolean)
- `at` (required, RFC3339 timestamp)
- `details` (optional key-value map)

Usage:

- Used for predictable API and workflow error payloads.
- `retryable=true` indicates caller may retry with same correlation context.
