#!/usr/bin/env python3

import requests
import json
import argparse
from datetime import datetime, timezone
import sys
import uuid  # For generating nonce
import jwt  # PyJWT library

DEFAULT_DID_RESOLVER_URL = "https://dev.uniresolver.io/1.0/identifiers/"


def decode_jws(jws_token, public_key=None):
    """
    Decodes a JWS (JSON Web Signature) and returns the payload.

    Args:
        jws_token (str): The JWS token (compact format, three parts: header.payload.signature).
        public_key (str, optional): The public key for signature verification. Default is None.

    Returns:
        dict: The decoded payload.
    """
    try:
        if public_key:
            # If a public key is provided, verify the signature
            payload = jwt.decode(
                jws_token, public_key, algorithms=["RS256", "ES256", "HS256"]
            )
        else:
            # If no public key is provided, decode without verification (useful for debugging)
            payload = jwt.decode(jws_token, options={"verify_signature": False})

        return payload
    except jwt.ExpiredSignatureError:
        print("Error: JWS signature has expired.")
    except jwt.InvalidTokenError:
        print("Error: Invalid JWS token.")
    except Exception as e:
        print(f"Error decoding JWS: {e}")


def generate_nonce():
    """
    Generates a secure random nonce using UUID4.
    """
    return str(uuid.uuid4())


def urljoin(base: str, url: str) -> str:
    return f"{base.rstrip('/')}/{url.lstrip('/')}"


def resolve_did(did, resolver_url):
    """
    Resolves a DID to its DID Document using the DID Resolver.
    """
    resolver_endpoint = urljoin(resolver_url, did)
    try:
        response = requests.get(resolver_endpoint)
        # response.raise_for_status()
        did_document = response.json()
        ret = did_document.get("didDocument", None)
        return ret
    except requests.exceptions.RequestException as e:
        print(f"Error resolving DID {did}: {e}", file=sys.stderr)
        return None


def get_service_endpoint(did_document, service_type):
    """
    Extracts the service endpoint URL from the DID Document based on service type.
    """
    services = did_document.get("service", [])
    for service in services:
        if service.get("type") == service_type:
            print(f"Found service type '{service_type}' in DID Document.")
            return service.get("serviceEndpoint").get("uri")
    print(f"Service type '{service_type}' not found in DID Document.", file=sys.stderr)
    return None


def format_time(time_str=None):
    """
    Formats the time to be in RFC3339 format (e.g., '2025-03-07T00:20:48Z').
    Ensures it follows 'YYYY-MM-DDTHH:MM:SSZ' format.
    """
    if time_str:
        try:
            # Ensure compatibility with Z-suffixed times
            if time_str.endswith("Z"):
                time_str = time_str[:-1] + "+00:00"

            parsed_time = datetime.fromisoformat(time_str)
            return parsed_time.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}")
    else:
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def ecosystem_recognition_query(
    egf_did, ecosystem_id, time, scope, nonce, resolver_url
):
    """
    Performs the Ecosystem Recognition Query by first resolving the EGF DID,
    getting the TR DID from the EGF DID document, then resolving the TR DID to get
    the HTTP endpoint and making the query.
    """
    print("\n--- Ecosystem Recognition Query ---")

    formatted_time = format_time(time)
    # Step 1: Resolve the EGF DID to get the EGF DID Document
    did_doc = resolve_did(egf_did, resolver_url)
    if not did_doc:
        print("Failed to resolve EGF DID.", file=sys.stderr)
        raise Exception("Failed to resolve EGF DID.")

    # Step 2: Extract the TR DID from the EGF DID Document (service endpoint)
    tr_did = get_service_endpoint(did_doc, "TRQP")
    if not tr_did:
        print("No TR DID found in EGF DID Document.", file=sys.stderr)
        raise Exception("No TR DID found in EGF DID Document.")

    # Step 3: Resolve the TR DID to get the HTTP endpoint
    print(f"Resolving TR DID: {tr_did}")
    tr_did_doc = resolve_did(tr_did, resolver_url)
    if not tr_did_doc:
        print(f"Failed to resolve TR DID: {tr_did}", file=sys.stderr)
        raise Exception(f"Failed to resolve TR DID: {tr_did}")

    # Step 4: Extract the HTTP endpoint from the TR DID Document
    tr_endpoint = get_service_endpoint(tr_did_doc, "TRQP")
    if not tr_endpoint:
        print(
            "No HTTP endpoint found in TR DID Document under 'TRQP' service.",
            file=sys.stderr,
        )
        raise Exception(
            "No HTTP endpoint found in TR DID Document under 'TRQP' service."
        )

    # Step 5: Construct the URL for the ecosystem recognition query
    endpoint_url = urljoin(tr_endpoint, f"/ecosystems/{ecosystem_id}/recognition")

    # Prepare query parameters
    params = {"egf_did": egf_did, "time": formatted_time}

    try:
        print("Making recognition query")
        # Step 6: Send GET request to the constructed endpoint
        response = requests.get(endpoint_url, params=params)
        print("Done making recognition query", response)
        response.raise_for_status()
        print("Ecosystem Recognition Query Response:")

        resp = response.json()
        print(json.dumps(resp, indent=2))
        return resp
    except requests.exceptions.RequestException as e:
        print(f"Error performing Ecosystem Recognition Query: {e}", file=sys.stderr)


