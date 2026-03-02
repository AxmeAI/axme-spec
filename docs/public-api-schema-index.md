# Public API Schema Index (Step 4)

## Scope

Schemas for external client contracts in `services/gateway` API.

Intent lifecycle baseline (durable execution semantics) is defined in:

- `docs/intent-lifecycle-v1.md`
- `schemas/protocol/intent.lifecycle.v1.json`
- `schemas/protocol/intent.event.v1.json`

Public API status projection rule:

- `intent.status` is canonical lifecycle status (`CREATED` -> terminal).
- `intent.legacy_status` is optional compatibility projection for legacy clients.

Related artifacts:

- OpenAPI export: `docs/openapi/gateway.v1.json`
- Auth/idempotency/rate-limit docs: `docs/public-api-auth.md`

## Files

- `schemas/public_api/api.intents.create.request.v1.json`
- `schemas/public_api/api.intents.create.response.v1.json`
- `schemas/public_api/api.intents.get.response.v1.json`
- `schemas/public_api/api.intents.events.list.response.v1.json`
- `schemas/public_api/api.intents.resolve.request.v1.json`
- `schemas/public_api/api.intents.resolve.response.v1.json`
- `schemas/public_api/api.approvals.decision.request.v1.json`
- `schemas/public_api/api.approvals.decision.response.v1.json`
- `schemas/public_api/api.webhooks.events.request.v1.json`
- `schemas/public_api/api.webhooks.events.response.v1.json`
- `schemas/public_api/api.webhooks.events.replay.response.v1.json`
- `schemas/public_api/api.webhooks.subscriptions.upsert.request.v1.json`
- `schemas/public_api/api.webhooks.subscriptions.response.v1.json`
- `schemas/public_api/api.webhooks.subscriptions.list.response.v1.json`
- `schemas/public_api/api.webhooks.subscriptions.delete.response.v1.json`
- `schemas/public_api/api.capabilities.get.response.v1.json`
- `schemas/public_api/api.schemas.upsert.request.v1.json`
- `schemas/public_api/api.schemas.upsert.response.v1.json`
- `schemas/public_api/api.schemas.get.response.v1.json`
- `schemas/public_api/api.inbox.list.response.v1.json`
- `schemas/public_api/api.inbox.changes.response.v1.json`
- `schemas/public_api/api.inbox.thread.response.v1.json`
- `schemas/public_api/api.inbox.reply.request.v1.json`
- `schemas/public_api/api.inbox.messages.delete.request.v1.json`
- `schemas/public_api/api.inbox.messages.delete.response.v1.json`
- `schemas/public_api/api.inbox.delegate.request.v1.json`
- `schemas/public_api/api.inbox.decision.request.v1.json`
- `schemas/public_api/api.users.register_nick.request.v1.json`
- `schemas/public_api/api.users.register_nick.response.v1.json`
- `schemas/public_api/api.users.check_nick.response.v1.json`
- `schemas/public_api/api.users.rename_nick.request.v1.json`
- `schemas/public_api/api.users.rename_nick.response.v1.json`
- `schemas/public_api/api.users.profile.get.response.v1.json`
- `schemas/public_api/api.users.profile.update.request.v1.json`
- `schemas/public_api/api.users.profile.update.response.v1.json`
- `schemas/public_api/api.invites.create.request.v1.json`
- `schemas/public_api/api.invites.create.response.v1.json`
- `schemas/public_api/api.invites.get.response.v1.json`
- `schemas/public_api/api.invites.accept.request.v1.json`
- `schemas/public_api/api.invites.accept.response.v1.json`
- `schemas/public_api/api.media.create_upload.request.v1.json`
- `schemas/public_api/api.media.create_upload.response.v1.json`
- `schemas/public_api/api.media.finalize_upload.request.v1.json`
- `schemas/public_api/api.media.finalize_upload.response.v1.json`
- `schemas/public_api/api.media.get.response.v1.json`

## Endpoint Mapping

