# Ayra Trust Registry Resources

This repository contains resources for implementers and organizations interested in connecting with the Ayra Trust Network. These resources include specifications, guides, tools, sample code, and conformance tests to help you understand and implement the requirements for interacting with the Ayra ecosystem.




## Normative Resources

* [TRQP v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/)
* [Swagger YAML](./swagger.yaml) - RESTful API specification describing the required endpoints for any TRQP-compliant registry in the network.
* [Profile](./profile.md) - Ayra Authority Verification Profile required to register into the Ayra Trust Network.



## Guides

* [Implementers Guide](./guides/implementers_guide.md) - Comprehensive guide for connecting to the Ayra Trust Network.
* [Playground Guide](./playground/playground.md) - Instructions for setting up and using the testing playground environment.
* [TRQP Alignment](./trqp/README.md) - Information about how the Ayra TRQP Profile aligns with and informs the TRQP efforts. 
* [Integration Playbook](./guides/integration_playbook.md) - creates an (early at time of writing) playbook/framework for systems integrators to consider as they bring new or existing systems of record online using the TRQP.


## Tools

* [EGF DID Creator](./tools/did_creator_ui.py) - Python tool to create an Ayra Profile-aligned DID for an ecosystem.
* [DID Peer Utils](./tools/did_peer_utils.py) - Utility functions for DID generation and resolution.

## Playground

The playground provides a working example environment with sample implementations:

* [Sample Trust Registry](./playground/trust-registry/) - Go implementation of a Trust Registry compliant with the TRQP specification.
* [Sample Verifier](./playground/verifier/) - Python implementation of a verifier that can query the Trust Registry.

## Tests

* [API Conformance Test](./tests/api_conformance_test.py) - Tool for testing compliance of a Trust Registry endpoint with the TRQP specification.
* [DID Conformance Test](./tests/did_conformance_test.py) - Tool for checking conformance of the Ecosystem DID being registered. *(TODO)*
* [Ayra Authority Verification Profile Conformance Test](./tests/authority_profile_test.py) - Tool for checking that an ecosystem is compliant to register in the Ayra Trust Network. *(TODO)*

## Getting Started

1. Read the [Ayra Authority Verification Profile](https://ayraforum.github.io/ayra-trust-registry-resources/) to see understand the basic verification requirements. 
2. Read the [Implementers Guide](./guides/implementers_guide.md) to understand the core concepts of how to interact with the Ayra Trust Network according to your ecosystem. 
3. Set up the [Playground](./playground/playground.md) to experiment with the sample implementations.
4. Use the [Tools](./tools/) to create and manage DIDs for your ecosystem.
5. Run the [Tests](./tests/) to validate your implementation against the Ayra Trust Network requirements.

## Contributing

We welcome contributions to improve these resources. Please see [CONTRIBUTING](./CONTRIBUTING) for details on how to contribute.

## TRTF Key Links:

- [**TRQL 2.0 Specification DRAFT Specification**](https://trustoverip.github.io/tswg-trust-registry-protocol/)
  - [**github repo**](https://github.com/trustoverip/tswg-trust-registry-protocol/tree/main)