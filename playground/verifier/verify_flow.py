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
        if "didDocument" not in did_document:
            error_msg = did_document.get("error", "Unknown error resolving DID")
            print(f"Error resolving DID {did}: {error_msg}", file=sys.stderr)
            raise Exception(f"DID resolution failed: {error_msg}")
        
        ret = did_document.get("didDocument", None)
        return ret
    except requests.exceptions.RequestException as e:
        print(f"Error resolving DID {did}: {e}", file=sys.stderr)
        raise Exception(f"Network error resolving DID: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON response when resolving DID {did}: {e}", file=sys.stderr)
        raise Exception(f"Invalid response format when resolving DID: {str(e)}")


def get_service_endpoint(did_document, service_type):
    """
    Extracts the service endpoint URL from the DID Document based on service type.
    Handles different service endpoint formats including abbreviated versions.
    """
    if not did_document:
        raise Exception("DID document is empty or invalid")
        
    services = did_document.get("service", [])
    if not services:
        raise Exception(f"No services found in DID document")
        
    for service in services:
        if service.get("type") == service_type:
            print(f"Found service type '{service_type}' in DID Document.")
            
            # Handle different service endpoint formats
            service_endpoint = service.get("serviceEndpoint")
            
            # Standard format with 'uri' property
            if isinstance(service_endpoint, dict) and "uri" in service_endpoint:
                return service_endpoint.get("uri")
            
            # Standard format with direct string
            elif isinstance(service_endpoint, str):
                return service_endpoint
            
            # Check abbreviated formats and convert to standard format
            # 'p' -> 'profile', 'u' -> 'uri', 'i' -> 'integrity'
            elif isinstance(service_endpoint, dict):
                # Handle both abbreviated and standard property names
                
                # First check for standard 'uri' property
                if "uri" in service_endpoint:
                    uri_value = service_endpoint.get("uri")
                    if isinstance(uri_value, list) and len(uri_value) > 0:
                        return uri_value[0]
                    return uri_value
                
                # Then check for abbreviated 'u' property
                elif "u" in service_endpoint:
                    u_value = service_endpoint.get("u")
                    if isinstance(u_value, list) and len(u_value) > 0:
                        return u_value[0]
                    return u_value
                
                # Create standard format from abbreviated
                standard_endpoint = {}
                if "p" in service_endpoint:
                    standard_endpoint["profile"] = service_endpoint.get("p")
                if "u" in service_endpoint:
                    standard_endpoint["uri"] = service_endpoint.get("u")
                if "i" in service_endpoint:
                    standard_endpoint["integrity"] = service_endpoint.get("i")
                
                # Convert abbreviated format to standard and try again
                print(f"Converting abbreviated format to standard: {standard_endpoint}")
                
                # Extract URI from standard format
                uri_value = standard_endpoint.get("uri")
                if uri_value:
                    if isinstance(uri_value, list) and len(uri_value) > 0:
                        return uri_value[0]
                    return uri_value
                
                print(f"Service endpoint does not contain a URI: {service_endpoint}", file=sys.stderr)
                raise Exception(f"Service endpoint does not contain a URI: {service_endpoint}")
            else:
                print(f"Unsupported service endpoint format: {service_endpoint}", file=sys.stderr)
                raise Exception(f"Unsupported service endpoint format: {service_endpoint}")
                
    print(f"Service type '{service_type}' not found in DID Document.", file=sys.stderr)
    raise Exception(f"Service type '{service_type}' not found in DID document")


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
    
    error_details = {}
    
    try:
        formatted_time = format_time(time)
        
        # Step 1: Resolve the EGF DID to get the EGF DID Document
        print("Resolving EGF DID:", egf_did)
        did_doc = resolve_did(egf_did, resolver_url)
        if not did_doc:
            raise Exception("Failed to resolve EGF DID.")
        error_details["egf_did_doc"] = did_doc
            
        # Step 2: Extract the TR DID from the EGF DID Document (service endpoint)
        tr_did = get_service_endpoint(did_doc, "TRQP")
        if not tr_did:
            raise Exception("No TR DID found in EGF DID Document.")
        error_details["tr_did"] = tr_did
            
        # Step 3: Resolve the TR DID to get the HTTP endpoint
        print(f"Resolving TR DID: {tr_did}")
        tr_did_doc = resolve_did(tr_did, resolver_url)
        if not tr_did_doc:
            raise Exception(f"Failed to resolve TR DID: {tr_did}")
        error_details["tr_did_doc"] = tr_did_doc
            
        # Step 4: Extract the HTTP endpoint from the TR DID Document
        tr_endpoint = get_service_endpoint(tr_did_doc, "TRQP")
        if not tr_endpoint:
            raise Exception("No HTTP endpoint found in TR DID Document under 'TRQP' service.")
        error_details["tr_endpoint"] = tr_endpoint
            
        # Step 5: Construct the URL for the ecosystem recognition query
        endpoint_url = urljoin(tr_endpoint, f"/ecosystems/{ecosystem_id}/recognition")
        error_details["endpoint_url"] = endpoint_url
        
        # Prepare query parameters
        params = {"egf_did": egf_did, "time": formatted_time}
        error_details["query_params"] = params
        
        # Step 6: Send GET request to the constructed endpoint
        print("Making recognition query to:", endpoint_url)
        response = requests.get(endpoint_url, params=params)
        error_details["response_status"] = response.status_code
        error_details["response_text"] = response.text
        
        try:
            error_details["response_json"] = response.json()
        except:
            pass
            
        response.raise_for_status()
        
        resp = response.json()
        print("Ecosystem Recognition Query Response:")
        print(json.dumps(resp, indent=2))
        return resp
            
    except Exception as e:
        print(f"Error performing Ecosystem Recognition Query: {e}", file=sys.stderr)
        error_message = str(e)
        
        # Enhance the error message with relevant details
        return {
            "error": error_message,
            "status": "failed",
            "details": error_details,
            "resolution_steps": [
                "Check that the EGF DID is correct and resolves properly",
                "Verify that the Trust Registry DID exists in the EGF DID document as a TRQP service",
                "Confirm the Trust Registry service is running and accessible",
                "Ensure the ecosystem ID is valid and recognized by the Trust Registry"
            ]
        }