- `POST /v1/intents`
  - request: `api.intents.create.request.v1.json`
  - response: `api.intents.create.response.v1.json`
- `GET /v1/intents/{intent_id}`
  - response: `api.intents.get.response.v1.json`
- `GET /v1/intents/{intent_id}/events`
  - response: `api.intents.events.list.response.v1.json`
- `POST /v1/intents/{intent_id}/resolve`
  - request: `api.intents.resolve.request.v1.json`
  - response: `api.intents.resolve.response.v1.json`
- `GET /v1/intents/{intent_id}/events/stream`
  - transport: `text/event-stream` (SSE)
  - event payload shape: same event object as `api.intents.events.list.response.v1.json` item
- `POST /v1/approvals/{approval_id}/decision`
  - request: `api.approvals.decision.request.v1.json`
  - response: `api.approvals.decision.response.v1.json`
- `POST /v1/webhooks/events`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.webhooks.events.request.v1.json`
  - response: `api.webhooks.events.response.v1.json`
- `POST /v1/webhooks/events/{event_id}/replay`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.webhooks.events.replay.response.v1.json`
- `POST /v1/webhooks/subscriptions`
  - request: `api.webhooks.subscriptions.upsert.request.v1.json`
  - response: `api.webhooks.subscriptions.response.v1.json`
- `GET /v1/webhooks/subscriptions`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.webhooks.subscriptions.list.response.v1.json`
- `DELETE /v1/webhooks/subscriptions/{subscription_id}`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.webhooks.subscriptions.delete.response.v1.json`
- `GET /v1/capabilities`
  - response: `api.capabilities.get.response.v1.json`
- `POST /v1/schemas`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.schemas.upsert.request.v1.json`
  - response: `api.schemas.upsert.response.v1.json`
- `GET /v1/schemas/{semantic_type}`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.schemas.get.response.v1.json`
- `GET /v1/inbox`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.inbox.list.response.v1.json`
- `GET /v1/inbox/changes`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.inbox.changes.response.v1.json`
- `GET /v1/inbox/{thread_id}`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - response: `api.inbox.thread.response.v1.json`
- `POST /v1/inbox/{thread_id}/reply`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.inbox.reply.request.v1.json`
  - response: `api.inbox.thread.response.v1.json`
- `POST /v1/inbox/{thread_id}/messages/delete`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.inbox.messages.delete.request.v1.json`
  - response: `api.inbox.messages.delete.response.v1.json`
- `POST /v1/inbox/{thread_id}/delegate`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.inbox.delegate.request.v1.json`
  - response: `api.inbox.thread.response.v1.json`
- `POST /v1/inbox/{thread_id}/approve`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.inbox.decision.request.v1.json`
  - response: `api.inbox.thread.response.v1.json`
- `POST /v1/inbox/{thread_id}/reject`
  - owner scoping: `x-owner-agent` header or `owner_agent` query
  - request: `api.inbox.decision.request.v1.json`
  - response: `api.inbox.thread.response.v1.json`
- `POST /v1/users/register-nick`
  - request: `api.users.register_nick.request.v1.json`
  - response: `api.users.register_nick.response.v1.json`
- `GET /v1/users/check-nick?nick=...`
  - response: `api.users.check_nick.response.v1.json`
- `POST /v1/users/rename-nick`
  - request: `api.users.rename_nick.request.v1.json`
  - response: `api.users.rename_nick.response.v1.json`
- `GET /v1/users/profile?owner_agent=...`
  - response: `api.users.profile.get.response.v1.json`
- `POST /v1/users/profile/update`
  - request: `api.users.profile.update.request.v1.json`
  - response: `api.users.profile.update.response.v1.json`
- `POST /v1/invites/create`
  - request: `api.invites.create.request.v1.json`
  - response: `api.invites.create.response.v1.json`
- `GET /v1/invites/{token}`
  - response: `api.invites.get.response.v1.json`
