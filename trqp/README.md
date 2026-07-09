# TRQP Alignment

This directory contains resources that track the alignment between the Ayra TRQP Profile and the [TRQP v2.0 specification](https://trustoverip.github.io/tswg-trust-registry-protocol/).

## Ayra Profile Relationship to TRQP v2.0

The Ayra TRQP Profile is a **profile** of TRQP v2.0. It:

- **Requires** both `/authorization` and `/recognition` endpoints (TRQP v2.0 requires at least one). These core endpoints are mandatory for the Ayra Profile and MUST NOT use `501 Not Implemented` to indicate non-support.
- **Requires** identifiers to use TRQP's `_id` field names. Ayra Profile `_id` values are DID URI strings; supported DID methods are discoverable through the Ayra DID methods lookup, and `did:webvh` is preferred and may be required for higher assurance levels.
- **Recommends** JWS response signing (not required by TRQP core).
- **Adds** extension endpoints for metadata, entity lookup, assurance levels, authorizations, and DID methods.

## Schemas

The `schema/` directory contains JSON Schema files aligned with TRQP v2.0's PARC model (`entity_id`, `authority_id`, `action`, `resource`):

- `trqp_authorization_request.schema.json`
- `trqp_authorization_response.schema.json`
- `trqp_recognition_request.schema.json`
- `trqp_recognition_response.schema.json`

## Items for Future TRQP Consideration

- **Metadata endpoint:** TRQP v2.0 does not define an explicit `/metadata` endpoint. Ayra defines this as a profile extension. A future TRQP version may benefit from a standardized metadata query type.
