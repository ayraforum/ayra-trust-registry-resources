# Ayra Trust Registry Resources

This repository contains resources for implementers and organizations interested in connecting with the Ayra Trust Network. These resources include specifications, guides, and API definitions to help you understand and implement the requirements for interacting with the Ayra ecosystem.

## API Specifications

Interactive Swagger UI rendering of the TRQP and Ayra Profile API:

- [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html) -- TRQP v2.0 core endpoints (`trqp-core` tag) and Ayra extension endpoints (`ayra-extension` tag)

## Normative Resources

- [TRQP v2.0 Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/) -- The Trust Registry Query Protocol specification
- [Ayra TRQP Profile API](./trqp_ayra_profile_swagger.yaml) -- OpenAPI specification covering TRQP v2.0 core and Ayra extensions
- [Ayra Authority Verification Profile](./spec/profile.md) -- Profile required to register into the Ayra Trust Network

## Guides

- [Implementers Guide](./guides/implementers_guide.md) -- Comprehensive guide for connecting to the Ayra Trust Network, including conformance checklist, request/response examples, and integration patterns.
- [TRQP Alignment](./trqp/README.md) -- How the Ayra TRQP Profile aligns with and extends TRQP v2.0.

## Schemas

- [TRQP JSON Schemas](./trqp/schema/) -- JSON Schema definitions for TRQP v2.0 authorization and recognition queries and responses.
- [Ayra Metadata Schema](./schema/ayra_metadata.jsonschema) -- JSON Schema for Ayra Trust Registry metadata.

## Getting Started

1. Read the [Ayra Authority Verification Profile](https://ayraforum.github.io/ayra-trust-registry-resources/) to understand the verification requirements.
2. Read the [Implementers Guide](./guides/implementers_guide.md) to understand core concepts and how to integrate with the Ayra Trust Network.
3. Review the [API Specifications](#api-specifications) to understand the endpoints, request/response formats, and error handling.

## Contributing

We welcome contributions to improve these resources. Please see [CONTRIBUTING](./CONTRIBUTING) for details on how to contribute.

## Key Links

- [TRQP v2.0 Specification](https://trustoverip.github.io/tswg-trust-registry-protocol/)
- [TRQP Specification GitHub Repository](https://github.com/trustoverip/tswg-trust-registry-protocol/tree/main)
