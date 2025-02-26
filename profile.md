# **Ayra TRQP Implementation Profile**

This specification introduces the Ayra TRQP Profile that will be used to describe the Ayra Trust Network. 

| Author(s) | Andor Kesselman |
| :---- | :---- |
| **Email** | andor.kesselman@ayra.forum |
| **ID** | Authority Verification Interoperability Profile |
| **Description** | This RFC defines the interoperability requirements for  inter and intra ecosystem authority verification. This RFC impacts the design and implementation of the Ayra Metaregistry Network as well as Trust Registry vendors who wish their systems to interact..  |
| **Impact** | Critical |
| **Audience** | Implementors of Trust Registries: Consumers using TRQP queries to get answers about the ecosystems they are accessing. Providers integrating their system of record into the Ayra Trust Network, by adding TRQP Swagger API to their system \- directly, or via a Bridge pattern. |
| **Version** | **Draft v0.0.2** |
| **Table Of Contents** |  [Profile Overview](#profile-overview) [Identifier Requirements](#identifier-requirements) [Security and Privacy Requirements](#security-and-privacy-requirements) [Protocol Requirements](#protocol-requirements) [Roles](#roles) [Sample Pattern](?tab=t.q9xo7eqyr0bz#heading=h.u96dh747m6a) [Versioning and Backwards Compatibility](#versioning-and-backwards-compatibility)  |

# **Profile Overview**  {#profile-overview}

| Component | Authority Verification Profile API Based |
| :---- | :---- |
| **Trust Establishment Core Protocol** | Trust Registry Query Protocol (TRQP) |
| **TRQP Binding**  | RESTful Binding |
| **Ecosystem Identifiers** | Decentralized Identifiers ( did:webvh ) |
| **Trust Registry Identifiers** | Decentralized Identifiers ( did:webvh ) |
| **Cluster Identifiers** | Decentralized Identifiers ( did:webvh ) |
| **Ecosystem Governance Framework Resolution Mechanism** | HTTP Human Readable URI.  |
| **Authorization Data Model** | String |
| **DateTime Format** | [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) in UTC Time |
| **Reference Propagation Method** | TODO |
| **Authorized registries lookup protocol** | Within DID Document |


# **Identifier Requirements** {#identifier-requirements}

## **Ecosystem Identifier**

All Ecosystem Identifiers MUST be one of [Ayra Trust Network Valid DID Methods](#ayra-trust-network-valid-did-methods) with *AT LEAST* *two* required
service endpoints that conform to the [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile/blob/main/spec.md)
specification. 

1. A service endpoint that points to the Ecosystem Governance Framework’s documentation. The service profile url pointer is to [https://ayra.forum/profiles/trqp/egfURI/v1](https://ayra.forum/profiles/trqp/egfURI/v1) with hash \<TODO\>.  
2. A service endpoint that points to the DID of the Trust Registry that is TRQP enabled. The service profile url pointer is to [https://ayra.forum/profiles/trqp/tr/v1](https://ayra.forum/profiles/trqp/egfURI/v1) with hash \<TODO\>.  
   

Only valid ecosystem controllers are allowed to register the ecosystem with the
Ayra Trust Network. 

## **Trust Registry Identifier**

All Trust Registries MUST be a DID with at least *one* service endpoint with one
service profile. The service profile url pointer is to
[https://ayra.forum/profiles/trqp/tr/v1](https://ayra.forum/profiles/trqp/egfURI/v1)
with hash \<TODO\>. 

## **Cluster Identifier**

All Cluster Identifiers MUST be a DID with at least *one* service endpoint with
one service profile.The service profile url pointer is to
[https://ayra.forum/profiles/trqp/tr/v1](https://ayra.forum/profiles/trqp/egfURI/v1)
with hash \<TODO\>.

All uris defined in the service profile MUST describe valid trust metaregistries for the cluster.  

## **Ayra Trust Network Valid DID Methods** {#ayra-trust-network-valid-did-methods}

Currently, the Ayra Trust Network only accepts **did:webvh**.

# **Security and Privacy Requirements** {#security-and-privacy-requirements}

### **Trust Registries**

All Trust Registries returning a TRQP compliant response in the Ayra Trust
Network MUST return a JWS with the signature derived from the controller of the
DID document of the Trust Registry. 

### **Clusters**

All Ayra recognized clusters SHOULD support a description of how they manage
their keys for the DID Document and the metaregistries that serve the state of
the cluster.


# **Protocol Requirements** {#protocol-requirements}

All Trust Registries **MUST** serve the [RESTful
binding](?tab=t.0#heading=h.n2gndmivxfsb) per the specification. 

All required information **MUST** be shared through the credential *except* the
Ayra Trust Network’s DID. The ATN DID **MUST** be configured to : 

**did:webvh:ayra.forum** 

Valid metaregistries under the Ayra Trust Network are currently hosted at
did:webvh:arya.forum\#valid-trust-registries

# **Roles** {#roles}

| Persona | Description |
| :---- | :---- |
| **TRQP API Provider** | Vendors that supply a trust registry query protocol (TRQP) service on behalf of an ecosystem.   |
| **Ayra Metaregistry Operators** | The set of metaregistry operators that serve the Ayra Trust Network state by relaying recognized ecosystems.    |
| **Verifier** | The end authority verifier that is interested in verifying not only the cryptography, but the validity of the author for the set of claims.  |
| **Ecosystem** | Ecosystems will leverage the TR Vendors to manage their authority state. Each ecosystem must have sovereignty over their authority state.  |

# **Versioning and Backwards Compatibility** {#versioning-and-backwards-compatibility}

When the profile version is updated, the service profile document will also
update, providing a hash. 

Backward compatibility requirements will be determined by future updates.

# **Authorized registries lookup protocol**

The **Authorized Registries Lookup** is a mechanism by which an ecosystem
designates the **Trust Registries** that serve its state. This lookup provides a
verifiable way to discover the registries that an ecosystem recognizes as
authoritative for verifying identities, credentials, and other trust-related
information.

### **Definition within the Ecosystem's DID**

This lookup is explicitly defined within the ecosystem’s **Decentralized
Identifier (DID)**. It includes a **service endpoint** that references the **DID
of the Trust Registry**, which is **TRQP-enabled** (Trust Registry Query
Protocol). This endpoint enables automated discovery and validation of trust
registries within the ecosystem.

### **Service Endpoint**

The ecosystem’s DID includes a service endpoint structured as follows:

* **Service Type**: `TrustRegistryService`  
* **Service Endpoint**: A DID reference pointing to the **Trust Registry**  
* **Service Profile URL**: A pointer to the **service profile definition**,
  hosted at:

```
https://ayra.forum/profiles/trqp/tr/v1
```

  * This URL specifies the capabilities and structure of the TRQP-enabled Trust Registry.  
  * A specific **content hash** (`<TODO>`) ensures the integrity and versioning
    of the profile.

# **Additional API Requirements**

 Described
 [here](./swagger.yaml)

* /ecosystems/{ecosystem\_did}/lookups/assuranceLevels : A list of available assurance levels.
* /ecosystems/{ecosystem\_did}/lookups/authorizations: A list of available authorization types.
* /egfs/{ecosystem\_did}/lookups/didmethods: A list of supported DID Methods.
* /entities/{entity\_id}: Additional entity information.
