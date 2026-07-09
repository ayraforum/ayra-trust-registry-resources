# Ayra Trust Network Smoke Tests

This directory contains a lightweight smoke test for Ayra Trust Registry implementers.

## Available Test

### TRQP Profile Smoke Test

- [api_conformance_test.py](./api_conformance_test.py) - despite the historical filename, this is now a small smoke test for the current Ayra TRQP Profile API surface.

The script checks that an implementation exposes the current profile endpoints and returns profile-shaped JSON when those endpoints return `200`:

- `POST /authorization`
- `POST /recognition`
- `GET /metadata`
- `GET /lookups/assuranceLevels`
- `GET /lookups/authorizations`
- `GET /lookups/didMethods`

It accepts expected unavailable/auth responses (`401`, `404`, and `501` for optional extension endpoints) so members can use it early while standing up a registry.

## When to use this smoke test

Use this script when you want a quick local sanity check that your Trust Registry is wired to the current Ayra profile endpoint shape.

Good uses:

1. Checking that your base URL is reachable.
2. Confirming you implemented the current `POST /authorization` and `POST /recognition` request/response shapes.
3. Confirming top-level lookup routes use `/lookups/...` and not older nested paths.
4. Running a fast pre-flight before deeper interoperability testing.

## When not to use this smoke test

Do not use this script as certification or as the full Ayra conformance process. It does not verify credential issuance, holder/verifier flows, agent interoperability, protocol state machines, evidence reporting, negative cases, or full TRQP behavior.

For advanced conformance and interoperability work, use the Ayra Conformance Test Suite instead:

https://github.com/ayraforum/conformance-test-suite

## Requirements

- Python 3.7 or higher
- `requests`

Install the Python dependency if needed:

```bash
python -m pip install requests
```

## Usage

Run the smoke test against your Trust Registry base URL:

```bash
python api_conformance_test.py --base-url <your-trust-registry-base-url>
```

If the target registry requires bearer-token authentication, pass a token with:

```bash
python api_conformance_test.py --base-url <your-trust-registry-base-url> --bearer-token <token>
```

You can override the example identifiers and PARC values used by the POST checks:

```bash
python api_conformance_test.py \
  --base-url <your-trust-registry-base-url> \
  --entity-id did:example:issuer \
  --recognition-entity-id did:example:trust-registry \
  --authority-id did:example:ecosystem \
  --authorization-action issue \
  --authorization-resource credential \
  --recognition-action recognize \
  --recognition-resource trust-registry
```

## Contributing New Tests

Keep this repository's test script intentionally small. Add only smoke-level checks that help members catch endpoint-shape drift quickly.

If you need deeper conformance, interoperability, credential-flow, or protocol-state validation, contribute that work to the Ayra Conformance Test Suite:

https://github.com/ayraforum/conformance-test-suite