def authorization_query(
    egf_did, entity_id, authorization_id, time, nonce, resolver_url
):
    """
    Performs the Authorization Query by first resolving the EGF DID,
    then resolving the TR DID to get the HTTP endpoint for authorization.
    """
    print("\n--- Authorization Query ---")
    formatted_time = format_time(time)

    # Step 1: Resolve the EGF DID to get the EGF DID Document
    did_doc = resolve_did(egf_did, resolver_url)
    if not did_doc:
        print("Failed to resolve EGF DID.", file=sys.stderr)
        raise Exception("Failed to resolve EGF DID.")

    # Step 2: Extract the TR DID from the EGF DID Document (service endpoint)
    tr_did = get_service_endpoint(did_doc, "TRQP")
    if not tr_did:
        print("No TR DID found in EGF DID Document.", file=sys.stderr)
        raise Exception("No TR DID found in EGF DID Document.")

    # Step 3: Resolve the TR DID to get the HTTP endpoint
    print(f"Resolving TR DID: {tr_did}")
    tr_did_doc = resolve_did(tr_did, resolver_url)
    if not tr_did_doc:
        print(f"Failed to resolve TR DID: {tr_did}", file=sys.stderr)
        raise Exception(f"Failed to resolve TR DID: {tr_did}")

    # Step 4: Extract the HTTP endpoint from the TR DID Document
    tr_endpoint = get_service_endpoint(tr_did_doc, "TRQP")
    if not tr_endpoint:
        print(
            "No HTTP endpoint found in TR DID Document under 'TRQP' service.",
            file=sys.stderr,
        )
        raise Exception(
            "No HTTP endpoint found in TR DID Document under 'TRQP' service."
        )

    # Step 5: Construct the URL for the authorization query
    endpoint_url = urljoin(tr_endpoint, f"/entities/{entity_id}/authorization")

    # Prepare query parameters
    params = {
        "authorization_id": authorization_id,
        "ecosystem_did": egf_did,
        "time": formatted_time,
        "all": "true",  # Assuming "true" by default to return list of authorizations
    }

    try:
        # Step 6: Send GET request to the constructed endpoint
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()
        print("Authorization Query Response:")

        resp = response.json()
        print(json.dumps(resp, indent=2))
        return resp
    except requests.exceptions.RequestException as e:
        print(f"Error performing Authorization Query: {e}", file=sys.stderr)
        return None


def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="CLI Tool for Ecosystem Recognition and Authorization Queries."
    )

    # Global argument for DID Resolver URL
    parser.add_argument(
        "--resolver-url",
        type=str,
        default=DEFAULT_DID_RESOLVER_URL,
        help=f"DID Resolver endpoint URL (default: {DEFAULT_DID_RESOLVER_URL})",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Available commands",
        dest="command",
        required=True,
    )

    # Subparser for Ecosystem Recognition Query
    recognize_parser = subparsers.add_parser(
        "recognize", help="Perform Ecosystem Recognition Query."
    )
    recognize_parser.add_argument(
        "--egf-did",
        type=str,
        default="did:web:ayra:forum",
        help="EGF DID for Recognition Query (default: did:web:ayra:forum)",
    )
    recognize_parser.add_argument(
        "--ecosystem-id",
        type=str,
        required=True,
        help="Ecosystem ID for Recognition Query",
    )
    recognize_parser.add_argument(
        "--scope", type=str, required=False, help="Scope for Recognition Query"
    )
    recognize_parser.add_argument(
        "--time",
        type=str,
        default=datetime.utcnow().isoformat(),
        help="Time for Recognition Query in ISO format (default: current UTC time)",
    )
    recognize_parser.add_argument(
        "--nonce",
        type=str,
        default=None,
        help="A unique client-generated nonce to prevent replay attacks (optional; will be generated if not provided)",
    )

    # Subparser for Authorization Query
    authorize_parser = subparsers.add_parser(
        "authorize", help="Perform Authorization Query."
    )
    authorize_parser.add_argument(
        "--egf-did", type=str, required=True, help="EGF DID for Authorization Query"
    )
    authorize_parser.add_argument(
        "--entity-id", type=str, required=True, help="Entity ID for Authorization Query"
    )
    authorize_parser.add_argument(
        "--authorization-id",
        type=str,
        required=True,
        help="Authorization ID for Authorization Query",
    )
    authorize_parser.add_argument(
        "--time",
        type=str,
        default=datetime.utcnow().isoformat(),
        help="Time for Authorization Query in ISO format (default: current UTC time)",
    )
    authorize_parser.add_argument(
        "--nonce",
        type=str,
        default=None,
        help="A unique client-generated nonce to prevent replay attacks (optional; will be generated if not provided)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    resolver_url = args.resolver_url if args.resolver_url else DEFAULT_DID_RESOLVER_URL
    print("RESOLVER_URL")

    if args.command == "recognize":
        nonce = args.nonce if args.nonce else generate_nonce()
        print(f"Using nonce: {nonce}")
        ecosystem_recognition_query(
            egf_did=args.egf_did,
            ecosystem_id=args.ecosystem_id,
            time=args.time,
            scope=args.scope,
            nonce=nonce,
            resolver_url=resolver_url,
        )
    elif args.command == "authorize":
        nonce = args.nonce if args.nonce else generate_nonce()
        print(f"Using nonce: {nonce}")
        authorization_query(
            egf_did=args.egf_did,
            entity_id=args.entity_id,
            authorization_id=args.authorization_id,
            time=args.time,
            nonce=nonce,
            resolver_url=resolver_url,
        )
    else:
        print("Unknown command. Use --help for more information.", file=sys.stderr)


if __name__ == "__main__":
    main()
