# **Ayra TRQP Profile**

This specification defines the Ayra TRQP Profile for the Ayra Trust Network. It profiles the [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) for use within the Ayra Trust Network.

| | |
| :---- | :---- |
| **Version** | v0.5.0-draft |
| **Audience** | Implementors of Trust Registries participating in the Ayra Trust Network -- both TRQP API Providers and TRQP Consumers (Verifiers). |

- [Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/) -- non-normative guidance, examples, and integration patterns
- [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) -- normative OpenAPI documentation for the Ayra TRQP Profile API surface (use tags to filter by `trqp-core` or `ayra-extension`)

# **Profile Overview**

| Component | Ayra Profile Requirement |
| :---- | :---- |
| **Core Protocol** | [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) |
| **TRQP Binding** | HTTPS RESTful Binding |
| **Query Model** | PARC: Principal (`entity_id`), Action (`action`), Resource (`resource`), Context (`authority_id` + `context`) |
| **Identifier Method** | [DID URI](https://www.w3.org/TR/did-core/); supported DID methods are discoverable via `/lookups/didMethods`; `did:webvh` is preferred for higher assurance levels |
| **Ecosystem Governance Framework** | Identifier or URI discoverable via `authority_id` |
| **DateTime Format** | [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) in UTC (Z offset only) |
| **Error Format** | [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Problem Details |

# **Identifier Requirements**

## General Identifier Requirements

The approved TRQP v2.0 specification is the source of truth for core identifier semantics. [W3C DID Core](https://www.w3.org/TR/did-core/) is the source of truth for DID, DID URI, DID method, DID controller, and DID Document semantics. The Ayra Profile uses the TRQP field names `authority_id`, `entity_id`, `action`, and `resource` for all core queries and uses `_id`, not `_did`, for Ayra extension parameters and properties.

All `_id` values in Ayra TRQP messages **MUST** be DIDs represented as DID URI strings, as defined by W3C DID Core. The supported DID methods are defined by the relevant authority or registry and should be exposed through `GET /lookups/didMethods` when that optional endpoint is implemented. `did:webvh` is preferred and may be required for higher assurance levels. `did:web` and other DID methods may be acceptable, subject to authority policy and any assurance-level limits advertised by the registry.

## Ecosystem and Authority Identifiers

For Ayra, an ecosystem DID is normally used as the TRQP `authority_id`. The `authority_id` identifies the authority whose governance context is being queried.

The ecosystem governance framework **MUST** be discoverable via the `authority_id`, consistent with TRQP v2.0. This discovery may be expressed through [DID Document](https://www.w3.org/TR/did-core/) service entries or another mechanism defined by the ecosystem's governance and implementation profile.

Only valid ecosystem controllers are allowed to register the ecosystem with the Ayra Trust Network.

## Trust Registry Identifiers

Trust Registry identifiers **MUST** be DIDs. The Trust Registry DID Document should make its TRQP service endpoint discoverable. A Trust Registry may serve authority statements for one or more ecosystems.

# **Protocol Requirements**

## TRQP v2.0 Compliance

All Trust Registries in the Ayra Trust Network **MUST** implement the [TRQP v2.0 HTTPS Binding](https://trustoverip.github.io/tswg-trust-registry-protocol/):

1. **`POST /authorization`** -- accept authorization queries and return responses conforming to the TRQP v2.0 schema.
2. **`POST /recognition`** -- accept recognition queries and return responses conforming to the TRQP v2.0 schema.

All queries use the PARC model with required fields: `entity_id`, `authority_id`, `action`, `resource`, and optional `context`, as defined by TRQP v2.0.

All error responses **MUST** use [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Problem Details format with appropriate HTTP status codes (400, 401, 404, 500).

## Ayra Trust Network DID

The Ayra Trust Network DID is:

```text
did:webvh:ayra.forum
```

Valid trust registries that serve the metaregistry state of the Ayra Trust Network are represented as `TrustRegistryService` service endpoints in the ATN DID Document.

## Ayra Extension Endpoints

In addition to the TRQP v2.0 core endpoints, the Ayra Profile defines the following optional extension endpoints. If an extension endpoint is not implemented, a Trust Registry **MUST** return HTTP 501 with a Problem Details response. If an extension endpoint is implemented, it **MUST** conform to the Ayra TRQP Profile API.

| Endpoint | Method | Description |
| :---- | :---- | :---- |
| `/metadata` | GET | Retrieve Trust Registry metadata |
| `/entities/{entity_id}` | GET | Retrieve entity information |
| `/entities` | GET | List entities known to the Trust Registry (paginated, filterable) |
| `/entities/{entity_id}/authorizations` | GET | List authorizations held by an entity |
| `/ecosystems/{ecosystem_id}` | GET | Retrieve ecosystem information |
| `/ecosystems/{ecosystem_id}/recognitions` | GET | List ecosystems recognized by a given ecosystem |
| `/lookups/assuranceLevels` | GET | Discover supported assurance levels |
| `/lookups/authorizations` | GET | Discover available action+resource authorization pairs |
| `/lookups/didMethods` | GET | Discover supported DID methods |

See the [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) for full endpoint details, request/response schemas, and error codes.

# **Security Requirements**

## Transport Security

All TRQP endpoints **MUST** be served over HTTPS (TLS 1.2 or later).

## Response Signing

Trust Registries returning TRQP-compliant responses in the Ayra Trust Network **SHOULD** sign responses using JWS with keys controlled by the Trust Registry controller or operator.

::: note
The JWS signing mechanism (format, scope, and key discovery) is under active discussion. See [GitHub Issue #36](https://github.com/ayraforum/ayra-trust-registry-resources/issues/36) for current status. Until that mechanism is finalized, unsigned `application/json` responses remain conformant to the Ayra TRQP Profile API.
:::
