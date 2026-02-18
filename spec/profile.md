# **Ayra Authority Verification Profile**

This specification defines the Ayra TRQP Profile used to describe the Ayra Trust Network. It profiles the [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) for use within the Ayra Trust Network.

| **ID** | Ayra TRQP Profile |
| **Description** | This specification defines the interoperability requirements for inter and intra ecosystem authority verification. It impacts the design and implementation of the Ayra Metaregistry Network as well as Trust Registry vendors who wish their systems to interact. |
| **Audience** | Implementors of Trust Registries: Consumers using TRQP queries to get answers about the ecosystems they are accessing. Providers integrating their system of record into the Ayra Trust Network, by adding TRQP API endpoints to their system -- directly, or via a Bridge pattern. |
| **Version** | **v0.5.0-draft** |
| **Table Of Contents** | [Profile Overview](#profile-overview) [Identifier Requirements](#identifier-requirements) [Security and Privacy Requirements](#security-and-privacy-requirements) [Protocol Requirements](#protocol-requirements) [Roles](#roles) [Versioning and Backwards Compatibility](#versioning-and-backwards-compatibility) |

Learn more at the [Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/)

## Resources

- [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) -- TRQP v2.0 core endpoints and Ayra extension endpoints (use tags to filter by `trqp-core` or `ayra-extension`)

# **Profile Overview**

| Component | Profile |
| :---- | :---- |
| **Core Protocol** | [Trust Registry Query Protocol (TRQP) v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/) |
| **TRQP Binding** | https RESTful Binding |
| **Query Model** | PARC: <br/>Principal (`entity_id`) <br/>Action (`action`) <br/>Resource (`resource`) <br/>Context (`authority_id` +[`context`]) |
| **Ecosystem Identifiers** | Decentralized Identifiers ( did:webvh ) |
| **Trust Registry Identifiers** | Decentralized Identifiers ( did:webvh ) |
| **Ecosystem Governance Framework Resolution** | HTTP Human Readable URI |
| **DateTime Format** | [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) in UTC Time (Z offset only) |
| **Error Format** | [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Problem Details |
| **Authorized Registries Lookup** | Within DID Document |

# **Identifier Requirements**

## **Ecosystem Identifiers**

All Ecosystem Identifiers MUST be one of [Ayra Trust Network Valid DID Methods](#ayra-trust-network-valid-did-methods) with *AT LEAST* *two* required service endpoints that conform to the [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile/blob/main/spec.md) specification.

1. A service endpoint that points to the Ecosystem Governance Framework's documentation. The service profile URL pointer is to `https://ayra.forum/profiles/trqp/egfURI/v1`.
2. A service endpoint that points to the DID of the Trust Registry that is TRQP enabled. The service profile URL pointer is to `https://ayra.forum/profiles/trqp/tr/v1`.

Only valid ecosystem controllers are allowed to register the ecosystem with the Ayra Trust Network.

## **Trust Registry Identifier**

All Trust Registries MUST be a DID with at least *one* service endpoint with one service profile. The [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile) URL pointer is to `https://ayra.forum/profiles/trqp/tr/v1`.

## **Cluster Identifier**

All Cluster Identifiers MUST be a DID with at least *one* service endpoint with one service profile. The [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile) URL pointer is to `https://ayra.forum/profiles/trqp/tr/v1`.

All URIs defined in the service profile MUST describe valid trust metaregistries for the cluster.

## **Ayra Trust Network Valid DID Methods**

Currently, the Ayra Trust Network only accepts **did:webvh**.

# **Security and Privacy Requirements**

### **Trust Registries**

All Trust Registries returning a TRQP compliant response in the Ayra Trust Network MUST return a JWS with the signature derived from the controller of the DID document of the Trust Registry.

### **Clusters**

All Ayra recognized clusters SHOULD support a description of how they manage their keys for the DID Document and the metaregistries that serve the state of the cluster.

# **Protocol Requirements**

## TRQP v2.0 Compliance

All Trust Registries in the Ayra Trust Network **MUST** implement the [TRQP v2.0 HTTPS Binding](https://trustoverip.github.io/tswg-trust-registry-protocol/). This requires:

1. **`POST /authorization`** -- Accept authorization queries and return authorization responses conforming to the TRQP v2.0 schema.
2. **`POST /recognition`** -- Accept recognition queries and return recognition responses conforming to the TRQP v2.0 schema.

All queries use the PARC model with required fields: `entity_id`, `authority_id`, `action`, `resource`, and optional `context`.

All error responses **MUST** use [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Problem Details format with appropriate HTTP status codes (400, 401, 404, 500).

## Ayra Trust Network Configuration

All required information **MUST** be shared through the credential *except* the Ayra Trust Network's DID. The ATN DID **MUST** be configured to:

**did:webvh:ayra.forum**

Valid trust registries that serve the metaregistry state of the Ayra Trust Network will be represented as the TrustRegistry service endpoints in the DID Document.

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

# **Roles**

| Persona | Description |
| :---- | :---- |
| **TRQP API Provider** | Vendors that supply a trust registry query protocol (TRQP) service on behalf of an ecosystem. |
| **Ayra Metaregistry Operators** | The set of metaregistry operators that serve the Ayra Trust Network state by relaying recognized ecosystems. |
| **Verifier** | The end authority verifier that is interested in verifying not only the cryptography, but the validity of the author for the set of claims. |
| **Ecosystem** | Ecosystems will leverage the TR Vendors to manage their authority state. Each ecosystem must have sovereignty over their authority state. |

# **Versioning and Backwards Compatibility**

When the profile version is updated, the service profile document will also update, providing a hash.

Backward compatibility requirements will be determined by future updates.

TRQP versioning is handled by the service profiles.

# **Authorized Registries Lookup Protocol**

The **Authorized Registries Lookup** is a mechanism by which an ecosystem designates the **Trust Registries** that serve its state. This lookup provides a verifiable way to discover the registries that an ecosystem recognizes as authoritative for verifying identities, credentials, and other trust-related information.

### **Definition within the Ecosystem's DID**

This lookup is explicitly defined within the ecosystem's **Decentralized Identifier (DID)**. It includes a **service endpoint** that references the **DID of the Trust Registry**, which is **TRQP-enabled**. This endpoint enables automated discovery and validation of trust registries within the ecosystem.

### **Service Endpoint**

The ecosystem's DID includes a service endpoint structured as follows:

- **Service Type**: `TrustRegistryService`
- **Service Endpoint**: A DID reference pointing to the **Trust Registry**
- **Service Profile URL**: A pointer to the **service profile definition**, hosted at:

```
https://ayra.forum/profiles/trqp/tr/v2
```

This URL specifies the capabilities and structure of the TRQP-enabled Trust Registry.
