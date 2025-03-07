#!/usr/bin/env python

import json
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives import serialization
from base58 import b58encode

# Mappings for abbreviation/expansion
full_to_abbreviation = {
    "profile": "profile",
    "type": "type",
    "serviceEndpoint": "serviceEndpoint",
    "routingKeys": "routingKeys",
    "accept": "accept",
    "DIDCommMessaging": "dm",
    "integrity": "integrity",
    "uri": "uri",
}
abbreviation_to_full = {v: k for k, v in full_to_abbreviation.items()}


def abbreviate_service(obj):
    """Convert full service fields to abbreviations."""
    if isinstance(obj, dict):
        return {
            full_to_abbreviation.get(k, k): abbreviate_service(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [abbreviate_service(elem) for elem in obj]
    return obj


def expand_service(obj):
    """Convert abbreviated service fields to full names."""
    if isinstance(obj, dict):
        return {
            abbreviation_to_full.get(k, k): expand_service(v) for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [expand_service(elem) for elem in obj]
    return obj


def generate_did_peer2(config_data, method_prefix="did:peer:2"):
    """Generate a DID:peer:2 identifier with service endpoints."""
    # Generate Ed25519 Key
    ed_private_key = ed25519.Ed25519PrivateKey.generate()
    ed_public_key = ed_private_key.public_key()
    ed_pub_bytes = ed_public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    # Generate X25519 Key
    x25519_private_key = x25519.X25519PrivateKey.generate()
    x25519_public_key = x25519_private_key.public_key()
    x25519_pub_bytes = x25519_public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )

    # Encode multibase public keys
    ed_pub_mb = "z" + b58encode(ed_pub_bytes).decode()
    x25519_pub_mb = "z" + b58encode(x25519_pub_bytes).decode()

    # Build DID segments: V=auth key, E=keyAgreement
    did_parts = [method_prefix, "V" + ed_pub_mb, "E" + x25519_pub_mb]

    # Abbreviate and encode services
    for svc in config_data.get("services", []):
        abbrev = abbreviate_service(svc)
        svc_bytes = json.dumps(abbrev).encode()
        b64 = base64.urlsafe_b64encode(svc_bytes).decode().rstrip("=")
        did_parts.append("S" + b64)

    did = ".".join(did_parts)

    # Private keys in hex format
    ed_priv_hex = ed_private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()

    x25519_priv_hex = x25519_private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()

    return did, ed_priv_hex, x25519_priv_hex


def resolve_did_peer2(did_str, method_prefix="did:peer:2"):
    """Resolve a DID:peer:2 string into a DID Document."""
    if not did_str.startswith(method_prefix):
        raise ValueError(
            f"DID '{did_str}' does not match method prefix '{method_prefix}'"
        )

    doc = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "id": did_str,
    }

    vm_list, auth, assertion, key_agreement, cap_inv, cap_del, services = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
    service_count = 0

    body = did_str[len(method_prefix) :].lstrip(".")
    parts = body.split(".")
    key_index = 1

    for seg in parts:
        if len(seg) < 2:
            raise ValueError(f"Malformed segment: '{seg}'")
        purpose, rest = seg[0], seg[1:]

        if purpose in ["V", "A", "E", "I", "D"]:
            key_id = f"#key-{key_index}"
            key_index += 1
            vm_list.append(
                {
                    "id": key_id,
                    "type": "Multikey",
                    "controller": did_str,
                    "publicKeyMultibase": rest,
                }
            )

            if purpose == "V":
                auth.append(key_id)
            elif purpose == "A":
                assertion.append(key_id)
            elif purpose == "E":
                key_agreement.append(key_id)
            elif purpose == "I":
                cap_inv.append(key_id)
            elif purpose == "D":
                cap_del.append(key_id)

        elif purpose == "S":
            # Decode the service segment
            padding_needed = (4 - len(rest) % 4) % 4
            svc_bytes = base64.urlsafe_b64decode(rest + ("=" * padding_needed))
            expanded = expand_service(json.loads(svc_bytes))

            if not isinstance(expanded, dict):
                raise ValueError("Decoded service is not an object")

            expanded["id"] = (
                f"#service-{service_count}" if service_count else "#service"
            )
            service_count += 1
            services.append(expanded)

        else:
            raise ValueError(f"Unknown purpose code '{purpose}' in segment '{seg}'")

    if vm_list:
        doc["verificationMethod"] = vm_list
    if auth:
        doc["authentication"] = auth
    if assertion:
        doc["assertionMethod"] = assertion
    if key_agreement:
        doc["keyAgreement"] = key_agreement
    if cap_inv:
        doc["capabilityInvocation"] = cap_inv
    if cap_del:
        doc["capabilityDelegation"] = cap_del
    if services:
        doc["service"] = services

    return doc