- `POST /v1/invites/{token}/accept`
  - request: `api.invites.accept.request.v1.json`
  - response: `api.invites.accept.response.v1.json`
- `POST /v1/media/create-upload`
  - request: `api.media.create_upload.request.v1.json`
  - response: `api.media.create_upload.response.v1.json`
- `POST /v1/media/finalize-upload`
  - request: `api.media.finalize_upload.request.v1.json`
  - response: `api.media.finalize_upload.response.v1.json`
- `GET /v1/media/{upload_id}`
  - response: `api.media.get.response.v1.json`

## Track F Phase 1 Families (Draft Contracts)

### Files

- `schemas/public_api/api.organizations.create.request.v1.json`
- `schemas/public_api/api.organizations.create.response.v1.json`
- `schemas/public_api/api.organizations.get.response.v1.json`
- `schemas/public_api/api.organizations.update.request.v1.json`
- `schemas/public_api/api.organizations.update.response.v1.json`
- `schemas/public_api/api.organizations.workspaces.create.request.v1.json`
- `schemas/public_api/api.organizations.workspaces.create.response.v1.json`
- `schemas/public_api/api.organizations.workspaces.list.response.v1.json`
- `schemas/public_api/api.organizations.workspaces.update.request.v1.json`
- `schemas/public_api/api.organizations.workspaces.update.response.v1.json`
- `schemas/public_api/api.organizations.members.list.response.v1.json`
- `schemas/public_api/api.organizations.members.add.request.v1.json`
- `schemas/public_api/api.organizations.members.add.response.v1.json`
- `schemas/public_api/api.organizations.members.update.request.v1.json`
- `schemas/public_api/api.organizations.members.update.response.v1.json`
- `schemas/public_api/api.organizations.members.remove.response.v1.json`
- `schemas/public_api/api.access_requests.create.request.v1.json`
- `schemas/public_api/api.access_requests.create.response.v1.json`
- `schemas/public_api/api.access_requests.list.response.v1.json`
- `schemas/public_api/api.access_requests.get.response.v1.json`
- `schemas/public_api/api.access_requests.review.request.v1.json`
- `schemas/public_api/api.access_requests.review.response.v1.json`

### Planned Endpoint Mapping

- `POST /v1/organizations`
  - request: `api.organizations.create.request.v1.json`
  - response: `api.organizations.create.response.v1.json`
- `GET /v1/organizations/{org_id}`
  - response: `api.organizations.get.response.v1.json`
- `PATCH /v1/organizations/{org_id}`
  - request: `api.organizations.update.request.v1.json`
  - response: `api.organizations.update.response.v1.json`
- `POST /v1/organizations/{org_id}/workspaces`
  - request: `api.organizations.workspaces.create.request.v1.json`
  - response: `api.organizations.workspaces.create.response.v1.json`
- `GET /v1/organizations/{org_id}/workspaces`
  - response: `api.organizations.workspaces.list.response.v1.json`
- `PATCH /v1/organizations/{org_id}/workspaces/{workspace_id}`
  - request: `api.organizations.workspaces.update.request.v1.json`
  - response: `api.organizations.workspaces.update.response.v1.json`
- `GET /v1/organizations/{org_id}/members`
  - response: `api.organizations.members.list.response.v1.json`
- `POST /v1/organizations/{org_id}/members`
  - request: `api.organizations.members.add.request.v1.json`
  - response: `api.organizations.members.add.response.v1.json`
- `PATCH /v1/organizations/{org_id}/members/{member_id}`
  - request: `api.organizations.members.update.request.v1.json`
  - response: `api.organizations.members.update.response.v1.json`
- `DELETE /v1/organizations/{org_id}/members/{member_id}`
  - response: `api.organizations.members.remove.response.v1.json`
- `POST /v1/access-requests`
  - request: `api.access_requests.create.request.v1.json`
  - response: `api.access_requests.create.response.v1.json`
- `GET /v1/access-requests`
  - response: `api.access_requests.list.response.v1.json`
