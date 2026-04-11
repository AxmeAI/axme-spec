# axp-spec

**Normative source of truth for all AXP protocol and public API contracts.**

[![Alpha](https://img.shields.io/badge/status-alpha-orange)](https://cloud.axme.ai/alpha/cli)
[![License](https://img.shields.io/badge/license-see%20LICENSE-blue)](LICENSE)

[axme](https://github.com/AxmeAI/axme) · [Docs](https://github.com/AxmeAI/axme-docs) · [Conformance](https://github.com/AxmeAI/axme-conformance)

---

AXP is the open wire protocol behind AXME. This repo defines the normative contracts - everything else (runtime, SDKs, conformance suite) derives from or validates against these schemas.

---

## What Lives Here

```
axp-spec/
├── schemas/
│   ├── protocol/              # AXP wire protocol definitions (envelope, frames, versioning)
│   └── public_api/            # Public REST API contracts (request/response/error schemas)
├── docs/
│   ├── diagrams/              # Schema-level visualizations
│   ├── ADR-001-protocol-name.md
│   ├── ADR-004-synapse-no-modification-policy.md
│   ├── ADR-005-matrix-transport-e2ee-rollout.md
│   ├── ADR-006-intent-lifecycle-v1.md
│   ├── idempotency-correlation-rules.md
│   ├── intent-lifecycle-v1.md
│   ├── protocol-error-status-model.md
│   ├── public-api-schema-index.md
│   └── schema-versioning-rules.md
└── scripts/
    └── validate_schemas.py
```

> **Note on ADRs:** ADR-001, ADR-004 through ADR-006 live here. ADR-002 (service boundaries) and ADR-003 (trust/consent model) are hosted in [`axme-docs`](https://github.com/AxmeAI/axme-docs/tree/main/docs) as they span the full platform rather than schema contracts specifically.

---

## Intent Lifecycle

Every intent follows a durable lifecycle with explicit states:

```
CREATED -> ACCEPTED -> PROCESSING -> COMPLETED
                          |
                          v
                       WAITING (human / agent / time / tool)
                          |
                          v
                       PROCESSING -> COMPLETED
                                        |
                                     FAILED
```

- **CREATED** - intent submitted, validated, persisted
- **ACCEPTED** - routed to handler agent
- **PROCESSING** - agent is working on it
- **WAITING** - paused for human approval, timeout, external signal, or sub-intent
- **COMPLETED** - terminal success with result
- **FAILED** - terminal failure with error

Waiting states are first-class. An intent can wait for hours or days and resume exactly where it left off.

---

## Delivery Bindings

Five ways to deliver an intent to an agent:

| Binding | How it works | Use case |
|---|---|---|
| **stream** | SSE persistent connection - agent stays connected, intents pushed in real-time | Low-latency, always-on agents |
| **poll** | Agent pulls on its own schedule via `GET /v1/intents?status=pending` | Batch processing, cron jobs |
| **http** | Platform pushes to agent's URL (webhook with HMAC signature) | Serverless functions, existing APIs |
| **inbox** | Human-facing task queue - tasks appear in CLI (`axme tasks list`) or email | Human-in-the-loop workflows |
| **internal** | Runs inside the platform runtime - no external agent needed | Timeouts, reminders, approvals |

---

## Runtime Steps

### Internal steps (no agent needed)

These run inside the AXME runtime without any external agent:

| Step | What it does |
|---|---|
| **human_approval** | Pause workflow, wait for human to approve/reject via CLI, email magic link, or web form |
| **timeout** | Fail the intent if not completed within a deadline |
| **reminder** | Send a reminder after N seconds of waiting |
| **delay** | Pause workflow for a fixed duration before continuing |
| **escalation** | Chain of reminders with increasing urgency |
| **notification** | Send a one-way notification (email, webhook) without waiting |

### Human task types

Eight structured task types for human-in-the-loop workflows:

| Type | Purpose |
|---|---|
| **approval** | Yes/no gate - deploys, budgets, agent actions |
| **form** | Structured input with required fields - config, onboarding data |
| **review** | Approve, request changes, or reject with comments - code review, document sign-off |
| **override** | Bypass a policy gate with mandatory justification (audit-logged) |
| **confirmation** | Confirm a real-world action was completed - deployment verified, payment sent |
| **assignment** | Route work to a person or team with structured fields |
| **clarification** | Request missing context - comment required before proceeding |
| **manual_action** | Complete a physical task and attach evidence - hardware swap, site inspection |

---

## ScenarioBundle

The simplest way to run a workflow - one JSON file:

```json
{
  "agents": [{"address": "my-service", "delivery_mode": "stream"}],
  "workflow": {"steps": [{"step_id": "process", "assigned_to": "my-service"}]},
  "intent": {"type": "task.v1", "payload": {"data": "..."}}
}
```

```bash
axme scenarios apply scenario.json --watch
```

This provisions agents, compiles the workflow, submits the intent, and streams lifecycle events - all in one command.

---

## Protocol Envelope

The AXP envelope wraps every intent. It carries the payload, sender identity, schema version, idempotency key, and a cryptographic signature applied at the gateway boundary.

![AXP Protocol Envelope](https://raw.githubusercontent.com/AxmeAI/axme-docs/main/docs/diagrams/protocol/01-protocol-envelope.svg)

*Each field in the envelope is normatively defined here. The runtime and all SDKs must conform to these field names, types, and validation rules.*

---

## Related Repositories

| Repository | Relationship |
|---|---|
| [axme-docs](https://github.com/AxmeAI/axme-docs) | Derives OpenAPI artifacts and narrative docs from these schemas |
| [axme-conformance](https://github.com/AxmeAI/axme-conformance) | Validates runtime and SDK behavior against these contracts |
| Control-plane runtime (private) | Runtime implementation must conform to schemas defined here |
| [axme-sdk-python](https://github.com/AxmeAI/axme-sdk-python) | Python client - API surface derived from these contracts |
| [axme-sdk-typescript](https://github.com/AxmeAI/axme-sdk-typescript) | TypeScript client |
| [axme-sdk-go](https://github.com/AxmeAI/axme-sdk-go) | Go client |
| [axme-sdk-java](https://github.com/AxmeAI/axme-sdk-java) | Java client |
| [axme-sdk-dotnet](https://github.com/AxmeAI/axme-sdk-dotnet) | .NET client |

---

<details>
<summary><strong>Schema Governance (for contributors)</strong></summary>

### Schema Versioning and Deprecation

Schemas follow a three-phase lifecycle: stable -> deprecated -> removed. Breaking changes require a new major schema version. Additive changes are backward-compatible.

![Versioning and Deprecation Flow](https://raw.githubusercontent.com/AxmeAI/axme-docs/main/docs/diagrams/protocol/02-versioning-and-deprecation-flow.svg)

*A schema version enters deprecation with a minimum 90-day notice period. Clients targeting a deprecated version receive `Deprecation` response headers. Removal is announced in the migration guide.*

### Schema Governance and Compatibility

All schema changes go through a governance review before landing. The compatibility matrix ensures no existing consumer breaks across patch and minor versions.

![Schema Governance and Compatibility](https://raw.githubusercontent.com/AxmeAI/axme-docs/main/docs/diagrams/protocol/04-schema-governance-compatibility.svg)

*Governance steps: proposal -> impact analysis -> compatibility check -> reviewer sign-off -> merge -> changelog entry -> docs sync.*

### Intent Payload Extensibility

Intent schemas are typed by `intent_type`. The payload field is a structured JSON object defined per type - not a free-form blob.

![Intent Payload Extensibility and Semantic Schemas](https://raw.githubusercontent.com/AxmeAI/axme-docs/main/docs/diagrams/intents/09-intent-payload-extensibility-and-semantic-schemas.svg)

### Public API Error Model

All error responses follow a uniform model: HTTP status + machine-readable error code + retriability hint.

![Public API Error Model and Retriability](https://raw.githubusercontent.com/AxmeAI/axme-docs/main/docs/diagrams/api/02-error-model-retriability.svg)

### Integration Rule

A contract family is considered complete only when it is aligned across all five layers:

1. **`axp-spec`** - normative schema definition (this repo)
2. **`axme-docs`** - OpenAPI artifact and narrative documentation
3. **SDK clients** - implemented and tested method in each of the five SDKs
4. **`axme-conformance`** - conformance check covering the contract
5. **Runtime** - `axme-control-plane` behavior matches the schema

### Validation

```bash
python -m pip install -e ".[dev]"
python scripts/validate_schemas.py
pytest
```

</details>

---

## Contributing

- Schema proposals and breaking-change requests: open an issue with label `schema-proposal`
- Contribution guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)

---

[contact@axme.ai](mailto:contact@axme.ai) · [@axme_ai](https://x.com/axme_ai) · [Security](SECURITY.md) · [License](LICENSE)
