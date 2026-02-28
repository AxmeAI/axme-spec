from __future__ import annotations

import json
from pathlib import Path


def load_schema_documents(root: Path) -> list[dict]:
    docs: list[dict] = []
    for schema_path in sorted((root / "schemas").rglob("*.json")):
        docs.append(json.loads(schema_path.read_text(encoding="utf-8")))
    return docs


def validate_schema_documents(root: Path) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    for schema_path in sorted((root / "schemas").rglob("*.json")):
        try:
            doc = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_path}: invalid json ({exc})")
            continue

        schema_id = doc.get("$id")
        if not schema_id:
            errors.append(f"{schema_path}: missing $id")
            continue
        if schema_id in ids:
            errors.append(f"{schema_path}: duplicate $id={schema_id}")
        ids.add(schema_id)

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_schema_documents(root)
    if errors:
        print("schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
