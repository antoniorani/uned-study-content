"""Validate UNED Study content repository."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "subject.schema.json"


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def semantic_checks(path: Path, data: dict) -> list[str]:
    errors: list[str] = []

    if "subjects" in path.parts and path.name == "subject.json":
        expected = path.parent.name
        if data.get("id") != expected:
            errors.append(
                f"id {data.get('id')!r} does not match folder {expected!r}"
            )

    topics = data.get("topics", [])
    topic_ids = [topic.get("id") for topic in topics if isinstance(topic, dict)]
    if len(topic_ids) != len(set(topic_ids)):
        errors.append("topic IDs must be unique")
    known_topics = set(topic_ids)

    items = data.get("items", [])
    item_ids = [item.get("id") for item in items if isinstance(item, dict)]
    if len(item_ids) != len(set(item_ids)):
        errors.append("item IDs must be unique")

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        if item.get("topic") not in known_topics:
            errors.append(
                f"items[{index}] references unknown topic {item.get('topic')!r}"
            )

        if data.get("type") == "test":
            answers = item.get("answers", [])
            answer_ids = [
                answer.get("id")
                for answer in answers
                if isinstance(answer, dict)
            ]
            if len(answer_ids) != len(set(answer_ids)):
                errors.append(
                    f"items[{index}] contains duplicate answer IDs"
                )
            if item.get("correct_answer") not in set(answer_ids):
                errors.append(
                    f"items[{index}].correct_answer is not an answer ID"
                )

    return errors


def validate_file(
    validator: Draft202012Validator, path: Path
) -> list[str]:
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid JSON: {exc}"]

    errors = [
        error.message
        for error in sorted(
            validator.iter_errors(data),
            key=lambda error: list(error.absolute_path),
        )
    ]
    if isinstance(data, dict):
        errors.extend(semantic_checks(path, data))
    return errors


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    files = sorted((ROOT / "subjects").glob("*/subject.json"))
    files += sorted((ROOT / "examples").glob("*.json"))

    failed = False
    for path in files:
        errors = validate_file(validator, path)
        relative = path.relative_to(ROOT)
        if errors:
            failed = True
            print(f"ERROR: {relative}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK: {relative}")

    if not files:
        print("No subject or example files found.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