- `GET /v1/access-requests/{access_request_id}`
  - response: `api.access_requests.get.response.v1.json`
- `POST /v1/access-requests/{access_request_id}/review`
  - request: `api.access_requests.review.request.v1.json`
  - response: `api.access_requests.review.response.v1.json`

## Track F Phase 1 Quota and Usage Families (Draft Contracts)

### Files

- `schemas/public_api/api.quotas.get.response.v1.json`
- `schemas/public_api/api.quotas.update.request.v1.json`
- `schemas/public_api/api.quotas.update.response.v1.json`
- `schemas/public_api/api.usage.summary.get.response.v1.json`
- `schemas/public_api/api.usage.timeseries.get.response.v1.json`

### Planned Endpoint Mapping

- `GET /v1/quotas?org_id=...&workspace_id=...`
  - response: `api.quotas.get.response.v1.json`
- `PATCH /v1/quotas`
  - request: `api.quotas.update.request.v1.json`
  - response: `api.quotas.update.response.v1.json`
- `GET /v1/usage/summary?org_id=...&workspace_id=...`
  - response: `api.usage.summary.get.response.v1.json`
- `GET /v1/usage/timeseries?org_id=...&workspace_id=...`
  - response: `api.usage.timeseries.get.response.v1.json`

## Track F Phase 2 Service Accounts Families (Draft Contracts)

### Files

- `schemas/public_api/api.service_accounts.create.request.v1.json`
- `schemas/public_api/api.service_accounts.create.response.v1.json`
- `schemas/public_api/api.service_accounts.list.response.v1.json`
- `schemas/public_api/api.service_accounts.get.response.v1.json`
- `schemas/public_api/api.service_accounts.keys.create.request.v1.json`
- `schemas/public_api/api.service_accounts.keys.create.response.v1.json`
- `schemas/public_api/api.service_accounts.keys.revoke.response.v1.json`

### Planned Endpoint Mapping

- `POST /v1/service-accounts`
  - request: `api.service_accounts.create.request.v1.json`
  - response: `api.service_accounts.create.response.v1.json`
- `GET /v1/service-accounts?org_id=...&workspace_id=...`
  - response: `api.service_accounts.list.response.v1.json`
- `GET /v1/service-accounts/{service_account_id}`
  - response: `api.service_accounts.get.response.v1.json`
- `POST /v1/service-accounts/{service_account_id}/keys`
  - request: `api.service_accounts.keys.create.request.v1.json`
  - response: `api.service_accounts.keys.create.response.v1.json`
- `POST /v1/service-accounts/{service_account_id}/keys/{key_id}/revoke`
  - response: `api.service_accounts.keys.revoke.response.v1.json`

## Track F Phase 2 Billing Families (Draft Contracts)

### Files

- `schemas/public_api/api.billing.plan.update.request.v1.json`
- `schemas/public_api/api.billing.plan.update.response.v1.json`
- `schemas/public_api/api.billing.plan.get.response.v1.json`
- `schemas/public_api/api.billing.invoices.list.response.v1.json`
- `schemas/public_api/api.billing.invoices.get.response.v1.json`

### Planned Endpoint Mapping

- `PATCH /v1/billing/plan`
  - request: `api.billing.plan.update.request.v1.json`
  - response: `api.billing.plan.update.response.v1.json`
- `GET /v1/billing/plan?org_id=...&workspace_id=...`
  - response: `api.billing.plan.get.response.v1.json`
- `GET /v1/billing/invoices?org_id=...&workspace_id=...`
  - response: `api.billing.invoices.list.response.v1.json`
- `GET /v1/billing/invoices/{invoice_id}`
  - response: `api.billing.invoices.get.response.v1.json`

## Track F Phase 3 Naming, Routing, Transports, Deliveries Families (Draft Contracts)

### Files

