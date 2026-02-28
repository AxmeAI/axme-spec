# ADR-004: Synapse No-Modification Policy for MVP

- Status: Accepted
- Date: 2026-02-20

## Context

Axme MVP uses Matrix transport via Synapse. Forking or patching Synapse source in MVP increases maintenance cost and upgrade risk.

## Decision

Use official upstream Synapse image as-is for MVP. Do not modify Synapse source code.

Policy details:

- Allowed:
  - Runtime configuration via environment variables and mounted config/data
  - Operational tuning outside source modifications
- Not allowed:
  - Source forks, patches, or custom builds of Synapse for MVP
- Custom product logic must live in Axme services:
  - `gateway`
  - `agent_core`
  - `policy_engine`
  - `integrations`

## Consequences

- Faster security updates and predictable upstream compatibility.
- Clear ownership: protocol transport in Synapse, business behavior in Axme services.
- If transport-level custom behavior is needed later, it is treated as post-MVP architecture work.
