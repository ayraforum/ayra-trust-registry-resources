#!/usr/bin/env python3
"""Ayra TRQP profile smoke test.

This script is intentionally small. It checks that a Trust Registry exposes the
current Ayra profile surface for a quick implementer sanity check. It is not the
Ayra Conformance Test Suite and should not be used to certify advanced protocol,
credential, or interoperability behavior.
"""

import argparse
import sys

import requests


CORE_EXPECTED_STATUSES = {200, 400, 401, 404}
OPTIONAL_EXPECTED_STATUSES = {200, 401, 404, 501}


def build_headers(bearer_token):
    headers = {"Accept": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers


def validate_required_fields(data, required_fields, response_name):
    if not isinstance(data, dict):
        print(f"    Expected JSON object for {response_name}.")
        return False
    for field in required_fields:
        if field not in data:
            print(f"    Missing '{field}' in {response_name}.")
            return False
    return True


def validate_list_items(data, required_fields, response_name):
    if not isinstance(data, list):
        print(f"    Expected a list for {response_name}.")
        return False
    for item in data:
        if not validate_required_fields(item, required_fields, response_name):
            return False
    return True


def request_json(method, url, headers, expected_statuses, **kwargs):
    print(f"--> Testing {method.upper()} {url}")
    if kwargs.get("params"):
        print(f"    params={kwargs['params']}")
    if kwargs.get("json"):
        print(f"    json={kwargs['json']}")

    response = requests.request(method, url, headers=headers, timeout=15, **kwargs)
    print(f"    Status: {response.status_code}")

    if response.status_code not in expected_statuses:
        print("    Unexpected status code.")
        return False, None
    if response.status_code == 200:
        try:
            return True, response.json()
        except ValueError as ex:
            print(f"    Expected JSON response: {ex}")
            return False, None
    return True, None


def smoke_get_metadata(base_url, headers):
    """GET /metadata should be reachable or explicitly unavailable."""
    print("\n=== Smoke: GET /metadata ===")
    ok, data = request_json(
        "get",
        f"{base_url}/metadata",
        headers,
        OPTIONAL_EXPECTED_STATUSES,
    )
    if not ok or data is None:
        return ok
    return validate_required_fields(data, ["ecosystem_did", "description"], "metadata response")


def smoke_post_authorization(base_url, headers, entity_id, authority_id, action, resource):
    """POST /authorization should accept the current TrqpAuthorizationQuery shape."""
    print("\n=== Smoke: POST /authorization ===")
    payload = {
        "entity_id": entity_id,
        "authority_id": authority_id,
        "action": action,
        "resource": resource,
        "context": {},
    }
    ok, data = request_json(
        "post",
        f"{base_url}/authorization",
        {**headers, "Content-Type": "application/json"},
        CORE_EXPECTED_STATUSES,
        json=payload,
    )
    if not ok or data is None:
        return ok
    return validate_required_fields(
        data,
        ["entity_id", "authority_id", "action", "resource", "time_evaluated", "authorized"],
        "authorization response",
    )


def smoke_post_recognition(base_url, headers, entity_id, authority_id, action, resource):
    """POST /recognition should accept the current TrqpRecognitionQuery shape."""
    print("\n=== Smoke: POST /recognition ===")
    payload = {
        "entity_id": entity_id,
        "authority_id": authority_id,
        "action": action,
        "resource": resource,
        "context": {},
    }
    ok, data = request_json(
        "post",
        f"{base_url}/recognition",
        {**headers, "Content-Type": "application/json"},
        CORE_EXPECTED_STATUSES,
        json=payload,
    )
    if not ok or data is None:
        return ok
    return validate_required_fields(
        data,
        ["entity_id", "authority_id", "action", "resource", "time_evaluated", "recognized"],
        "recognition response",
    )


def smoke_lookup_assurance_levels(base_url, headers, ecosystem_did):
    """GET /lookups/assuranceLevels should use the top-level Ayra profile path."""
    print("\n=== Smoke: GET /lookups/assuranceLevels ===")
    ok, data = request_json(
        "get",
        f"{base_url}/lookups/assuranceLevels",
        headers,
        OPTIONAL_EXPECTED_STATUSES,
        params={"ecosystem_did": ecosystem_did},
    )
    if not ok or data is None:
        return ok
    return validate_list_items(data, ["assurance_level", "description"], "assurance levels response")


def smoke_lookup_authorizations(base_url, headers, ecosystem_did):
    """GET /lookups/authorizations should use the top-level Ayra profile path."""
    print("\n=== Smoke: GET /lookups/authorizations ===")
    ok, data = request_json(
        "get",
        f"{base_url}/lookups/authorizations",
        headers,
        OPTIONAL_EXPECTED_STATUSES,
        params={"ecosystem_did": ecosystem_did},
    )
    if not ok or data is None:
        return ok
    return validate_list_items(data, ["action", "resource"], "authorizations lookup response")


def smoke_list_entities(base_url, headers, ecosystem_did):
    """GET /entities should list entities or signal non-support (optional endpoint)."""
    print("\n=== Smoke: GET /entities ===")
    ok, data = request_json(
        "get",
        f"{base_url}/entities",
        headers,
        OPTIONAL_EXPECTED_STATUSES,
        params={"ecosystem_did": ecosystem_did, "limit": 10},
    )
    if not ok or data is None:
        return ok
    if not validate_required_fields(data, ["items", "pagination"], "entities list response"):
        return False
    return validate_list_items(data["items"], ["entity_id"], "entities list items")


def smoke_lookup_did_methods(base_url, headers, ecosystem_did):
    """GET /lookups/didMethods should use the top-level Ayra profile path."""
    print("\n=== Smoke: GET /lookups/didMethods ===")
    ok, data = request_json(
        "get",
        f"{base_url}/lookups/didMethods",
        headers,
        OPTIONAL_EXPECTED_STATUSES,
        params={"ecosystem_did": ecosystem_did},
    )
    if not ok or data is None:
        return ok
    return validate_list_items(data, ["identifier"], "DID methods response")


def run_smoke_tests(args):
    """Runs quick Ayra TRQP profile smoke checks."""
    base_url = args.base_url.rstrip("/")
    headers = build_headers(args.bearer_token)

    checks = [
        ("GET /metadata", smoke_get_metadata(base_url, headers)),
        (
            "POST /authorization",
            smoke_post_authorization(
                base_url,
                headers,
                args.entity_id,
                args.authority_id,
                args.authorization_action,
                args.authorization_resource,
            ),
        ),
        (
            "POST /recognition",
            smoke_post_recognition(
                base_url,
                headers,
                args.recognition_entity_id,
                args.authority_id,
                args.recognition_action,
                args.recognition_resource,
            ),
        ),
        (
            "GET /lookups/assuranceLevels",
            smoke_lookup_assurance_levels(base_url, headers, args.ecosystem_did),
        ),
        (
            "GET /lookups/authorizations",
            smoke_lookup_authorizations(base_url, headers, args.ecosystem_did),
        ),
        (
            "GET /lookups/didMethods",
            smoke_lookup_did_methods(base_url, headers, args.ecosystem_did),
        ),
        (
            "GET /entities",
            smoke_list_entities(base_url, headers, args.ecosystem_did),
        ),
    ]

    overall_success = True
    print("\n==================== Smoke Test Results ====================")
    for check_name, result in checks:
        status = "PASS" if result else "FAIL"
        print(f"{check_name}: {status}")
        overall_success = overall_success and result

    print("============================================================")
    if overall_success:
        print("SMOKE TESTS PASSED.")
        return 0

    print("ONE OR MORE SMOKE TESTS FAILED.")
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Ayra TRQP Profile smoke test. Use the full Ayra CTS for conformance certification."
    )
    parser.add_argument(
        "--base-url",
        required=True,
        help="Base URL of the Trust Registry API (for example, https://example-trust-registry.com)",
    )
    parser.add_argument(
        "--bearer-token",
        default="",
        help="Bearer token for registries that require authorization.",
    )
    parser.add_argument("--entity-id", default="did:example:entity123", help="Entity ID for /authorization.")
    parser.add_argument(
        "--recognition-entity-id",
        default="did:example:trust-registry",
        help="Entity/registry ID for /recognition.",
    )
    parser.add_argument(
        "--authority-id",
        default="did:example:ecosystem",
        help="Authority/ecosystem ID for TRQP core queries.",
    )
    parser.add_argument(
        "--ecosystem-did",
        default="did:example:ecosystem",
        help="Ecosystem DID used for lookup query parameters.",
    )
    parser.add_argument("--authorization-action", default="issue", help="Action for /authorization.")
    parser.add_argument("--authorization-resource", default="credential", help="Resource for /authorization.")
    parser.add_argument("--recognition-action", default="recognize", help="Action for /recognition.")
    parser.add_argument("--recognition-resource", default="trust-registry", help="Resource for /recognition.")
    args = parser.parse_args()

    sys.exit(run_smoke_tests(args))


if __name__ == "__main__":
    main()