- `schemas/public_api/api.principals.create.request.v1.json`
- `schemas/public_api/api.principals.create.response.v1.json`
- `schemas/public_api/api.principals.get.response.v1.json`
- `schemas/public_api/api.aliases.bind.request.v1.json`
- `schemas/public_api/api.aliases.bind.response.v1.json`
- `schemas/public_api/api.aliases.list.response.v1.json`
- `schemas/public_api/api.aliases.revoke.response.v1.json`
- `schemas/public_api/api.aliases.resolve.response.v1.json`
- `schemas/public_api/api.routing.endpoints.register.request.v1.json`
- `schemas/public_api/api.routing.endpoints.register.response.v1.json`
- `schemas/public_api/api.routing.endpoints.list.response.v1.json`
- `schemas/public_api/api.routing.endpoints.update.request.v1.json`
- `schemas/public_api/api.routing.endpoints.update.response.v1.json`
- `schemas/public_api/api.routing.endpoints.remove.response.v1.json`
- `schemas/public_api/api.routing.resolve.request.v1.json`
- `schemas/public_api/api.routing.resolve.response.v1.json`
- `schemas/public_api/api.transports.bindings.upsert.request.v1.json`
- `schemas/public_api/api.transports.bindings.upsert.response.v1.json`
- `schemas/public_api/api.transports.bindings.list.response.v1.json`
- `schemas/public_api/api.transports.bindings.remove.response.v1.json`
- `schemas/public_api/api.deliveries.submit.request.v1.json`
- `schemas/public_api/api.deliveries.submit.response.v1.json`
- `schemas/public_api/api.deliveries.list.response.v1.json`
- `schemas/public_api/api.deliveries.get.response.v1.json`
- `schemas/public_api/api.deliveries.replay.response.v1.json`

### Planned Endpoint Mapping

- `POST /v1/principals`
  - request: `api.principals.create.request.v1.json`
  - response: `api.principals.create.response.v1.json`
- `GET /v1/principals/{principal_id}`
  - response: `api.principals.get.response.v1.json`
- `POST /v1/aliases`
  - request: `api.aliases.bind.request.v1.json`
  - response: `api.aliases.bind.response.v1.json`
- `GET /v1/aliases`
  - response: `api.aliases.list.response.v1.json`
- `POST /v1/aliases/{alias_id}/revoke`
  - response: `api.aliases.revoke.response.v1.json`
- `GET /v1/aliases/resolve?org_id=...&workspace_id=...&alias=...`
  - response: `api.aliases.resolve.response.v1.json`
- `POST /v1/routing/endpoints`
  - request: `api.routing.endpoints.register.request.v1.json`
  - response: `api.routing.endpoints.register.response.v1.json`
- `GET /v1/routing/endpoints`
  - response: `api.routing.endpoints.list.response.v1.json`
- `PATCH /v1/routing/endpoints/{route_id}`
  - request: `api.routing.endpoints.update.request.v1.json`
  - response: `api.routing.endpoints.update.response.v1.json`
- `DELETE /v1/routing/endpoints/{route_id}`
  - response: `api.routing.endpoints.remove.response.v1.json`
- `POST /v1/routing/resolve`
  - request: `api.routing.resolve.request.v1.json`
  - response: `api.routing.resolve.response.v1.json`
- `POST /v1/transports/bindings`
  - request: `api.transports.bindings.upsert.request.v1.json`
  - response: `api.transports.bindings.upsert.response.v1.json`
- `GET /v1/transports/bindings`
  - response: `api.transports.bindings.list.response.v1.json`
- `DELETE /v1/transports/bindings/{binding_id}`
  - response: `api.transports.bindings.remove.response.v1.json`
- `POST /v1/deliveries`
  - request: `api.deliveries.submit.request.v1.json`
  - response: `api.deliveries.submit.response.v1.json`
- `GET /v1/deliveries`
  - response: `api.deliveries.list.response.v1.json`
- `GET /v1/deliveries/{delivery_id}`
  - response: `api.deliveries.get.response.v1.json`
- `POST /v1/deliveries/{delivery_id}/replay`
  - response: `api.deliveries.replay.response.v1.json`
