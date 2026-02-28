# ADR-005: Matrix Transport + Native E2EE Rollout

- Status: Accepted
- Date: 2026-02-26

## Context

Axme currently delivers messages through HTTP APIs between adapters/MCP and `gateway` (`/v1/intents`, `/v1/inbox/*`).
Matrix/Synapse is present in infrastructure but not yet used as runtime transport.

Product requirement: move non-MCP delivery to Matrix transport with native Matrix E2EE at production security level.

## Decisions

1. **Cutover strategy**: hard cutover (target state is Matrix-only transport for non-MCP paths).
2. **Key ownership for service-side Matrix devices**: Axme-managed crypto service with KMS/HSM wrapped storage.
3. **Backend Matrix stack**: Python `matrix-nio` + native Matrix crypto (`Olm/Megolm`) for service accounts.
4. **Release gate**: full cryptographic acceptance gate (messages + media + key backup/restore + rotation + tamper/replay testing).

## Scope

In scope:

- Gateway transport migration from HTTP-only delivery semantics to Matrix event transport semantics.
- Message envelope upgrade to encrypted profile (`message.envelope.v3`).
- Storage changes for encrypted payload metadata and Matrix routing references.
- Matrix identity/device store persistence for service accounts (encrypted at rest via KMS-backed store).
- Integration and adversarial tests for E2EE delivery and media.

Out of scope:

- MCP-side final cryptographic flow (handled after non-MCP cutover stabilization).

## Target Architecture

1. **Transport**
   - `gateway` accepts canonical intent envelope and emits Matrix encrypted events into per-conversation rooms.
   - Internal HTTP APIs remain control plane only; message data plane is Matrix.

2. **Crypto**
   - Native Matrix E2EE only (`Olm/Megolm`).
   - No custom parallel ciphertext protocol for message body.

3. **Keys**
   - Service account device stores are encrypted before persistence.
   - Wrapped by KMS/HSM key hierarchy.
   - Rotation and recovery flows are mandatory release criteria.

4. **Storage**
   - Persistent message records keep transport and encrypted metadata (`ciphertext`, `algorithm`, `matrix_room_id`, `matrix_event_id`).
   - Plaintext storage is disallowed in Matrix transport mode.

## Rollout Plan

1. **Phase A: schema + storage foundation**
   - Add encrypted envelope schema `message.envelope.v3`.
   - Add Matrix metadata and encrypted device-store tables.
2. **Phase B: runtime transport**
   - Implement Matrix send/receive pipeline in gateway and delivery workers.
   - Disable plaintext reply paths in Matrix mode.
3. **Phase C: crypto operations**
   - KMS-backed encrypted device store and rotation workflows.
4. **Phase D: full acceptance suite**
   - Two-account distributed E2EE tests (Olm/Megolm), media encryption/decryption, tamper/replay, restore.

## Consequences

- Significant migration effort across protocol, delivery runtime, storage, and tests.
- Better long-term security posture and protocol correctness for encrypted messaging.
- MCP work is intentionally delayed until non-MCP cryptographic baseline is production-ready.
