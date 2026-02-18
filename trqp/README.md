# TRQP Alignment

This directory contains resources that track the alignment between the Ayra TRQP Profile and the [TRQP v2.0 specification](https://trustoverip.github.io/tswg-trust-registry-protocol/).

## Ayra Profile Relationship to TRQP v2.0

The Ayra Authority Verification Profile is a **profile** of TRQP v2.0. It:

- **Requires** both `/authorization` and `/recognition` endpoints (TRQP v2.0 requires at least one). NOTE: either can return a 501 (NOT IMPLEMENTED), but both are required to conform with the Swagger/OAS specification.
- **Constrains** identifiers to `did:webvh` (TRQP v2.0 allows any RFC 3986 URI).
- **Adds** JWS response signing (not required by TRQP core).
- **Adds** extension endpoints for metadata, entity lookup, assurance levels, authorizations, and DID methods.

## Schemas

The `schema/` directory contains JSON Schema files aligned with TRQP v2.0's PARC model (`entity_id`, `authority_id`, `action`, `resource`):

- `trqp_authorization_request.jsonschema`
- `trqp_authorization_response.jsonschema`
- `trqp_recognition_request.jsonschema`
- `trqp_recognition_response.jsonschema`

## Items for Future TRQP Consideration

- **Metadata endpoint:** TRQP v2.0 does not define an explicit `/metadata` endpoint. Ayra defines this as a profile extension. A future TRQP version may benefit from a standardized metadata query type.
