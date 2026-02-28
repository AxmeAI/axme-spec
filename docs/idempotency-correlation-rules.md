# Idempotency and Correlation Rules (v1)

## Purpose

Define deterministic behavior for retries and multi-step workflow tracing.

## Identifiers

- `intent_id`
  - Unique per intent message/event.
  - Must be a UUID.
- `correlation_id`
  - Stable UUID shared across all messages/events in the same logical workflow.
  - Must remain unchanged across retries and follow-up actions for the same workflow.
- `idempotency_key` (optional in envelope, required for external retry-safe writes)
  - Stable client-generated token for deduplicating create operations.

## Idempotency Rules

- Deduplication key for create operations:
  - `(sender_identity, endpoint, idempotency_key)`
- If the same dedup key is received again, service must return the original accepted result.
- If payload differs under the same dedup key, service should reject with a conflict error.
- Recommended key TTL for dedup cache/index in MVP:
  - at least 24 hours.

## Correlation Rules

- New workflow:
  - Generate a new `correlation_id`.
- Existing workflow step/retry:
  - Reuse the same `correlation_id`.
- All status and error events must be attributable to the same `correlation_id`.

## Error Handling Guidance

- Validation/auth errors:
  - usually non-retryable with same payload.
- Transport/timeout errors:
  - may be retryable with the same `idempotency_key` and `correlation_id`.
