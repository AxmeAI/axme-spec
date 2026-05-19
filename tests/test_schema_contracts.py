"""
Schema contract tests for AXME protocol and public API schemas.

Covers all changes introduced in the PARTICIPANT_MODEL / DURABLE_WORKFLOW /
B2B_CORE_V2 updates:
  - TIMED_OUT status in lifecycle and event schemas
  - New event types (timed_out, reminder, escalated, delivery_failed, human_task_assigned)
  - from_agent optional in create request + durability fields
  - agent address schemas
  - runtime_type on WorkflowStepSpec
  - HumanTaskSpec enrichment (task_type, allowed_outcomes, assignees, etc.)
  - api.tasks.list response schema
  - service_account create response has agent_address
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "schemas" / "protocol"
PUBLIC_API = ROOT / "schemas" / "public_api"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def statuses_in(schema: dict, path: list[str]) -> list[str]:
    """Navigate nested dict by key path and return the 'enum' list."""
    node = schema
    for key in path:
        node = node[key]
    return node["enum"]


def collect_enum(schema: dict, *path: str) -> list[str]:
    node = schema
    for key in path:
        node = node[key]
    return node


# ---------------------------------------------------------------------------
# Group 1: intent.lifecycle.v1 — TIMED_OUT status
# ---------------------------------------------------------------------------

class TestIntentLifecycle:
    schema = load(PROTOCOL / "intent.lifecycle.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/protocol/intent.lifecycle.v1.json"

    def test_timed_out_in_status_enum(self):
        statuses = self.schema["properties"]["status"]["enum"]
        assert "TIMED_OUT" in statuses

    def test_all_expected_statuses_present(self):
        expected = {
            "CREATED", "SUBMITTED", "DELIVERED", "ACKNOWLEDGED",
            "IN_PROGRESS", "WAITING", "COMPLETED", "FAILED", "CANCELED", "TIMED_OUT"
        }
        statuses = set(self.schema["properties"]["status"]["enum"])
        assert expected == statuses

    def test_waiting_reason_enum_unchanged(self):
        reasons = self.schema["properties"]["waiting_reason"]["enum"]
        assert "WAITING_FOR_HUMAN" in reasons
        assert "WAITING_FOR_TOOL" in reasons
        assert "WAITING_FOR_AGENT" in reasons
        assert "WAITING_FOR_TIME" in reasons

    def test_required_fields_present(self):
        required = self.schema["required"]
        for field in ["intent_id", "correlation_id", "status", "seq", "created_at", "updated_at"]:
            assert field in required

    def test_allOf_waiting_requires_waiting_reason(self):
        all_of = self.schema["allOf"]
        assert len(all_of) >= 1
        rule = all_of[0]
        assert rule["if"]["properties"]["status"]["const"] == "WAITING"
        assert "waiting_reason" in rule["then"]["required"]


# ---------------------------------------------------------------------------
# Group 2: intent.event.v1 — new event_type values + TIMED_OUT status
# ---------------------------------------------------------------------------

class TestIntentEvent:
    schema = load(PROTOCOL / "intent.event.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/protocol/intent.event.v1.json"

    def test_timed_out_in_status_enum(self):
        statuses = self.schema["properties"]["status"]["enum"]
        assert "TIMED_OUT" in statuses

    def test_new_event_types_present(self):
        event_types = self.schema["properties"]["event_type"]["enum"]
        for et in ["intent.timed_out", "intent.reminder", "intent.escalated",
                   "intent.delivery_failed", "intent.human_task_assigned"]:
            assert et in event_types, f"Missing event_type: {et}"

    def test_legacy_event_types_preserved(self):
        event_types = self.schema["properties"]["event_type"]["enum"]
        for et in ["intent.created", "intent.submitted", "intent.delivered",
                   "intent.acknowledged", "intent.in_progress", "intent.waiting",
                   "intent.completed", "intent.failed", "intent.canceled",
                   "intent.transfer", "intent.timeout"]:
            assert et in event_types, f"Missing legacy event_type: {et}"

    def test_all_expected_statuses_present(self):
        expected = {
            "CREATED", "SUBMITTED", "DELIVERED", "ACKNOWLEDGED",
            "IN_PROGRESS", "WAITING", "COMPLETED", "FAILED", "CANCELED", "TIMED_OUT"
        }
        assert expected == set(self.schema["properties"]["status"]["enum"])

    def test_required_fields(self):
        required = self.schema["required"]
        for field in ["intent_id", "seq", "event_type", "status", "at"]:
            assert field in required

    def test_allOf_waiting_requires_waiting_reason(self):
        all_of = self.schema["allOf"]
        rule = all_of[0]
        assert rule["if"]["properties"]["status"]["const"] == "WAITING"
        assert "waiting_reason" in rule["then"]["required"]


# ---------------------------------------------------------------------------
# Group 3: api.intents.create.request — from_agent optional + durability fields
# ---------------------------------------------------------------------------

class TestIntentsCreateRequest:
    schema = load(PUBLIC_API / "api.intents.create.request.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/public_api/api.intents.create.request.v1.json"

    def test_from_agent_not_required(self):
        assert "from_agent" not in self.schema["required"]

    def test_to_agent_still_required(self):
        assert "to_agent" in self.schema["required"]

    def test_intent_type_still_required(self):
        assert "intent_type" in self.schema["required"]

    def test_payload_still_required(self):
        assert "payload" in self.schema["required"]

    def test_from_agent_field_still_present(self):
        # backwards compat — field accepted but deprecated
        assert "from_agent" in self.schema["properties"]

    def test_durability_fields_present(self):
        props = self.schema["properties"]
        for field in ["deadline_at", "remind_after_seconds", "remind_interval_seconds",
                      "max_reminders", "escalate_to", "max_delivery_attempts"]:
            assert field in props, f"Missing field: {field}"

    def test_deadline_at_is_datetime(self):
        assert self.schema["properties"]["deadline_at"]["format"] == "date-time"

    def test_remind_after_seconds_is_positive_int(self):
        prop = self.schema["properties"]["remind_after_seconds"]
        assert prop["type"] == "integer"
        assert prop["minimum"] == 1

    def test_max_delivery_attempts_is_positive_int(self):
        prop = self.schema["properties"]["max_delivery_attempts"]
        assert prop["type"] == "integer"
        assert prop["minimum"] == 1

    def test_human_task_field_present(self):
        assert "human_task" in self.schema["properties"]

    def test_defs_has_human_task_spec(self):
        assert "HumanTaskSpec" in self.schema.get("$defs", {})

    def test_human_task_spec_has_task_type(self):
        spec = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "task_type" in spec
        assert spec["task_type"]["type"] == "string"
        assert "approval" in spec["task_type"]["enum"]

    def test_human_task_spec_task_type_includes_v1_priorities(self):
        task_types = self.schema["$defs"]["HumanTaskSpec"]["properties"]["task_type"]["enum"]
        for t in ["approval", "review", "clarification", "manual_action", "confirmation",
                  "assignment", "override"]:
            assert t in task_types, f"Missing v1 priority task type: {t}"

    def test_human_task_spec_has_allowed_outcomes(self):
        spec = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "allowed_outcomes" in spec
        assert spec["allowed_outcomes"]["type"] == "array"

    def test_human_task_spec_has_required_comment(self):
        spec = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "required_comment" in spec
        assert spec["required_comment"]["type"] == "boolean"

    def test_human_task_spec_has_assignees(self):
        spec = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "assignees" in spec
        assert spec["assignees"]["type"] == "array"

    def test_human_task_spec_has_evidence_required(self):
        spec = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "evidence_required" in spec
        assert spec["evidence_required"]["type"] == "boolean"


# ---------------------------------------------------------------------------
# Group 4: api.intents.create.response — TIMED_OUT in status
# ---------------------------------------------------------------------------

class TestIntentsCreateResponse:
    schema = load(PUBLIC_API / "api.intents.create.response.v1.json")

    def test_timed_out_in_status_enum(self):
        statuses = self.schema["properties"]["status"]["enum"]
        assert "TIMED_OUT" in statuses


# ---------------------------------------------------------------------------
# Group 5: api.intents.get.response — TIMED_OUT + durability + pending_with
# ---------------------------------------------------------------------------

class TestIntentsGetResponse:
    schema = load(PUBLIC_API / "api.intents.get.response.v1.json")

    def test_timed_out_in_status_enum(self):
        statuses = self.schema["properties"]["intent"]["properties"]["status"]["enum"]
        assert "TIMED_OUT" in statuses

    def test_durability_fields_in_intent(self):
        intent_props = self.schema["properties"]["intent"]["properties"]
        for field in ["deadline_at", "remind_after_seconds", "remind_interval_seconds",
                      "max_reminders", "remind_count", "escalate_to",
                      "max_delivery_attempts", "delivery_attempt", "human_task"]:
            assert field in intent_props, f"Missing intent response field: {field}"

    def test_pending_with_field_present(self):
        intent_props = self.schema["properties"]["intent"]["properties"]
        assert "pending_with" in intent_props

    def test_pending_with_has_type_enum(self):
        pw = self.schema["properties"]["intent"]["properties"]["pending_with"]
        assert "type" in pw["properties"]
        assert set(pw["properties"]["type"]["enum"]) == {"agent", "human", "internal"}


# ---------------------------------------------------------------------------
# Group 6: api.agents.list.response — new schema
# ---------------------------------------------------------------------------

class TestAgentsListResponse:
    schema = load(PUBLIC_API / "api.agents.list.response.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/public_api/api.agents.list.response.v1.json"

    def test_required_top_level_fields(self):
        assert "ok" in self.schema["required"]
        assert "agents" in self.schema["required"]

    def test_agents_is_array(self):
        assert self.schema["properties"]["agents"]["type"] == "array"

    def test_agent_entry_required_fields(self):
        entry = self.schema["$defs"]["AgentEntry"]
        for field in ["address", "service_account_id", "service_account_name", "status", "created_at"]:
            assert field in entry["required"], f"Missing required field in AgentEntry: {field}"

    def test_agent_entry_status_enum(self):
        status_enum = self.schema["$defs"]["AgentEntry"]["properties"]["status"]["enum"]
        assert set(status_enum) == {"active", "suspended", "deleted"}

    def test_agent_entry_display_name_nullable(self):
        dn = self.schema["$defs"]["AgentEntry"]["properties"]["display_name"]
        assert "null" in dn["type"]

    def test_address_has_min_length(self):
        addr = self.schema["$defs"]["AgentEntry"]["properties"]["address"]
        assert addr.get("minLength", 0) >= 10


# ---------------------------------------------------------------------------
# Group 7: api.agents.get.response — new schema
# ---------------------------------------------------------------------------

class TestAgentsGetResponse:
    schema = load(PUBLIC_API / "api.agents.get.response.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/public_api/api.agents.get.response.v1.json"

    def test_required_top_level_fields(self):
        assert "ok" in self.schema["required"]
        assert "agent" in self.schema["required"]

    def test_agent_required_fields(self):
        agent = self.schema["properties"]["agent"]
        for field in ["address", "service_account_id", "service_account_name", "status", "created_at"]:
            assert field in agent["required"], f"Missing required field in agent: {field}"

    def test_agent_has_updated_at(self):
        # get response has updated_at, list does not
        agent_props = self.schema["properties"]["agent"]["properties"]
        assert "updated_at" in agent_props

    def test_address_format_documented(self):
        desc = self.schema["properties"]["agent"]["properties"]["address"].get("description", "")
        assert "agent://" in desc


# ---------------------------------------------------------------------------
# Group 8: api.scenarios.bundle.request — runtime_type + HumanTaskSpec enrichment
# ---------------------------------------------------------------------------

class TestScenariosBundleRequest:
    schema = load(PUBLIC_API / "api.scenarios.bundle.request.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/public_api/api.scenarios.bundle.request.v1.json"

    def test_workflow_step_tool_id_not_required(self):
        step = self.schema["$defs"]["WorkflowStepSpec"]
        assert "tool_id" not in step["required"]

    def test_workflow_step_step_id_required(self):
        step = self.schema["$defs"]["WorkflowStepSpec"]
        assert "step_id" in step["required"]

    def test_runtime_type_field_present(self):
        step_props = self.schema["$defs"]["WorkflowStepSpec"]["properties"]
        assert "runtime_type" in step_props

    def test_runtime_type_enum_values(self):
        rt_enum = self.schema["$defs"]["WorkflowStepSpec"]["properties"]["runtime_type"]["enum"]
        expected = {"human_approval", "timeout", "reminder", "delay", "escalation", "notification"}
        assert expected == set(rt_enum)

    def test_runtime_config_field_present(self):
        step_props = self.schema["$defs"]["WorkflowStepSpec"]["properties"]
        assert "runtime_config" in step_props

    def test_human_task_spec_has_task_type(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "task_type" in ht

    def test_task_type_enum_v1_priorities(self):
        task_type_enum = self.schema["$defs"]["HumanTaskSpec"]["properties"]["task_type"]["enum"]
        for t in ["approval", "review", "clarification", "manual_action",
                  "confirmation", "assignment", "override"]:
            assert t in task_type_enum, f"Missing v1 priority task_type: {t}"

    def test_allowed_outcomes_field(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "allowed_outcomes" in ht
        assert ht["allowed_outcomes"]["type"] == "array"

    def test_required_comment_field(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "required_comment" in ht
        assert ht["required_comment"]["type"] == "boolean"

    def test_assignees_field(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "assignees" in ht
        assert ht["assignees"]["type"] == "array"

    def test_evidence_required_field(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "evidence_required" in ht
        assert ht["evidence_required"]["type"] == "boolean"

    def test_humans_spec_present(self):
        # humans[] in bundle top-level
        assert "humans" in self.schema["properties"]

    def test_human_spec_required_fields(self):
        hs = self.schema["$defs"]["HumanSpec"]
        assert "role" in hs["required"]
        assert "contact" in hs["required"]


# ---------------------------------------------------------------------------
# Group 9: api.tasks.list.response — new schema
# ---------------------------------------------------------------------------

class TestTasksListResponse:
    schema = load(PUBLIC_API / "api.tasks.list.response.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/public_api/api.tasks.list.response.v1.json"

    def test_required_top_level_fields(self):
        assert "ok" in self.schema["required"]
        assert "tasks" in self.schema["required"]

    def test_tasks_is_array(self):
        assert self.schema["properties"]["tasks"]["type"] == "array"

    def test_task_item_required_fields(self):
        item = self.schema["$defs"]["HumanTaskItem"]
        for field in ["intent_id", "intent_type", "status", "assigned_at", "human_task"]:
            assert field in item["required"], f"Missing required field in HumanTaskItem: {field}"

    def test_task_item_status_only_waiting(self):
        status = self.schema["$defs"]["HumanTaskItem"]["properties"]["status"]
        assert status["enum"] == ["WAITING"]

    def test_task_item_intent_id_is_uuid(self):
        intent_id = self.schema["$defs"]["HumanTaskItem"]["properties"]["intent_id"]
        assert intent_id["format"] == "uuid"

    def test_task_item_due_at_is_datetime(self):
        due_at = self.schema["$defs"]["HumanTaskItem"]["properties"]["due_at"]
        assert due_at["format"] == "date-time"

    def test_task_item_has_human_task(self):
        item_props = self.schema["$defs"]["HumanTaskItem"]["properties"]
        assert "human_task" in item_props

    def test_human_task_spec_has_task_type(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "task_type" in ht

    def test_human_task_spec_has_allowed_outcomes(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "allowed_outcomes" in ht

    def test_human_task_spec_has_form_schema(self):
        ht = self.schema["$defs"]["HumanTaskSpec"]["properties"]
        assert "form_schema" in ht


# ---------------------------------------------------------------------------
# Group 10: api.service_accounts.create.response — agent_address + display_name
# ---------------------------------------------------------------------------

class TestServiceAccountsCreateResponse:
    schema = load(PUBLIC_API / "api.service_accounts.create.response.v1.json")

    def test_agent_address_field_present(self):
        sa_props = self.schema["properties"]["service_account"]["properties"]
        assert "agent_address" in sa_props

    def test_agent_address_has_description_with_scheme(self):
        desc = self.schema["properties"]["service_account"]["properties"]["agent_address"].get("description", "")
        assert "agent://" in desc

    def test_display_name_field_present(self):
        sa_props = self.schema["properties"]["service_account"]["properties"]
        assert "display_name" in sa_props

    def test_display_name_nullable(self):
        dn = self.schema["properties"]["service_account"]["properties"]["display_name"]
        assert "null" in dn["type"]

    def test_core_required_fields_unchanged(self):
        required = self.schema["properties"]["service_account"]["required"]
        for field in ["service_account_id", "org_id", "workspace_id", "name", "status", "created_at"]:
            assert field in required


# ---------------------------------------------------------------------------
# Group 11: schema uniqueness and $id integrity (meta)
# ---------------------------------------------------------------------------

class TestSchemaIntegrity:
    def test_all_schemas_have_unique_ids(self):
        ids: dict[str, Path] = {}
        for schema_path in sorted((ROOT / "schemas").rglob("*.json")):
            doc = json.loads(schema_path.read_text(encoding="utf-8"))
            schema_id = doc.get("$id")
            assert schema_id, f"Schema missing $id: {schema_path}"
            assert schema_id not in ids, (
                f"Duplicate $id={schema_id} in {schema_path} and {ids[schema_id]}"
            )
            ids[schema_id] = schema_path

    def test_new_schemas_exist(self):
        for name in [
            "api.agents.list.response.v1.json",
            "api.agents.get.response.v1.json",
            "api.tasks.list.response.v1.json",
        ]:
            assert (PUBLIC_API / name).exists(), f"Expected new schema file missing: {name}"

    def test_all_protocol_schemas_parseable(self):
        for schema_path in sorted(PROTOCOL.rglob("*.json")):
            doc = json.loads(schema_path.read_text(encoding="utf-8"))
            assert "$id" in doc

    def test_all_public_api_schemas_parseable(self):
        for schema_path in sorted(PUBLIC_API.rglob("*.json")):
            doc = json.loads(schema_path.read_text(encoding="utf-8"))
            assert "$id" in doc


# ---------------------------------------------------------------------------
# Group 12: Session protocol schemas (anti-messenger / D-030)
# ---------------------------------------------------------------------------

SESSION_STATUSES = {"OPEN", "WAITING_OWNER", "RESOLVED", "CLOSED", "PRUNED"}


class TestSessionLifecycle:
    schema = load(PROTOCOL / "session.lifecycle.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/protocol/session.lifecycle.v1.json"

    def test_status_enum_is_session_specific(self):
        assert set(self.schema["properties"]["status"]["enum"]) == SESSION_STATUSES

    def test_session_is_not_forward_only_like_intent(self):
        # D-031: Intent is forward-only with final terminals. Session is
        # bidirectional (RESOLVED -> OPEN on visitor return), so it must NOT
        # reuse the Intent lifecycle enum.
        statuses = set(self.schema["properties"]["status"]["enum"])
        for intent_terminal in ("COMPLETED", "FAILED", "CANCELED", "TIMED_OUT"):
            assert intent_terminal not in statuses

    def test_required_fields_present(self):
        required = self.schema["required"]
        for field in ["session_id", "correlation_id", "status", "seq", "created_at", "updated_at"]:
            assert field in required

    def test_additional_properties_false(self):
        assert self.schema["additionalProperties"] is False


class TestSessionEvent:
    schema = load(PROTOCOL / "session.event.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/protocol/session.event.v1.json"

    def test_event_types_present(self):
        event_types = set(self.schema["properties"]["event_type"]["enum"])
        for et in [
            "session.created", "session.message", "session.owner_intervened",
            "session.intent_spawned", "session.intent_resolved", "session.resolved",
            "session.reopened", "session.closed", "session.pruned",
        ]:
            assert et in event_types, f"Missing session event_type: {et}"

    def test_required_fields(self):
        for field in ["session_id", "seq", "event_type", "at"]:
            assert field in self.schema["required"]

    def test_intent_linkage_field_present(self):
        # session.intent_spawned / session.intent_resolved carry the spawned intent id
        assert "intent_id" in self.schema["properties"]


class TestSessionEnvelope:
    schema = load(PROTOCOL / "session.envelope.v1.json")

    def test_schema_has_correct_id(self):
        assert self.schema["$id"] == "https://axme.dev/schemas/protocol/session.envelope.v1.json"

    def test_version_const_v1(self):
        assert self.schema["properties"]["version"]["const"] == "v1"

    def test_required_fields(self):
        for field in ["version", "session_id", "correlation_id", "created_at", "owner_agent"]:
            assert field in self.schema["required"]


# ---------------------------------------------------------------------------
# Group 13: additive session_id linkage on existing intent/message schemas
# (must stay v1 — optional, never required)
# ---------------------------------------------------------------------------

class TestIntentSessionLinkageAdditive:
    lifecycle = load(PROTOCOL / "intent.lifecycle.v1.json")
    event = load(PROTOCOL / "intent.event.v1.json")
    envelope = load(PROTOCOL / "intent.envelope.v1.json")
    message_v3 = load(PROTOCOL / "message.envelope.v3.json")

    def test_lifecycle_session_id_optional(self):
        assert "session_id" in self.lifecycle["properties"]
        assert "parent_intent_id" in self.lifecycle["properties"]
        assert "session_id" not in self.lifecycle["required"]
        assert "parent_intent_id" not in self.lifecycle["required"]

    def test_lifecycle_status_enum_unchanged(self):
        # additive change must not touch the Intent status enum
        assert set(self.lifecycle["properties"]["status"]["enum"]) == {
            "CREATED", "SUBMITTED", "DELIVERED", "ACKNOWLEDGED", "IN_PROGRESS",
            "WAITING", "COMPLETED", "FAILED", "CANCELED", "TIMED_OUT",
        }

    def test_event_session_id_optional(self):
        assert "session_id" in self.event["properties"]
        assert "session_id" not in self.event["required"]

    def test_envelope_session_id_optional(self):
        assert "session_id" in self.envelope["properties"]
        assert "session_id" not in self.envelope["required"]

    def test_message_v3_session_id_optional_nullable(self):
        prop = self.message_v3["properties"]["session_id"]
        assert prop["type"] == ["string", "null"]
        assert "session_id" not in self.message_v3["required"]


# ---------------------------------------------------------------------------
# Group 14: Session public API schemas
# ---------------------------------------------------------------------------

class TestSessionPublicApi:
    create_req = load(PUBLIC_API / "api.sessions.create.request.v1.json")
    create_resp = load(PUBLIC_API / "api.sessions.create.response.v1.json")
    get_resp = load(PUBLIC_API / "api.sessions.get.response.v1.json")
    events_resp = load(PUBLIC_API / "api.sessions.events.list.response.v1.json")
    append_req = load(PUBLIC_API / "api.sessions.messages.append.request.v1.json")
    list_resp = load(PUBLIC_API / "api.sessions.list.response.v1.json")

    def test_ids_correct(self):
        base = "https://axme.dev/schemas/public_api/"
        assert self.create_req["$id"] == base + "api.sessions.create.request.v1.json"
        assert self.create_resp["$id"] == base + "api.sessions.create.response.v1.json"
        assert self.get_resp["$id"] == base + "api.sessions.get.response.v1.json"
        assert self.events_resp["$id"] == base + "api.sessions.events.list.response.v1.json"
        assert self.append_req["$id"] == base + "api.sessions.messages.append.request.v1.json"
        assert self.list_resp["$id"] == base + "api.sessions.list.response.v1.json"

    def test_create_request_required(self):
        assert set(self.create_req["required"]) == {"to_agent", "correlation_id"}

    def test_create_response_status_session_enum(self):
        assert set(self.create_resp["properties"]["status"]["enum"]) == SESSION_STATUSES
        assert set(self.create_resp["required"]) == {"ok", "session_id", "status", "created_at"}

    def test_get_response_shape(self):
        assert set(self.get_resp["required"]) == {"ok", "session"}

    def test_events_response_event_type_pattern(self):
        item = self.events_resp["properties"]["events"]["items"]
        assert item["properties"]["event_type"]["pattern"] == r"^session\.[a-z_]+$"
        assert set(item["required"]) == {"session_id", "seq", "event_type", "at"}

    def test_append_request_required_message(self):
        assert self.append_req["required"] == ["message"]

    def test_list_response_required(self):
        assert set(self.list_resp["required"]) == {"ok", "sessions"}
