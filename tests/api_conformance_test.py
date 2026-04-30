#!/usr/bin/env python3
import argparse
import sys

import requests


SUCCESS_OR_AUTH_OR_NOT_FOUND = {200, 401, 404}
SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED = {200, 401, 404, 501}
SUCCESS_OR_AUTH_OR_NOT_IMPLEMENTED = {200, 401, 501}


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


def test_get_metadata(base_url, headers):
    """
    Tests GET /metadata.
    Optional query param: egf_did.
    On 200, verifies fields required by TrustRegistryMetadata.
    """
    print("\n=== Test: GET /metadata ===")
    url = f"{base_url}/metadata"
    params = {
        # "egf_did": "did:example:egf"  # optional
    }
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            data = resp.json()
            return validate_required_fields(
                data,
                ["ecosystem_did", "description"],
                "metadata response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_get_entity_information(base_url, headers, entity_id):
    """
    Tests GET /entities/{entity_id}.
    Checks status (200, 401, 404, 501).
    On 200, expects a JSON object describing the entity.
    """
    print("\n=== Test: GET /entities/{entity_id} ===")
    url = f"{base_url}/entities/{entity_id}"
    print(f"--> Testing GET {url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200 and not isinstance(resp.json(), dict):
            print("    Expected a JSON object for entity info.")
            return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_query_authorization(base_url, headers):
    """
    Tests POST /authorization.
    Request body follows TrqpAuthorizationQuery.
    On 200, response follows TrqpAuthorizationResponse required fields.
    """
    print("\n=== Test: POST /authorization ===")
    url = f"{base_url}/authorization"
    payload = {
        "entity_id": "did:example:entity123",
        "authority_id": "did:example:ecosystem",
        "action": "issue",
        "resource": "credential",
        # "context": {"time": "2025-01-01T12:00:00Z"},
    }
    print(f"--> Testing POST {url} with json={payload}")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            data = resp.json()
            return validate_required_fields(
                data,
                [
                    "entity_id",
                    "authority_id",
                    "action",
                    "resource",
                    "time_evaluated",
                    "authorized",
                ],
                "authorization response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_query_recognition(base_url, headers):
    """
    Tests POST /recognition.
    Request body follows TrqpRecognitionQuery.
    On 200, response follows TrqpRecognitionResponse required fields.
    """
    print("\n=== Test: POST /recognition ===")
    url = f"{base_url}/recognition"
    payload = {
        "entity_id": "did:example:trust-registry",
        "authority_id": "did:example:ecosystem",
        "action": "recognize",
        "resource": "trust-registry",
        # "context": {"time": "2025-01-01T12:00:00Z"},
    }
    print(f"--> Testing POST {url} with json={payload}")
    try:
        resp = requests.post(url, headers=headers, json=payload)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            data = resp.json()
            return validate_required_fields(
                data,
                [
                    "entity_id",
                    "authority_id",
                    "action",
                    "resource",
                    "time_evaluated",
                    "recognized",
                ],
                "recognition response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_list_entity_authorizations(base_url, headers, entity_did):
    """
    Tests GET /entities/{entity_did}/authorizations.
    Optional query param: time.
    On 200, returns array of TrqpAuthorizationResponse objects.
    """
    print("\n=== Test: GET /entities/{entity_did}/authorizations ===")
    url = f"{base_url}/entities/{entity_did}/authorizations"
    params = {
        # "time": "2025-01-01T12:00:00Z"
    }
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            return validate_list_items(
                resp.json(),
                ["entity_id", "authority_id", "action", "resource", "time_evaluated", "authorized"],
                "entity authorizations response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_get_ecosystem_information(base_url, headers, ecosystem_did):
    """
    Tests GET /ecosystems/{ecosystem_did}.
    Checks status (200, 401, 404, 501).
    On 200, expects a JSON object describing the ecosystem.
    """
    print("\n=== Test: GET /ecosystems/{ecosystem_did} ===")
    url = f"{base_url}/ecosystems/{ecosystem_did}"
    print(f"--> Testing GET {url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200 and not isinstance(resp.json(), dict):
            print("    Expected a JSON object for ecosystem info.")
            return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_list_ecosystem_recognitions(base_url, headers, ecosystem_did):
    """
    Tests GET /ecosystems/{ecosystem_did}/recognitions.
    Optional query param: time.
    On 200, returns array of TrqpRecognitionResponse objects.
    """
    print("\n=== Test: GET /ecosystems/{ecosystem_did}/recognitions ===")
    url = f"{base_url}/ecosystems/{ecosystem_did}/recognitions"
    params = {
        # "time": "2025-01-01T12:00:00Z"
    }
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            return validate_list_items(
                resp.json(),
                ["entity_id", "authority_id", "action", "resource", "time_evaluated", "recognized"],
                "ecosystem recognitions response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_lookup_supported_assurance_levels(base_url, headers, ecosystem_did):
    """
    Tests GET /lookups/assuranceLevels.
    Optional query param: ecosystem_did.
    On 200, returns array of AssuranceLevelResponse objects.
    """
    print("\n=== Test: GET /lookups/assuranceLevels ===")
    url = f"{base_url}/lookups/assuranceLevels"
    params = {"ecosystem_did": ecosystem_did}
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            return validate_list_items(
                resp.json(),
                ["assurance_level", "description"],
                "assurance levels response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_lookup_authorizations(base_url, headers, ecosystem_did):
    """
    Tests GET /lookups/authorizations.
    Optional query param: ecosystem_did.
    On 200, returns array of Authorization objects.
    """
    print("\n=== Test: GET /lookups/authorizations ===")
    url = f"{base_url}/lookups/authorizations"
    params = {"ecosystem_did": ecosystem_did}
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            return validate_list_items(
                resp.json(),
                ["action", "resource"],
                "authorizations lookup response",
            )
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_lookup_supported_did_methods(base_url, headers, ecosystem_did):
    """
    Tests GET /lookups/didMethods.
    Optional query param: ecosystem_did.
    On 200, returns DIDMethodListType (array of DIDMethodType).
    """
    print("\n=== Test: GET /lookups/didMethods ===")
    url = f"{base_url}/lookups/didMethods"
    params = {"ecosystem_did": ecosystem_did}
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in SUCCESS_OR_AUTH_OR_NOT_FOUND_OR_NOT_IMPLEMENTED:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            return validate_list_items(resp.json(), ["identifier"], "DID methods response")
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def run_all_tests(base_url, bearer_token):
    """
    Runs all test functions for the TRQP Profile API.
    """
    headers = build_headers(bearer_token)

    # Provide dummy or example arguments for required path/query params.
    # Adjust these as needed for your environment.
    dummy_entity_did = "did:example:entity123"
    dummy_ecosystem_did = "did:example:ecosystem"

    tests = [
        ("test_get_metadata", test_get_metadata(base_url, headers)),
        (
            "test_get_entity_information",
            test_get_entity_information(base_url, headers, dummy_entity_did),
        ),
        ("test_query_authorization", test_query_authorization(base_url, headers)),
        ("test_query_recognition", test_query_recognition(base_url, headers)),
        (
            "test_list_entity_authorizations",
            test_list_entity_authorizations(base_url, headers, dummy_entity_did),
        ),
        (
            "test_get_ecosystem_information",
            test_get_ecosystem_information(base_url, headers, dummy_ecosystem_did),
        ),
        (
            "test_list_ecosystem_recognitions",
            test_list_ecosystem_recognitions(base_url, headers, dummy_ecosystem_did),
        ),
        (
            "test_lookup_supported_assurance_levels",
            test_lookup_supported_assurance_levels(base_url, headers, dummy_ecosystem_did),
        ),
        (
            "test_lookup_authorizations",
            test_lookup_authorizations(base_url, headers, dummy_ecosystem_did),
        ),
        (
            "test_lookup_supported_did_methods",
            test_lookup_supported_did_methods(base_url, headers, dummy_ecosystem_did),
        ),
    ]

    overall_success = True
    print("\n==================== Test Results ====================")
    for test_name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            overall_success = False

    print("=====================================================")
    if overall_success:
        print("ALL TESTS PASSED.")
        sys.exit(0)
    else:
        print("ONE OR MORE TESTS FAILED.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Ayra™ TRQP Profile API Test Script")
    parser.add_argument(
        "--base-url",
        required=True,
        help="The base URL of the TRQP-compliant Trust Registry API (e.g. https://example-trust-registry.com)",
    )
    parser.add_argument(
        "--bearer-token",
        required=False,
        default="",
        help="Bearer token for authorization (if required).",
    )
    args = parser.parse_args()

    run_all_tests(args.base_url.rstrip("/"), args.bearer_token)


if __name__ == "__main__":
    main()
