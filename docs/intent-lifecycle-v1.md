# Intent Lifecycle v1

Canonical concept: **AXP is the Intent Protocol (durable execution layer).**

This document defines the lifecycle contract for intent execution and observation in v1.

## Core Invariants

- `Intent` is the central durable execution primitive.
- Lifecycle changes are event-sourced and ordered by per-intent monotonic `seq`.
- `SUBMITTED` means the intent is durably persisted by the protocol.
- Delivery to downstream participants/subscribers is at-least-once.
- API interactions observe durable state evolution (non-RPC semantics).

## Status Model

Allowed statuses:

- `CREATED`
- `SUBMITTED`
- `DELIVERED`
- `ACKNOWLEDGED`
- `IN_PROGRESS`
- `WAITING`
- `COMPLETED`
- `FAILED`
- `CANCELED`

Allowed waiting reasons (`WAITING` only):

- `WAITING_FOR_HUMAN`
- `WAITING_FOR_TOOL`
- `WAITING_FOR_AGENT`
- `WAITING_FOR_TIME`

## Event Types

Lifecycle events are represented with `intent.event.v1`:

- `intent.created`
- `intent.submitted`
- `intent.delivered`
- `intent.acknowledged`
- `intent.in_progress`
- `intent.waiting`
- `intent.completed`
- `intent.failed`
- `intent.canceled`
- `intent.transfer`
- `intent.timeout`

## Transition Rules (v1)

Baseline allowed transitions:

- `CREATED -> SUBMITTED`
- `SUBMITTED -> DELIVERED | IN_PROGRESS | WAITING | FAILED | CANCELED`
- `DELIVERED -> ACKNOWLEDGED | IN_PROGRESS | WAITING | FAILED | CANCELED`
- `ACKNOWLEDGED -> IN_PROGRESS | WAITING | FAILED | CANCELED`
- `IN_PROGRESS -> WAITING | COMPLETED | FAILED | CANCELED`
- `WAITING -> IN_PROGRESS | FAILED | CANCELED`

Terminal statuses:

- `COMPLETED`
- `FAILED`
- `CANCELED`

`intent.transfer` does not require a status change, but updates active `handler`.

## Schemas

- `schemas/protocol/intent.lifecycle.v1.json`
- `schemas/protocol/intent.event.v1.json`
