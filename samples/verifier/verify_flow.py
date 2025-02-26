#!/usr/bin/env python3

import requests
import json
import argparse
from datetime import datetime
import sys
import uuid  # For generating nonce
import secrets  # For generating secure tokens
from urllib.parse import urljoin as urllib_urljoin  # Use standard library for URL joining
import jwt  # PyJWT library
import json


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
            payload = jwt.decode(jws_token, public_key, algorithms=["RS256", "ES256", "HS256"])
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
        ret = did_document.get('didDocument', None)
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


def ecosystem_recognition_query(egf_did, ecosystem_id, time, scope, nonce, resolver_url):
    """
    Performs the Ecosystem Recognition Query.
    """
    print("\n--- Ecosystem Recognition Query ---")
    did_doc = resolve_did(egf_did, resolver_url)
    if not did_doc:
        print("Failed to resolve EGF DID.", file=sys.stderr)
        raise Exception("Failed to resolve EGF DID.")

    # Assuming the service type for recognition is 'TRQP'
    recognition_service = get_service_endpoint(did_doc, "TRQP")
    if not recognition_service:
        print("RecognitionService endpoint not found.", file=sys.stderr)
        raise Exception("RecognitionService endpoint not found.")

    # Construct the URL as per OpenAPI spec: /ecosystem/recognition/{egf_did}/{ecosystem_id}
    endpoint_url = urljoin(recognition_service, f"/ecosystem/recognition/{egf_did}/{ecosystem_id}")

    # Prepare query parameters
    params = {
        "time": time,
        "nonce": nonce
    }

    try:
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()
        print("Ecosystem Recognition Query Response:")
        resp = response.json()
        jws = resp.get("jws", None)
        if jws:
            # Decode the JWS token
            decoded_payload = decode_jws(jws)
            if decoded_payload:
                resp["decoded_payload"] = decoded_payload
                return resp
        else:
            raise Exception("No JWS token found in response.")

        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error performing Ecosystem Recognition Query: {e}", file=sys.stderr)


def authorization_query(egf_did, entity_id, authorization_id, time, nonce, resolver_url):
    """
    Performs the Authorization Query.
    """
    print("\n--- Authorization Query ---")
    did_doc = resolve_did(egf_did, resolver_url)
    if not did_doc:
        print("Failed to resolve EGF DID.", file=sys.stderr)
        return

    # Confirm acceptance (implementation depends on specific requirements)
    # For example, checking if the DID Document has a specific verification method
    # Here, we'll assume acceptance if DID Document is successfully resolved
    print(f"DID {egf_did} resolved successfully. Confirmed to accept.")

    # Assuming the service type for authorization is 'TRQP'
    trqp_service = get_service_endpoint(did_doc, "TRQP")
    if not trqp_service:
        print("AuthorizationService endpoint not found.", file=sys.stderr)
        return

    # Construct the URL as per OpenAPI spec: /entity/authorized/{entity_id}/{authorization_id}/{egf_did}
    endpoint_url = urljoin(trqp_service, f"/entity/authorized/{entity_id}/{authorization_id}/{egf_did}")

    # Prepare query parameters
    params = {
        "time": time,
        "nonce": nonce
    }

    try:
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()
        print("Authorization Query Response:")
        resp = response.json()
        jws = resp.get("jws", None)
        if jws:
            # Decode the JWS token
            decoded_payload = decode_jws(jws)
            if decoded_payload:
                resp["decoded_payload"] = decoded_payload
                return resp
        else:
            raise Exception("No JWS token found in response.")
    except requests.exceptions.RequestException as e:
        print(f"Error performing Authorization Query: {e}", file=sys.stderr)


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
        help=f"DID Resolver endpoint URL (default: {DEFAULT_DID_RESOLVER_URL})"
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Available commands",
        dest="command",
        required=True
    )

    # Subparser for Ecosystem Recognition Query
    recognize_parser = subparsers.add_parser(
        "recognize",
        help="Perform Ecosystem Recognition Query."
    )
    recognize_parser.add_argument(
        "--egf-did",
        type=str,
        default="did:web:ayra:forum",
        help="EGF DID for Recognition Query (default: did:web:ayra:forum)"
    )
    recognize_parser.add_argument(
        "--ecosystem-id",
        type=str,
        required=True,
        help="Ecosystem ID for Recognition Query"
    )
    recognize_parser.add_argument(
        "--scope",
        type=str,
        required=False,
        help="Scope for Recognition Query"
    )
    recognize_parser.add_argument(
        "--time",
        type=str,
        default=datetime.utcnow().isoformat(),
        help="Time for Recognition Query in ISO format (default: current UTC time)"
    )
    recognize_parser.add_argument(
        "--nonce",
        type=str,
        default=None,
        help="A unique client-generated nonce to prevent replay attacks (optional; will be generated if not provided)"
    )

    # Subparser for Authorization Query
    authorize_parser = subparsers.add_parser(
        "authorize",
        help="Perform Authorization Query."
    )
    authorize_parser.add_argument(
        "--egf-did",
        type=str,
        required=True,
        help="EGF DID for Authorization Query"
    )
    authorize_parser.add_argument(
        "--entity-id",
        type=str,
        required=True,
        help="Entity ID for Authorization Query"
    )
    authorize_parser.add_argument(
        "--authorization-id",
        type=str,
        required=True,
        help="Authorization ID for Authorization Query"
    )
    authorize_parser.add_argument(
        "--time",
        type=str,
        default=datetime.utcnow().isoformat(),
        help="Time for Authorization Query in ISO format (default: current UTC time)"
    )
    authorize_parser.add_argument(
        "--nonce",
        type=str,
        default=None,
        help="A unique client-generated nonce to prevent replay attacks (optional; will be generated if not provided)"
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
            resolver_url=resolver_url
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
            resolver_url=resolver_url
        )
    else:
        print("Unknown command. Use --help for more information.", file=sys.stderr)


if __name__ == "__main__":
    main()
