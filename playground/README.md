# Ayra Trust Network Playground

This directory contains a complete playground environment for experimenting with the Ayra Trust Network. It includes sample implementations of a Trust Registry and Verifier that demonstrate the TRQP (Trust Registry Query Protocol) in action.

## Components

- [Trust Registry](./trust-registry/) - A Go implementation of a TRQP-compliant Trust Registry
- [Verifier](./verifier/) - A Python implementation of a Verifier that can query Trust Registries
- [playground.md](./playground.md) - Detailed guide for setting up and using the playground

## Quick Start

The easiest way to run the playground is using Docker Compose:

```bash
docker-compose up
```

This will start all services:
- Ayra Trust Registry: http://localhost:8082
- Ecosystem Trust Registry: http://localhost:8083
- Verifier UI: http://localhost:8501

## Playground Scenarios

The playground allows you to experiment with several key scenarios:

1. **Trust Registry Operation** - Explore how a Trust Registry manages authorization data
2. **Ecosystem Recognition** - Test how one ecosystem recognizes another
3. **Authorization Verification** - Verify if an entity is authorized within an ecosystem

## Documentation

For detailed instructions on setting up and using the playground, see [playground.md](./playground.md).

## Architecture

The playground implements a simplified version of the Ayra Trust Network architecture:

```
┌────────────────┐     Recognition     ┌────────────────┐
│                │◄────────────────────┤                │
│  Ayra Trust    │                     │   Ecosystem    │
│   Registry     │                     │  Trust Registry│
│                │                     │                │
└────────────────┘                     └────────────────┘
         ▲                                      ▲
         │                                      │
         │ Recognition                          │ Authorization
         │ Query                                │ Query
         │                                      │
         │                                      │
      ┌──┴──────────────────────────────────────┴──┐
      │                                             │
      │               Verifier                      │
      │                                             │
      └─────────────────────────────────────────────┘
```

## Customizing

You can customize the playground by:

1. Modifying the registry data in `trust-registry/data/registry.json`
2. Extending the verifier's UI in `verifier/ui.py`
3. Configuring environment variables in `docker-compose.yaml`

## Development

For active development, you may prefer running the components manually:

1. Run the Trust Registries:
   ```bash
   cd trust-registry
   go mod tidy
   go run main.go --port=8082 --registry-name=TR-1
   ```
   
   In another terminal:
   ```bash
   cd trust-registry
   go run main.go --port=8083 --registry-name=TR-2
   ```

2. Run the Verifier:
   ```bash
   cd verifier
   pip install -r requirements.txt
   streamlit run ui.py
   ```
