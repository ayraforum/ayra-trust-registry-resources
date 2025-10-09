

# Ayra Implementation Guide: TRQP Consumer 

## SCOPE

This guide is focused on providing implementation guidance about steps required to use the Trust Registry Query Protocol v2.0 (PR02) as a consumer. 

## Core + Profile

Ayra extends the TRQP to add queries that go beyond the TRQP "core" protocol. These are added to make traversal and low-level discovery feasible. 

### TRQP Core

The TRQP v2.0 PR02 must be supported. This requires two endpoints:

* `/authorization`
* `/recognition`

### Ayra Profile

The Ayra Profile extends the TRQP by adding multiple additional queries that make integration simpler. 

## Information Needed

To consume information from an Ayra Trust Network ecosystem you will need some mandatory and optional information.

### Mandatory

* **The Ecosystem ID** (`ecosystem_id`) of the ecosystem that you are working with. 
  * This `ecosystem_id` is the foundational piece as the ecoystem is the authority for the questions being asked. i.e. if you're asking the wrong ecosystem, you're starting from the wrong point. 
* **Trust Registry Endpoint** - the URI (https initially or DIDComm when binding exists) for that ecosystem. 
* **The Entity** that you will be querying the trust registry about. This typically will come from a credential you have received, or a communication from the entity that you are checking up on.
* The **Assertion** that you are testing (aka Authorization) that are active in the ecoystem. These will be used in the `assertion_id` value.
  * The Ayra Profile adds the ability to "discover" the list of authorizations that an ecosystem supports.

### Optional

* **Namespacing for Assertions** - the `assertion_id` values are, at the protocol level, opaque strings. 
  * At the implementation level they may benefit from meaning and human readability. 

> **NOTE:** Ayra Cards has a defined namespace. 


# Two Main Queries: Authorization and Recognition

the TRQP has two queries at its core: Authorization and Recognition

## Authorization Query

The **Authorization** (`/authorization`) query asks 
> **"Does EntityX have AuthorizationY under EcosystemZ?"**

## Recognition Query

The **Recognition** (`/recognition`) query is about linking ecosystems. This is a cross-recognition - basically one-way statements:

* EcosystemA acknowledges that EcosystemC has AuthorityB
  * e.g. "Canada acknowledges Japan's Education Ecosystem as authoritative for higher-education credentials."
* EcosystemC acknowledges that EcosystemA has AuthorityD
  * e.g. "Japan acknowledges Canada's Education Ecosystem as authoritative for university degrees." NOTE: There are differnt assertions about authority here. This allows each ecosystem to support an assertion-by-assertion granularity.

Stated in relatively plain English:

> **Does EcosytemA hold authorityB according to EcosystemC? **
> 

Now, with parameters that map to the TRQP `/recognition` endpoint:

> **Does EcosytemA (`entity_id`) hold authorityB (`assertion_id`) according to EcosystemC (`authority_id`)? **






> **SUGGESTION** use `trustregistry_id` even though we are talking to it????




* query is ab