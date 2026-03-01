# ADR-001: Canonical Protocol Name

- Status: Accepted
- Date: 2026-02-20

## Context

Project docs had inconsistent legacy protocol naming, which created ambiguity in schemas, API docs, and onboarding materials.

## Decision

Use `AXP` as the single canonical protocol name for MVP and onward.

Use this canonical concept statement for protocol positioning:

- **AXP is the Intent Protocol (durable execution layer).**

## Consequences

- All new docs, schema IDs, and API references use `AXP`.
- Existing legacy aliases are replaced with `AXP`.
- This removes naming ambiguity and reduces integration mistakes.
- New materials should use intent-lifecycle language and avoid messaging-only or RPC-first framing.
