# **Ayra TRQP Implementation Profile**

This specification introduces the Ayra TRQP Profile that will be used to describe the Ayra Trust Network. 

| Author(s) | Andor Kesselman |
| :---- | :---- |
| **Email** | andor.kesselman@ayra.forum |
| **ID** | Authority Verification Interoperability Profile |
| **Description** | This RFC defines the interoperability requirements for  inter and intra ecosystem authority verification. This RFC impacts the design and implementation of the Ayra Metaregistry Network as well as Trust Registry vendors who wish their systems to interact..  |
| **Audience** | Implementors of Trust Registries: Consumers using TRQP queries to get answers about the ecosystems they are accessing. Providers integrating their system of record into the Ayra Trust Network, by adding TRQP Swagger API to their system \- directly, or via a Bridge pattern. |
| **Version** | **Draft v0.0.2** |
| **Table Of Contents** |  [Profile Overview](#profile-overview) [Identifier Requirements](#identifier-requirements) [Security and Privacy Requirements](#security-and-privacy-requirements) [Protocol Requirements](#protocol-requirements) [Roles](#roles) [Sample Pattern](?tab=t.q9xo7eqyr0bz#heading=h.u96dh747m6a) [Versioning and Backwards Compatibility](#versioning-and-backwards-compatibility)  |

Learn more at the [Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/)

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

## **Ecosystem Identifiers**

All Ecosystem Identifiers MUST be one of [Ayra Trust Network Valid DID Methods](#ayra-trust-network-valid-did-methods) with *AT LEAST* *two* required
service endpoints that conform to the [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile/blob/main/spec.md)
specification. 

1. A service endpoint that points to the Ecosystem Governance Framework’s documentation. The service profile url pointer is to [https://ayra.forum/profiles/trqp/egfURI/v1](https://ayra.forum/profiles/trqp/egfURI/v1) with hash \<TODO\>.  
2. A service endpoint that points to the DID of the Trust Registry that is TRQP enabled. The service profile url pointer is to [https://ayra.forum/profiles/trqp/tr/v1](https://ayra.forum/profiles/trqp/egfURI/v1) with hash \<TODO\>.  

Only valid ecosystem controllers are allowed to register the ecosystem with the
Ayra Trust Network. 

## **Trust Registry Identifier**

All Trust Registries MUST be a DID with at least *one* service endpoint with one
service profile. The [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile) url pointer is to
[https://ayra.forum/profiles/trqp/tr/v1](https://ayra.forum/profiles/trqp/egfURI/v1)
with hash \<TODO\>. 

## **Cluster Identifier**

All Cluster Identifiers MUST be a DID with at least *one* service endpoint with
one service profile.The [service profile](https://github.com/trustoverip/tswg-trust-registry-service-profile) url pointer is to
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

Valid trust registries that serve the metaregistry state of the Ayra Trust
Network will be represented as the TrustRegistry service endpoints in the DID
Document.

# **Roles** 

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

TRQP versioning is handled by the service profiles.

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

<details>
<summary>Click to View the OpenAPI 3.0 Specification</summary>

```yaml
openapi: 3.0.1
info:
  title: Ayra TRQP Profile API
  version: 1.0.0
  description: >
    This specification defines a RESTful TRQP profile for use in the Ayra Trust Network.
    It includes endpoints for retrieving Trust Registry metadata,
    authorization data, verifying entity authorization status,
    and checking ecosystem recognition.

servers:
  - url: https://example-trust-registry.com
    description: Production server (example)
  - url: https://sandbox-trust-registry.com
    description: Sandbox server (example)

tags:
  - name: trqp
    description: TRQP Compliant Queries
  - name: extensions
    description: Ayra Extensions to TRQP

paths:
  /metadata:
    get:
      summary: Retrieve Trust Registry Metadata
      tags:
        - trqp
      description: Returns Trust Registry Metadata as a JSON object.
      operationId: getTrustRegistryMetadata
      parameters:
        - name: egf_did
          in: query
          required: false
          description: >
            An optional identifier specifying which ecosystem's
            metadata should be retrieved.
          schema:
            type: string
      responses:
        '200':
          description: Successfully retrieved Trust Registry Metadata.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TrustRegistryMetadata'
        '404':
          description: Metadata not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /entities/{entity_id}:
    get:
      summary: Retrieve Entity Information
      tags:
        - extensions
      description: Retrieves information about a specific entity.
      operationId: getEntityInformation
      parameters:
        - name: entity_id
          in: path
          required: true
          description: A unique identifier for the entity.
          schema:
            type: string
      responses:
        '200':
          description: Entity information successfully retrieved.
          content:
            application/json:
              schema:
                type: object
                description: A JSON object containing entity information.
        '404':
          description: Entity not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /entities/{entity_id}/authorization:
    get:
      summary: Check Entity Authorization Status
      tags:
        - trqp
      description: >
        Determines if the specified entity (entity_id) is authorized
        under the given authorization identifier (authorization_id)
        within the specified governance framework (ecosystem_did).
        Optionally, returns a list of authorizations if all is true.
      operationId: checkAuthorizationStatus
      parameters:
        - name: entity_id
          in: path
          required: true
          description: Unique identifier of the entity.
          schema:
            type: string
        - name: authorization_id
          in: query
          required: true
          description: Authorization identifier to evaluate.
          schema:
            type: string
        - name: ecosystem_did
          in: query
          required: true
          description: Unique identifier of the governance framework.
          schema:
            type: string
        - name: all
          in: query
          required: true
          description: Whether to return a list of authorizations.
          schema:
            type: boolean
        - name: time
          in: query
          required: false
          description: >
            ISO8601/RFC3339 timestamp for authorization status
            evaluation. Defaults to the current time if omitted.
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: Authorization status successfully retrieved.
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/AuthorizationResponse'
                  - type: array
                    items:
                      $ref: '#/components/schemas/AuthorizationResponse'
        '404':
          description: Entity not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /registries/{ecosystem_did}/recognition:
    get:
      summary: Check Ecosystem Recognition
      tags:
        - trqp
      description: >
        Verifies if the specified ecosystem (egf_target) is recognized
        under the given governance framework (egf_source).
      operationId: checkEcosystemRecognition
      parameters:
        - name: ecosystem_did
          in: path
          required: true
          description: Unique identifier of the ecosystem being queried.
          schema:
            type: string
        - name: egf_did
          in: query
          required: true
          description: >
            Unique identifier of the governance framework. Defaults to
            the trust registry’s own if none is supplied.
          schema:
            type: string
        - name: time
          in: query
          required: false
          description: >
            RFC3339 timestamp indicating when recognition is checked.
            Defaults to "now" on the system being queried.
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: Ecosystem recognition successfully verified.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RecognitionResponse'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '404':
          description: Ecosystem not recognized or not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /ecosystems/{ecosystem_did}/recognitions:
    get:
      summary: List Recognized Ecosystems
      tags:
        - extensions
      description: >
        Retrieves a collection of recognized ecosystems for a
        specified governance framework.
      operationId: listEcosystemRecognitions
      parameters:
        - name: ecosystem_did
          in: path
          required: true
          description: Unique identifier of the ecosystem being queried.
          schema:
            type: string
        - name: egf_did
          in: query
          required: false
          description: >
            Optional identifier of the governance framework to filter
            the response. 
          schema:
            type: string
        - name: time
          in: query
          required: false
          description: >
            RFC3339 timestamp indicating when recognition is checked.
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: Ecosystem recognitions retrieved successfully.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/RecognitionResponse'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '404':
          description: Ecosystem not recognized or not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /ecosystems/{ecosystem_did}/lookups/assuranceLevels:
    get:
      summary: Lookup Supported Assurance Levels
      tags:
        - extensions
      description: >
        Retrieves the supported assurance levels for the specified
        ecosystem.
      operationId: lookupSupportedAssuranceLevels
      parameters:
        - name: ecosystem_did
          in: path
          required: true
          description: Unique identifier of the ecosystem being queried.
          schema:
            type: string
      responses:
        '200':
          description: Supported assurance levels retrieved successfully.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AssuranceLevelResponse'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '404':
          description: Ecosystem not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /ecosystems/{ecosystem_did}/lookups/authorizations:
    get:
      summary: Lookup Authorizations
      tags:
        - extensions
      description: >
        Performs an authorization lookup based on the provided
        ecosystem identifier.
      operationId: lookupAuthorizations
      parameters:
        - name: ecosystem_did
          in: path
          required: true
          description: Ecosystem identifier.
          schema:
            type: string
      responses:
        '200':
          description: A list of authorization responses.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/AuthorizationResponse'
        '404':
          description: Entity not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /egfs/{ecosystem_did}/lookups/didmethods:
    get:
      summary: Lookup Supported DID Methods
      tags:
        - extensions
      description: >
        Retrieves the supported DID Methods recognized by this trust
        registry for the specified ecosystem governance framework.
      operationId: lookupSupportedDIDMethods
      parameters:
        - name: ecosystem_did
          in: path
          required: true
          description: Unique identifier of the ecosystem being queried.
          schema:
            type: string
      responses:
        '200':
          description: Supported DID Methods retrieved successfully.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/DIDMethodListType'
        '401':
          description: Unauthorized request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'
        '404':
          description: Ecosystem not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

components:
  schemas:
    ProblemDetails:
      type: object
      description: >
        A Problem Details object (RFC 7807).
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the problem type.
        title:
          type: string
          description: Short, human-readable summary of the problem.
        status:
          type: integer
          description: HTTP status code (e.g., 404).
        detail:
          type: string
          description: Human-readable explanation of the problem.
        instance:
          type: string
          format: uri
          description: URI reference identifying this specific occurrence.
      additionalProperties: true

    TrustRegistryMetadata:
      type: object
      properties:
        id:
          type: string
          description: Unique identifier of the Trust Registry.
        default_egf_did:
          type: string
          description: >
            Default EGF DID used if none is supplied in queries.
        description:
          type: string
          maxLength: 4096
          description: A description of the Trust Registry.
        name:
          type: string
          description: Human-readable name of the Trust Registry.
        controllers:
          type: array
          description: List of unique identifiers for controllers.
          items:
            type: string
          minItems: 1
      required:
        - id
        - description
        - name
        - controllers

    AuthorizationResponse:
      type: object
      properties:
        egf_did:
          type: string
          description: EGF DID this authorization response relates to.
        recognized:
          type: boolean
          description: Indicates if the entity is recognized by the TR.
        authorized:
          type: boolean
          description: Indicates if the entity holds the authorization.
        message:
          type: string
          description: Additional context for the authorization status.
        evaluated_at:
          type: string
          format: date-time
          description: Timestamp when the status was evaluated.
        response_time:
          type: string
          format: date-time
          description: Timestamp when the response was generated.
        expiry_time:
          type: string
          format: date-time
          description: Expiration timestamp (if any).
        jws:
          type: string
          description: Signed response (JWS) from the registry’s controller.
      required:
        - recognized
        - authorized
        - message
        - evaluated_at
        - response_time

    RecognitionResponse:
      type: object
      properties:
        recognized:
          type: boolean
          description: Indicates if the ecosystem is recognized.
        message:
          type: string
          description: Additional info about the recognition status.
        egf_did:
          type: string
          description: EGF DID this recognition applies to.
        evaluated_at:
          type: string
          format: date-time
          description: Timestamp when the status was evaluated.
        response_time:
          type: string
          format: date-time
          description: Timestamp when the response was generated.
        expiry_time:
          type: string
          format: date-time
          description: Expiration timestamp (if any).
        jws:
          type: string
          description: Signed response (JWS) from the registry’s controller.
      required:
        - recognized
        - message
        - evaluated_at
        - response_time

    AssuranceLevelResponse:
      type: object
      properties:
        egf_did:
          type: string
          description: EGF DID this assurance level applies to.
        assurance_level:
          type: string
          description: The assurance level (e.g. LOA2).
        description:
          type: string
          description: Details about the assurance level.
      required:
        - assurance_level
        - description

    DIDMethodType:
      type: object
      required:
        - identifier
      description: DID Method supported by the trust registry.
      properties:
        identifier:
          type: string
          description: Name or URI referencing the DID method.
        egf_did:
          type: string
          description: EGF DID that recognizes this DID method.
        maximumAssuranceLevel:
          $ref: "#/components/schemas/AssuranceLevelType"

    DIDMethodListType:
      type: array
      items:
        $ref: "#/components/schemas/DIDMethodType"

    AssuranceLevelType:
      type: object
      description: Defines a recognized assurance level in a trust registry.
      required:
        - identifier
        - name
        - description
      properties:
        identifier:
          type: string
          format: uri
        name:
          type: string
        description:
          type: string
```
</details>

