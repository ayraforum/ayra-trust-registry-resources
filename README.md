# Ayra Trust Registry Resources

This repository contains the Ayra Trust Registry Query Protocol (TRQP) Profile: the API specification, profile requirements, schemas, guides, and smoke tests needed to expose or consume Ayra-compatible trust registry services.

TRQP answers two core questions for verifiers and ecosystems:

- **Authorization:** Is this entity authorized to perform this action on this resource under this authority?
- **Recognition:** Does this authority recognize this other authority or registry for this action and resource?

The Ayra Profile narrows and extends TRQP v2.0 for the Ayra Trust Network. It keeps the TRQP field names (`entity_id`, `authority_id`, `action`, `resource`, and optional `context`) and requires Ayra `_id` values to be DID URI strings as defined by [W3C DID Core](https://www.w3.org/TR/did-core/). Supported DID methods are authority- or registry-specific and discoverable through lookup endpoints; `did:webvh` is preferred and may be required for higher assurance levels.

The [Ayra TRQP Profile API](./trqp_ayra_profile_swagger.yaml) is the normative API surface for this repository.

## Ayra Profile at a Glance

Ayra-conformant Trust Registries:

- **MUST** implement both TRQP core endpoints: `POST /authorization` and `POST /recognition`.
- **MUST** use TRQP's `_id` field names, with Ayra `_id` values represented as DID URI strings.
- **MUST** return RFC 7807 Problem Details for error responses.
- **MAY** implement Ayra extension endpoints for metadata, entity discovery, ecosystem discovery, and lookups.
- **MUST** return HTTP 501 with Problem Details when an optional Ayra extension endpoint is not implemented.
- **SHOULD** sign responses with JWS where supported; the signing mechanism is still being finalized.

## API Surface

Core TRQP endpoints:

| Endpoint | Method | Purpose |
| :-- | :-- | :-- |
| `/authorization` | POST | Query whether an entity is authorized for an action/resource under an authority. |
| `/recognition` | POST | Query whether an authority recognizes another authority or registry. |

Optional Ayra extension endpoints:

| Endpoint | Method | Purpose |
| :-- | :-- | :-- |
| `/metadata` | GET | Retrieve basic trust registry metadata. |
| `/entities/{entity_id}` | GET | Retrieve entity information. |
| `/entities` | GET | List known entities with optional filters. |
| `/entities/{entity_id}/authorizations` | GET | List authorizations for an entity. |
| `/ecosystems/{ecosystem_id}` | GET | Retrieve ecosystem information. |
| `/ecosystems/{ecosystem_id}/recognitions` | GET | List ecosystems recognized by a given ecosystem. |
| `/lookups/assuranceLevels` | GET | Discover supported assurance levels. |
| `/lookups/authorizations` | GET | Discover supported action/resource authorization pairs. |
| `/lookups/didMethods` | GET | Discover supported DID methods and assurance limits. |

## API Specifications

Interactive Swagger UI rendering of the TRQP and Ayra Profile API:

- [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) -- TRQP v2.0 core endpoints (`trqp-core` tag) and Ayra extension endpoints (`ayra-extension` tag)

## Normative Resources

- [TRQP v2.0 Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/) -- The Trust Registry Query Protocol specification
- [W3C DID Core](https://www.w3.org/TR/did-core/) -- Decentralized Identifiers (DIDs) v1.0, including DID URI and DID Document definitions
- [Ayra TRQP Profile API](./trqp_ayra_profile_swagger.yaml) -- OpenAPI specification covering TRQP v2.0 core and Ayra extensions
- [Ayra TRQP Profile](./spec/profile.md) -- Profile required to register into the Ayra Trust Network

## Guides

- [Implementers Guide](./guides/implementers_guide.md) -- Comprehensive guide for connecting to the Ayra Trust Network, including conformance checklist, request/response examples, and integration patterns.
- [TRQP Alignment](./trqp/README.md) -- How the Ayra TRQP Profile aligns with and extends TRQP v2.0.

## Which Document Should I Read?

- **Implementing a Trust Registry:** Start with the [Ayra TRQP Profile](./spec/profile.md), then use the [Ayra TRQP Profile API](./trqp_ayra_profile_swagger.yaml) while building.
- **Consuming/verifying trust registry data:** Start with the [Implementers Guide](./guides/implementers_guide.md), especially the authorization and recognition flows.
- **Checking TRQP compatibility:** Read [TRQP Alignment](./trqp/README.md) and compare against the [TRQP v2.0 Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/).
- **Running a quick implementation check:** Use the smoke test in [tests/api_conformance_test.py](./tests/api_conformance_test.py).

## For Agents and Automation

If you are an automated coding agent, documentation assistant, or conformance tool, use this source-of-truth order:

1. **TRQP v2.0** is authoritative for the core protocol model and core field names.
2. **W3C DID Core** is authoritative for DID URI, DID method, DID controller, and DID Document semantics.
3. **Ayra TRQP Profile API** ([trqp_ayra_profile_swagger.yaml](./trqp_ayra_profile_swagger.yaml)) is authoritative for the Ayra API surface.
4. **Ayra TRQP Profile** ([spec/profile.md](./spec/profile.md)) is authoritative for Ayra profile requirements.
5. Guides and tests are supporting material and can lag the normative files.

Important interpretation rules:

- Do not rename TRQP fields to `_did`. Ayra uses TRQP-compatible `_id` field names such as `entity_id` and `authority_id`, and the values are DID URI strings.
- Do not assume only `did:webvh` and `did:web` are supported. Supported DID methods are registry/authority-specific and discoverable through `GET /lookups/didMethods`.
- Do not treat Ayra extension endpoints as mandatory. If unsupported, they return HTTP 501 with Problem Details.
- Do not treat response signing as mandatory. JWS response signing is a SHOULD while the signing mechanism is being finalized.
- JSON Schema files use the `.schema.json` extension.

Useful local checks:

```bash
python3 -m py_compile tests/api_conformance_test.py
python3 -c 'import json, pathlib; [json.loads(p.read_text()) for p in pathlib.Path("trqp/schema").glob("*.schema.json")]; json.loads(pathlib.Path("schema/ayra_metadata.schema.json").read_text()); print("json ok")'
```

## Schemas

- [TRQP JSON Schemas](./trqp/schema/) -- JSON Schema definitions for TRQP v2.0 authorization and recognition queries and responses.
- [Ayra Metadata Schema](./schema/ayra_metadata.schema.json) -- JSON Schema for Ayra Trust Registry metadata.

## Getting Started

1. Read the [Ayra TRQP Profile](./spec/profile.md) to understand the normative profile requirements.
2. Review the [Ayra TRQP Profile API](./trqp_ayra_profile_swagger.yaml) or the [interactive API docs](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) for endpoint details.
3. Read the [Implementers Guide](./guides/implementers_guide.md) for examples, implementation patterns, and verifier flows.
4. Run the smoke test in [tests/api_conformance_test.py](./tests/api_conformance_test.py) against your implementation.

## Contributing

We welcome contributions to improve these resources. Please see [CONTRIBUTING](./CONTRIBUTING) for details on how to contribute.

## Dependency maintenance

- JavaScript documentation tooling uses npm and the committed `package-lock.json`; install with `npm ci`.
- Current dependency audit notes and accepted residual risk are documented in [Dependency risk notes](./docs/dependency-risk.md).

## Key Links

- [TRQP v2.0 Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/)
- [W3C DID Core](https://www.w3.org/TR/did-core/)
- [TRQP Specification GitHub Repository](https://github.com/trustoverip/tswg-trust-registry-protocol/tree/main)
