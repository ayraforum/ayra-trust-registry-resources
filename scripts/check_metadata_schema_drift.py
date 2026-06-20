#!/usr/bin/env python3
"""Check Ayra metadata JSON Schema matches OpenAPI TrustRegistryMetadata.

This deliberately uses only the Python standard library so the check can run in
CI before optional tooling is installed. It extracts the small OpenAPI component
surface this repository owns (required fields, property names, and
additionalProperties) and compares it with schema/ayra_metadata.jsonschema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_SCHEMA_PATH = ROOT / "schema" / "ayra_metadata.jsonschema"
OPENAPI_PATH = ROOT / "trqp_ayra_profile_swagger.yaml"
COMPONENT_NAME = "TrustRegistryMetadata"


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _component_lines(openapi_text: str) -> tuple[int, list[str]]:
    lines = openapi_text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == f"{COMPONENT_NAME}:":
            component_indent = _indent(line)
            block: list[str] = []
            for child in lines[index + 1 :]:
                if child.strip() and _indent(child) <= component_indent:
                    break
                block.append(child)
            return component_indent, block
    raise SystemExit(f"Could not find components.schemas.{COMPONENT_NAME} in {OPENAPI_PATH}")


def _extract_required(block: list[str]) -> list[str]:
    required: list[str] = []
    in_required = False
    required_indent = 0
    for line in block:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "required:":
            in_required = True
            required_indent = _indent(line)
            continue
        if in_required:
            if _indent(line) <= required_indent:
                break
            if stripped.startswith("-"):
                required.append(stripped[1:].strip())
    return required


def _extract_properties(block: list[str]) -> set[str]:
    properties: set[str] = set()
    in_properties = False
    properties_indent = 0
    property_indent = 0
    for line in block:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == "properties:":
            in_properties = True
            properties_indent = _indent(line)
            property_indent = properties_indent + 2
            continue
        if in_properties:
            if _indent(line) <= properties_indent:
                break
            if _indent(line) == property_indent and stripped.endswith(":"):
                properties.add(stripped[:-1])
    return properties


def _extract_additional_properties(block: list[str]) -> bool | None:
    properties_indent = None
    for line in block:
        stripped = line.strip()
        if stripped == "properties:":
            properties_indent = _indent(line)
        if stripped.startswith("additionalProperties:"):
            # Only accept schema-level additionalProperties, not a mistaken
            # property named additionalProperties inside properties.
            if properties_indent is None or _indent(line) <= properties_indent:
                value = stripped.split(":", 1)[1].strip().lower()
                if value == "false":
                    return False
                if value == "true":
                    return True
                return None
    return None


def load_openapi_metadata_contract() -> dict[str, object]:
    _, block = _component_lines(OPENAPI_PATH.read_text(encoding="utf-8"))
    return {
        "required": _extract_required(block),
        "properties": _extract_properties(block),
        "additionalProperties": _extract_additional_properties(block),
    }


def load_json_schema_metadata_contract() -> dict[str, object]:
    schema = json.loads(JSON_SCHEMA_PATH.read_text(encoding="utf-8"))
    return {
        "required": schema.get("required", []),
        "properties": set(schema.get("properties", {}).keys()),
        "additionalProperties": schema.get("additionalProperties"),
    }


def main() -> int:
    json_contract = load_json_schema_metadata_contract()
    openapi_contract = load_openapi_metadata_contract()

    failures: list[str] = []
    if set(json_contract["required"]) != set(openapi_contract["required"]):
        failures.append(
            "required fields differ: "
            f"jsonschema={sorted(json_contract['required'])} "
            f"openapi={sorted(openapi_contract['required'])}"
        )
    if json_contract["properties"] != openapi_contract["properties"]:
        failures.append(
            "properties differ: "
            f"jsonschema={sorted(json_contract['properties'])} "
            f"openapi={sorted(openapi_contract['properties'])}"
        )
    if json_contract["additionalProperties"] != openapi_contract["additionalProperties"]:
        failures.append(
            "additionalProperties differs: "
            f"jsonschema={json_contract['additionalProperties']} "
            f"openapi={openapi_contract['additionalProperties']}"
        )

    if failures:
        print("Ayra metadata schema drift detected:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Ayra metadata JSON Schema matches OpenAPI TrustRegistryMetadata.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
