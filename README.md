# Ayra Trust Registry Resources

The following resources are designed to support implementers and those
interested in connecting with the Ayra Trust Network. Many of these resources
are non-normative and serve as guides to help you understand the steps needed to
    interact with your ecosystem.

## Normative Resources
* [Swagger YAML](./swagger.yaml) - RESTFul specification to describe the required endpoints for any TRQP compliant registry in the network.
* [Profile](./profile.md) - Ayra Authority Verification Profile required to register into the Ayra Trust Network.

## [Guides](./guides)
* [Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/) - Implementation guide to connect to the Ayra Trust Network.
* [Playground Guide](https://ayraforum.github.io/ayra-trust-registry-resources/playground/) -- How to run the playground

## [Tools](./tools)
* [EGF DID Creator](./tools/did_creator_ui.py) -- Create an Ayra Profile aligned DID for an ecosystem.  (Python)

## [Playground](./playground)
* [Sample Trust Registry](./playground/trust-registry) -- Sample Trust Registry Code To Run (Go)
* [Sample Verifier](./playground/verifier) -- Sample Verifier Code To Run (Python)

## [Tests](./tests)
* [API Conformance Test](./tests/api_conformance_test.py) - Conformance Testing Tool for testing a Trust Registry endpoint. (Python)
* [DID Conformance Test](./tests/did_conformance_test.py) - Checks conformance of the Ecosystem DID that is being registered. (TODO) 
* [Ayra Authority Verification Profile Conformance Test](tests/authority_profile_test.py) -- Checks that an ecosystem is compliant to register in the Ayra Trust Network `TODO`
