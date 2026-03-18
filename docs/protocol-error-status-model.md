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

### Standard Error Codes

The `code` field is a stable, machine-readable identifier. The following codes are defined by the protocol:

| Code | Category | Retryable | Description |
|---|---|---|---|
| `agent_not_found` | `transport` | No | The target agent does not exist in the registry. |
| `invalid_agent_address` | `validation` | No | The agent address is syntactically invalid or does not conform to the expected format. |
| `schema_invalid` | `validation` | No | The intent payload does not conform to the expected schema. |
| `auth_failed` | `auth` | No | Authentication or authorization failed. |
| `policy_denied` | `policy` | No | The request was rejected by a policy rule. |
| `delivery_failed` | `transport` | Yes | The intent could not be delivered to the target agent. |
| `intent_timeout` | `timeout` | Yes | The intent exceeded its deadline without completion. |
| `internal_error` | `internal` | Yes | An unexpected internal error occurred. |

Implementations may define additional codes within the `^[a-z0-9_:.\-]{3,128}$` pattern. Standard codes should be used where applicable for cross-implementation interoperability.

Usage:

- Used for predictable API and workflow error payloads.
- `retryable=true` indicates caller may retry with same correlation context.
