from __future__ import annotations

from pathlib import Path

from scripts.validate_schemas import validate_schema_documents


def test_schema_documents_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    errors = validate_schema_documents(root)
    assert errors == []
