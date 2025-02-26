#!/usr/bin/env python3
import argparse
import sys
import requests


def test_get_metadata(base_url, headers):
    """
    Tests the GET /metadata endpoint.
    Optional query param: egf_did.
    Checks for a 200, 401, or 404 status code.
    On 200, verifies JSON structure against 'TrustRegistryMetadata' basics.
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

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            # Basic structural check
            data = resp.json()
            if not isinstance(data, dict):
                print("    Expected JSON object for metadata.")
                return False
            # Check required fields from TrustRegistryMetadata
            for required_key in ["id", "description", "name", "controllers"]:
                if required_key not in data:
                    print(f"    Missing required key '{required_key}'.")
                    return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_get_entity_information(base_url, headers, entity_id):
    """
    Tests GET /entities/{entity_id}.
    Checks status (200, 401, 404).
    On 200, expects a JSON object describing the entity.
    """
    print("\n=== Test: GET /entities/{entity_id} ===")
    url = f"{base_url}/entities/{entity_id}"
    print(f"--> Testing GET {url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False
        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, dict):
                print("    Expected a JSON object for entity info.")
                return False
            # Optionally, check if it has at least some identifying field
            # (Spec only says it's a JSON object, so minimal check done.)
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_check_entity_authorization(base_url, headers, entity_id):
    """
    Tests GET /entities/{entity_id}/authorization.
    Required query params: authorization_id, ecosystem_did, all.
    Optional query param: time.
    The 200 response can be either a single AuthorizationResponse or an array.
    """
    print("\n=== Test: GET /entities/{entity_id}/authorization ===")
    url = f"{base_url}/entities/{entity_id}/authorization"
    params = {
        "authorization_id": "did:example:authz",
        "ecosystem_did": "did:example:egf",
        "all": False,  # or True, or the string "false"/"true" depending on your backend
        # "time": "2025-01-01T12:00:00Z"
    }
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False

        if resp.status_code == 200:
            data = resp.json()
            # Could be a single AuthorizationResponse or an array of them
            if isinstance(data, dict):
                # Check for 'authorized' in single object
                if "authorized" not in data:
                    print("    Missing 'authorized' key in single object response.")
                    return False
            elif isinstance(data, list):
                # For array, each item should have an 'authorized' key
                for item in data:
                    if "authorized" not in item:
                        print("    Missing 'authorized' key in one array item.")
                        return False
            else:
                print("    Unexpected JSON type (expected dict or list).")
                return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_check_ecosystem_recognition(base_url, headers, ecosystem_did):
    """
    Tests GET /registries/{ecosystem_did}/recognition
    Required query param: egf_did
    Optional query param: time
    Expected 200, 401, or 404. On 200, must match RecognitionResponse structure.
    """
    print("\n=== Test: GET /registries/{ecosystem_did}/recognition ===")
    url = f"{base_url}/registries/{ecosystem_did}/recognition"
    params = {
        "egf_did": "did:example:egf",
        # "time": "2025-01-01T12:00:00Z"
    }
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False

        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, dict):
                print("    Expected a JSON object for recognition response.")
                return False
            # Check required keys from RecognitionResponse
            for key in ["recognized", "message", "evaluated_at", "response_time"]:
                if key not in data:
                    print(f"    Missing '{key}' in recognition response.")
                    return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_list_ecosystem_recognitions(base_url, headers, ecosystem_did):
    """
    Tests GET /ecosystems/{ecosystem_did}/recognitions
    Optional query params: egf_did, time
    Expect status 200, 401, or 404. On 200, returns array of RecognitionResponse objects.
    """
    print("\n=== Test: GET /ecosystems/{ecosystem_did}/recognitions ===")
    url = f"{base_url}/ecosystems/{ecosystem_did}/recognitions"
    params = {
        # "egf_did": "did:example:egf",
        # "time": "2025-01-01T12:00:00Z"
    }
    print(f"--> Testing GET {url} with params={params}")
    try:
        resp = requests.get(url, headers=headers, params=params)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False

        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                print("    Expected a list of RecognitionResponse objects.")
                return False
            # Optionally check each item for 'recognized' key, etc.
            for item in data:
                if "recognized" not in item:
                    print("    Missing 'recognized' in a recognition item.")
                    return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_lookup_supported_assurance_levels(base_url, headers, ecosystem_did):
    """
    Tests GET /ecosystems/{ecosystem_did}/lookups/assuranceLevels
    Expect 200, 401, or 404. On 200, returns array of AssuranceLevelResponse objects.
    """
    print("\n=== Test: GET /ecosystems/{ecosystem_did}/lookups/assuranceLevels ===")
    url = f"{base_url}/ecosystems/{ecosystem_did}/lookups/assuranceLevels"
    print(f"--> Testing GET {url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False

        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                print("    Expected a list for assurance levels.")
                return False
            # Minimal check for each item
            for level_info in data:
                if not isinstance(level_info, dict):
                    print("    Each item should be a JSON object.")
                    return False
                # The spec says the object has "assurance_level", "description", ...
                # But also has 'egf_did' as well.
                # We'll just check a couple to confirm minimal structure.
                if "assurance_level" not in level_info:
                    print("    Missing 'assurance_level' key in item.")
                    return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_lookup_authorizations(base_url, headers, ecosystem_did):
    """
    Tests GET /ecosystems/{ecosystem_did}/lookups/authorizations
    Expect 200, 401, or 404. On 200, returns array of AuthorizationResponse objects.
    """
    print("\n=== Test: GET /ecosystems/{ecosystem_did}/lookups/authorizations ===")
    url = f"{base_url}/ecosystems/{ecosystem_did}/lookups/authorizations"
    print(f"--> Testing GET {url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False

        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                print("    Expected a list for authorization responses.")
                return False
            # Minimal check for each authorization response
            for auth_item in data:
                if "authorized" not in auth_item:
                    print("    Missing 'authorized' key in an auth item.")
                    return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def test_lookup_supported_did_methods(base_url, headers, ecosystem_did):
    """
    Tests GET /egfs/{ecosystem_did}/lookups/didmethods
    Expect 200, 401, or 404. On 200, returns DIDMethodListType (array of DIDMethodType).
    """
    print("\n=== Test: GET /egfs/{ecosystem_did}/lookups/didmethods ===")
    url = f"{base_url}/egfs/{ecosystem_did}/lookups/didmethods"
    print(f"--> Testing GET {url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"    Status: {resp.status_code}")

        if resp.status_code not in [200, 401, 404]:
            print("    Unexpected status code.")
            return False

        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                print("    Expected a list of DIDMethodType objects.")
                return False
            # Check minimal structure
            for method_item in data:
                if "identifier" not in method_item:
                    print("    Missing 'identifier' in DID method item.")
                    return False
    except Exception as ex:
        print(f"    Exception occurred: {ex}")
        return False
    return True


def run_all_tests(base_url, bearer_token):
    """
    Runs all test functions for the TRQP Profile API.
    """
    headers = {
        "Accept": "application/json",
        # If you do NOT use Bearer auth, remove or adjust the "Authorization" header.
        "Authorization": f"Bearer {bearer_token}" if bearer_token else "",
    }

    # Provide dummy or example arguments for required path/query params.
    # Adjust these as needed for your environment:
    dummy_entity_id = "did:example:entity123"
    dummy_ecosystem_did = "did:example:ecosystem"

    tests = [
        ("test_get_metadata", test_get_metadata(base_url, headers)),
        (
            "test_get_entity_information",
            test_get_entity_information(base_url, headers, dummy_entity_id),
        ),
        (
            "test_check_entity_authorization",
            test_check_entity_authorization(base_url, headers, dummy_entity_id),
        ),
        (
            "test_check_ecosystem_recognition",
            test_check_ecosystem_recognition(base_url, headers, dummy_ecosystem_did),
        ),
        (
            "test_list_ecosystem_recognitions",
            test_list_ecosystem_recognitions(base_url, headers, dummy_ecosystem_did),
        ),
        (
            "test_lookup_supported_assurance_levels",
            test_lookup_supported_assurance_levels(
                base_url, headers, dummy_ecosystem_did
            ),
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

    run_all_tests(args.base_url, args.bearer_token)


if __name__ == "__main__":
    main()
