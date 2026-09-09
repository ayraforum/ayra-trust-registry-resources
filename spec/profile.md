# **Ayra TRQP Profile**

This specification defines the Ayra TRQP Profile for the Ayra Trust Network. It profiles the [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) for use within the Ayra Trust Network.

# **Core Principle**

> The registry **informs** the decision.
>
> The relying party **makes** the decision.

TRQP provides authorization and recognition information. It does not make a relying party's trust, acceptance, or transaction decision.

| | |
| :---- | :---- |
| **Version** | v0.6.0-draft |
| **Audience** | Implementors of Trust Registries participating in the Ayra Trust Network -- both TRQP API Providers and TRQP Consumers (Verifiers). |

- [Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/) -- non-normative guidance, examples, and integration patterns
- [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) -- normative OpenAPI documentation for the Ayra TRQP Profile API surface (use tags to filter by `trqp-core` or `ayra-extension`)

# **Normative References and Source of Truth**

For this profile:

1. [TRQP v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) is authoritative for the core protocol model, HTTPS binding, and core field names.
2. [W3C DID Core](https://www.w3.org/TR/did-core/) is authoritative for DID, DID URI, DID method, DID controller, and DID Document semantics.
3. The [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) is authoritative for the Ayra API surface, request and response schemas, parameters, and status codes.
4. This document is authoritative for Ayra profile requirements and conformance policy.
5. The Implementers Guide is non-normative supporting material.

# **Profile at a Glance**

Ayra-conformant Trust Registries:

- **MUST** implement both TRQP core endpoints: `POST /authorization` and `POST /recognition`.
- **MUST** use TRQP-compatible `_id` field names, including `entity_id` and `authority_id`; these fields **MUST NOT** be renamed to `_did`.
- **MUST** represent all Ayra `_id` values as DID URI strings.
- **MUST** return RFC 7807 Problem Details for error responses, as required by TRQP v2.0. RFC 9457 is an informative forward-compatibility consideration and is not a requirement of this profile version.
- **MAY** apply rate limits and, when returning a rate-limit response, **MUST** use HTTP 429 with RFC 7807 Problem Details.
- **MAY** implement Ayra extension endpoints for metadata, entity discovery, ecosystem discovery, and lookups.
- **MUST** return HTTP 501 with Problem Details when an optional Ayra extension endpoint is not implemented.
- **SHOULD** sign responses with JWS where supported; the signing mechanism is still being finalized.

# **Profile Overview**

| Component | Ayra Profile Requirement |
| :---- | :---- |
| **Core Protocol** | [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) |
| **TRQP Binding** | HTTPS RESTful Binding |
| **Query Model** | PARC: Principal (`entity_id`), Action (`action`), Resource (`resource`), Context (`authority_id` + `context`) |
| **Identifier Method** | [DID URI](https://www.w3.org/TR/did-core/); supported DID methods are discoverable via `/lookups/didMethods`; `did:webvh` is preferred for higher assurance levels |
| **Ecosystem Governance Framework** | Identifier or URI discoverable via `authority_id` |
| **DateTime Format** | [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) in UTC (Z offset only) |
| **Error Format** | [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807.html) Problem Details, as required by TRQP v2.0. See "Problem Details Versioning and Forward Compatibility" for possible future RFC 9457 alignment. |

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

All core TRQP error responses **MUST** use [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807.html) Problem Details format with appropriate HTTP status codes as defined by the Ayra TRQP Profile API. JSON Problem Details responses **MUST** use the `application/problem+json` media type. Core TRQP endpoints use the status codes defined for `/authorization` and `/recognition` in the OpenAPI specification and **MUST NOT** return HTTP 501 to indicate non-support.

## Problem Details Versioning and Forward Compatibility

::: note
This subsection is informative. It records a possible future change and does not adopt RFC 9457 or change the conformance requirements of this profile. See [GitHub Issue #44](https://github.com/ayraforum/ayra-trust-registry-resources/issues/44) for discussion.
:::

The current Ayra TRQP Profile profiles TRQP v2.0. TRQP v2.0 normatively requires [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807.html) Problem Details. RFC 7807 therefore remains the applicable requirement for conformance to this version of the Ayra profile.

[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), published in July 2023, obsoletes RFC 7807 at the IETF level. It preserves the `application/problem+json` media type, the core `type`, `title`, `status`, `detail`, and `instance` members, and support for extension members. Its principal additions clarify handling of multiple problems and non-dereferenceable problem type URIs and establish a registry of common problem type URIs.

RFC 9457 is not normative for TRQP v2.0 or for this version of the Ayra profile. Support for RFC 9457 does not by itself establish conformance with a future TRQP or Ayra profile version; that version would need to adopt RFC 9457 expressly.

If a future TRQP version adopts RFC 9457, the corresponding Ayra profile version should:

- identify the applicable TRQP version and Problem Details RFC explicitly;
- define whether and how implementations can support both profile versions;
- update its OpenAPI description, conformance tests, examples, and implementation guidance together;
- preserve the established meaning of existing problem `type` URIs;
- test handling of unknown extension members, registered problem types, multiple reported problems, and non-dereferenceable type URIs; and
- document any compatibility expectations for RFC 7807-only consumers.

An implementation cannot determine which RFC governs a response merely from the `application/problem+json` media type or the core Problem Details members, because both RFCs use the same values. Any future transition must therefore be tied to an explicitly selected TRQP and Ayra profile version, rather than inferred from the error document.

Adopting RFC 9457 would not, by itself, add HTTP status codes such as `429 Too Many Requests` or define use of the `Retry-After` header. Those are separate HTTP binding and profile decisions. This profile defines 429 behavior independently below without adopting RFC 9457.

## HTTP Errors and Query Results

Consistent with the Core Principle, an HTTP error means that the TRQP query did not return authorization or recognition information. A consumer **MUST NOT** interpret an HTTP error, including a rate-limiting or temporary-service error, as `authorized: false` or `recognized: false`. Successful TRQP query results are information that a relying party may use when making its own trust decision.

## Rate Limiting

Trust Registries **MAY** apply rate limits to core TRQP and Ayra extension endpoints. When a Trust Registry returns an HTTP response because a request rate limit has been exceeded, it **MUST** use `429 Too Many Requests` as defined by [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html).

The 429 response:

- **MUST** contain an RFC 7807 Problem Details body using `Content-Type: application/problem+json`;
- **MUST** use `429` for the Problem Details `status` member when that member is present;
- **SHOULD** include a `Retry-After` response header when the registry can provide useful retry timing; and
- **MUST NOT** be stored by a cache.

The standard `about:blank` problem type **MAY** be used because HTTP 429 supplies the generic semantics. A registry **MAY** instead use a stable, documented problem `type` URI and **MAY** add problem-specific extension members. Consumers **MUST** ignore extension members they do not recognize and **MUST NOT** parse `title` or `detail` to determine retry timing.

Consumers **SHOULD** honor `Retry-After`. When it is absent, consumers should use bounded exponential backoff with jitter according to local policy. Consumers **MUST** treat 429 as a failure to obtain authorization or recognition information and **MUST NOT** interpret or cache it as `authorized: false` or `recognized: false`.

This 429 representation is compatible with both RFC 7807 and RFC 9457. Its use does not make RFC 9457 normative for the current profile.

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

The `/metadata` response shape and minimum required fields are defined by the Ayra TRQP Profile API. This profile intentionally does not duplicate the metadata schema.

# **Security Requirements**

## Transport Security

All TRQP endpoints **MUST** be served over HTTPS (TLS 1.2 or later).

## Response Signing

Trust Registries returning TRQP-compliant responses in the Ayra Trust Network **SHOULD** sign responses using JWS with keys controlled by the Trust Registry controller or operator.

::: note
The JWS signing mechanism (format, scope, and key discovery) is under active discussion. See [GitHub Issue #36](https://github.com/ayraforum/ayra-trust-registry-resources/issues/36) for current status. Until that mechanism is finalized, unsigned `application/json` responses remain conformant to the Ayra TRQP Profile API.
:::

# **Agent and Automation Notes**

Automated agents, documentation tools, and conformance tools should apply these interpretation rules:

- Treat TRQP v2.0, W3C DID Core, the Ayra TRQP Profile API, and this profile in the source-of-truth order listed above.
- Do not rename TRQP fields to `_did`. Ayra uses TRQP-compatible `_id` field names and constrains the values to DID URI strings.
- Do not assume only `did:webvh` and `did:web` are supported. Supported DID methods are registry- or authority-specific and discoverable through `GET /lookups/didMethods`.
- Do not treat optional Ayra extension endpoints as mandatory. Unsupported extension endpoints return HTTP 501 with Problem Details.
- Apply RFC 7807 to the current profile. Do not treat RFC 9457 as normative unless a later TRQP version and corresponding Ayra profile version explicitly adopt it.
- Treat HTTP 429 as an operational failure to obtain authorization or recognition information, honor `Retry-After` when supplied, and never interpret it as a negative answer.
- Do not treat JWS response signing as mandatory. Response signing is a **SHOULD** until the signing mechanism is finalized.
- JSON Schema files in this repository use the `.schema.json` extension.
