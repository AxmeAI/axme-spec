# ADR-006: Intent Lifecycle v1 Baseline

- Status: Accepted
- Date: 2026-03-01

## Context

AXP positioning was standardized as: **AXP is the Intent Protocol (durable execution layer)**.

The protocol needed a single, explicit lifecycle model for durable execution semantics,
including status transitions, waiting reasons, and ordered lifecycle events.

## Decision

Adopt the Intent Lifecycle v1 baseline with the following constraints:

- Intent state is represented by status + monotonic per-intent `seq`.
- Lifecycle changes are materialized through explicit `intent.*` events.
- `WAITING` state always includes an explicit waiting reason.
- Timeout is represented as lifecycle signal (`intent.timeout` and resulting status), not as hidden transport/RPC failure.
- Lifecycle semantics are non-RPC: consumers observe progression via state + events.

Concrete schema artifacts:

- `schemas/protocol/intent.lifecycle.v1.json`
- `schemas/protocol/intent.event.v1.json`

Normative reference:

- `docs/intent-lifecycle-v1.md`

## Consequences

- Runtime implementations can align on a single durable execution lifecycle contract.
- SDKs and API docs can expose a stable intent-first model.
- Conformance suites can validate ordered events and transition legality using shared semantics.