def authorization_query(
    egf_did, entity_id, authorization_id, time, nonce, resolver_url
):
    """
    Performs the Authorization Query by first resolving the EGF DID,
    then resolving the TR DID to get the HTTP endpoint for authorization.
    """
    print("\n--- Authorization Query ---")
    
    error_details = {}
    
    try:
        formatted_time = format_time(time)
        
        # Step 1: Resolve the EGF DID to get the EGF DID Document
        print("Resolving EGF DID:", egf_did)
        did_doc = resolve_did(egf_did, resolver_url)
        if not did_doc:
            raise Exception("Failed to resolve EGF DID.")
        error_details["egf_did_doc"] = did_doc
            
        # Step 2: Extract the TR DID from the EGF DID Document (service endpoint)
        tr_did = get_service_endpoint(did_doc, "TRQP")
        if not tr_did:
            raise Exception("No TR DID found in EGF DID Document.")
        error_details["tr_did"] = tr_did
            
        # Step 3: Resolve the TR DID to get the HTTP endpoint
        print(f"Resolving TR DID: {tr_did}")
        tr_did_doc = resolve_did(tr_did, resolver_url)
        if not tr_did_doc:
            raise Exception(f"Failed to resolve TR DID: {tr_did}")
        error_details["tr_did_doc"] = tr_did_doc
            
        # Step 4: Extract the HTTP endpoint from the TR DID Document
        tr_endpoint = get_service_endpoint(tr_did_doc, "TRQP")
        if not tr_endpoint:
            raise Exception("No HTTP endpoint found in TR DID Document under 'TRQP' service.")
        error_details["tr_endpoint"] = tr_endpoint
            
        # Step 5: Construct the URL for the authorization query
        endpoint_url = urljoin(tr_endpoint, f"/entities/{entity_id}/authorization")
        error_details["endpoint_url"] = endpoint_url
        
        # Prepare query parameters
        params = {
            "authorization_id": authorization_id,
            "ecosystem_did": egf_did,
            "time": formatted_time,
            "all": "true",  # Assuming "true" by default to return list of authorizations
        }
        error_details["query_params"] = params
        
        # Step 6: Send GET request to the constructed endpoint
        print("Making authorization query to:", endpoint_url)
        response = requests.get(endpoint_url, params=params)
        error_details["response_status"] = response.status_code
        error_details["response_text"] = response.text
        
        try:
            error_details["response_json"] = response.json()
        except:
            pass
            
        response.raise_for_status()
        
        resp = response.json()
        print("Authorization Query Response:")
        print(json.dumps(resp, indent=2))
        return resp
            
    except Exception as e:
        print(f"Error performing Authorization Query: {e}", file=sys.stderr)
        error_message = str(e)
        
        # Enhance the error message with relevant details
        return {
            "error": error_message,
            "status": "failed",
            "details": error_details,
            "resolution_steps": [
                "Check that the EGF DID is correct and resolves properly",
                "Verify that the Trust Registry DID exists in the EGF DID document as a TRQP service",
                "Confirm the entity ID is valid and exists in the Trust Registry",
                "Ensure the authorization ID is correct for the specified entity"
            ]
        }


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
