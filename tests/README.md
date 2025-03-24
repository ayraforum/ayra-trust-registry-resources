# Ayra Trust Network Conformance Tests

This directory contains tests to validate implementations against the Ayra Trust Network requirements.

## Available Tests

### API Conformance Test

- [api_conformance_test.py](./api_conformance_test.py) - Tests a Trust Registry endpoint against the TRQP specification to verify compliance.

### Planned Tests (TODO)

- [did_conformance_test.py](./did_conformance_test.py) - Will check conformance of an Ecosystem DID that is being registered.
- [authority_profile_test.py](./authority_profile_test.py) - Will check that an ecosystem is compliant to register in the Ayra Trust Network.

## Requirements

- Python 3.7 or higher
- Dependencies required by the specific test scripts

## Usage

### API Conformance Test

The API Conformance Test verifies that your Trust Registry implementation meets the requirements specified in the TRQP specification.

```bash
python api_conformance_test.py --endpoint <your-trust-registry-endpoint>
```

### Running Tests During Development

These tests can be used during development to ensure your implementation remains compliant as you make changes. They can also be used as part of a CI/CD pipeline to continuously validate your implementation.

## Contributing New Tests

If you would like to contribute additional tests, please follow these guidelines:

1. Ensure the test validates against the latest version of the specifications.
2. Include clear documentation on what the test verifies and how to run it.
3. Follow the contribution process outlined in [CONTRIBUTING](../CONTRIBUTING).
