# **Ayra TRQP Profile**

This specification defines the Ayra TRQP Profile for the Ayra Trust Network. It profiles the [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) for use within the Ayra Trust Network.

| | |
| :---- | :---- |
| **Version** | v0.5.0-draft |
| **Audience** | Implementors of Trust Registries participating in the Ayra Trust Network -- both TRQP API Providers and TRQP Consumers (Verifiers). |

- [Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/) -- non-normative guidance, examples, and integration patterns
- [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) -- interactive API documentation (use tags to filter by `trqp-core` or `ayra-extension`)

# **Profile Overview**

| Component | Ayra Profile Requirement |
| :---- | :---- |
| **Core Protocol** | [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) |
| **TRQP Binding** | HTTPS RESTful Binding |
| **Query Model** | PARC: Principal (`entity_id`), Action (`action`), Resource (`resource`), Context (`authority_id` + `context`) |
| **Identifier Method** | `did:webvh` (all ecosystem, trust registry, and cluster identifiers) |
| **Ecosystem Governance Framework** | HTTP human-readable URI |
| **DateTime Format** | [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) in UTC (Z offset only) |
| **Error Format** | [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Problem Details |

# **Identifier Requirements**

## Ecosystem Identifiers

All Ecosystem Identifiers **MUST** be `did:webvh` DIDs with at least **two** service endpoints conforming to the [Trust Registry Service Profile](https://github.com/trustoverip/tswg-trust-registry-service-profile/blob/main/spec.md) specification:

1. **Ecosystem Governance Framework endpoint** -- points to the EGF documentation. Service profile URL: `https://ayra.forum/profiles/trqp/egfURI/v1`.
2. **Trust Registry endpoint** -- points to the DID of the TRQP-enabled Trust Registry that serves this ecosystem's state. Service profile URL: `https://ayra.forum/profiles/trqp/tr/v2`. Service type: `TrustRegistryService`.

Only valid ecosystem controllers are allowed to register the ecosystem with the Ayra Trust Network.

## Trust Registry Identifiers

All Trust Registry Identifiers **MUST** be `did:webvh` DIDs with at least **one** service endpoint. The [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile) URL pointer is `https://ayra.forum/profiles/trqp/tr/v2`.

## Cluster Identifiers

All Cluster Identifiers **MUST** be `did:webvh` DIDs with at least **one** service endpoint. The [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile) URL pointer is `https://ayra.forum/profiles/trqp/tr/v2`.

All URIs defined in the service profile **MUST** describe valid trust metaregistries for the cluster.

# **Protocol Requirements**

## TRQP v2.0 Compliance

All Trust Registries in the Ayra Trust Network **MUST** implement the [TRQP v2.0 HTTPS Binding](https://trustoverip.github.io/tswg-trust-registry-protocol/):

1. **`POST /authorization`** -- accept authorization queries and return responses conforming to the TRQP v2.0 schema.
2. **`POST /recognition`** -- accept recognition queries and return responses conforming to the TRQP v2.0 schema.

All queries use the PARC model with required fields: `entity_id`, `authority_id`, `action`, `resource`, and optional `context`.

All error responses **MUST** use [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Problem Details format with appropriate HTTP status codes (400, 401, 404, 500).

## Ayra Trust Network DID

The Ayra Trust Network DID is:

```text
did:webvh:ayra.forum
```

Valid trust registries that serve the metaregistry state of the Ayra Trust Network are represented as `TrustRegistryService` service endpoints in the ATN DID Document.

## Ayra Extension Endpoints

In addition to the TRQP v2.0 core endpoints, the Ayra Profile defines the following extension endpoints. These are **RECOMMENDED** for full Ayra Trust Network participation:

| Endpoint | Method | Description |
| :---- | :---- | :---- |
| `/metadata` | GET | Retrieve Trust Registry metadata |
| `/entities/{entity_id}` | GET | Retrieve entity information |
| `/entities/{entity_did}/authorizations` | GET | List authorizations held by an entity |
| `/ecosystems/{ecosystem_did}` | GET | Retrieve ecosystem information |
| `/ecosystems/{ecosystem_did}/recognitions` | GET | List ecosystems recognized by a given ecosystem |
| `/lookups/assuranceLevels` | GET | Discover supported assurance levels |
| `/lookups/authorizations` | GET | Discover available action+resource authorization pairs |
| `/lookups/didMethods` | GET | Discover supported DID methods |

See the [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) for full endpoint details, request/response schemas, and error codes.

# **Security Requirements**

## Transport Security

All TRQP endpoints **MUST** be served over HTTPS (TLS 1.2 or later).

## Response Signing

All Trust Registries returning a TRQP-compliant response in the Ayra Trust Network **MUST** return a JWS with the signature derived from the controller of the DID Document of the Trust Registry.

::: note
The JWS signing mechanism (format, scope, and key discovery) is under active discussion. See [GitHub Issue #36](https://github.com/ayraforum/ayra-trust-registry-resources/issues/36) for current status.
:::

## Cluster Key Management

All Ayra-recognized clusters **SHOULD** support a description of how they manage their keys for the DID Document and the metaregistries that serve the state of the cluster.
