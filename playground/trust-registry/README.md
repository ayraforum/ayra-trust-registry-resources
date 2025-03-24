# Trust Registry Reference Implementation

This directory contains a simple reference implementation of a Trust Registry that supports the TRQP (Trust Registry Query Protocol) specification. The registry is managed using a Git JSON document and provides a complete implementation of the TRQP API.

## Features

- Complete TRQP API implementation with Redoc Frontend documentation
- Registry data stored in a simple JSON file (`data/registry.json`)
- Support for multiple Ecosystem Governance Frameworks (EGFs)
- Organization and Ecosystem registration
- Sample namespacing implementation

## Design Philosophy

This implementation is intentionally kept as simple as possible to serve as a clear reference for the minimum viable implementation required for TRQP compliance. It focuses on the core functionality needed for Phase 1 of the Ayra Trust Network.

## Data Model

The registry data is stored in `data/registry.json`. This file defines:

- Trust Registry information
- Registered organizations and ecosystems
- Authorization mappings
- Namespace definitions

## Running the Trust Registry

### Using Docker (Recommended)

From the parent playground directory:
```bash
docker-compose up -d
```

### Manual Setup

1. Ensure Go is installed on your system
2. Initialize the Go modules:
   ```bash
   go mod tidy
   ```
3. Run the application:
   ```bash
   go run main.go
   ```

The service will be available at http://localhost:8082 by default.

## Example Queries

### Get Entity Status

```bash
curl http://localhost:8082/entities/did:web:samplenetwork.foundation
```

Response:
```json
{
  "entityDataValidity": {
    "validFromDT": "2024-09-10T12:00:00Z",
    "validUntilDT": "2025-09-10T12:00:00Z"
  },
  "entityVID": "did:web:samplenetwork.foundation",
  "governanceFrameworkVID": "",
  "primaryTrustRegistryVID": "did:web:samplenetwork.foundation",
  "registrationStatus": {
    "detail": "",
    "status": "current"
  },
  "secondaryTrustRegistries": []
}
```

### Get Namespace Lookup

```bash
curl 'http://localhost:8082/lookup/namespaces?egfURI=did:web:samplenetwork2.com'
```

Response:
```json
["foundation.samplenetwork.certified.person.verify","foundation.samplenetwork.certified.person.issue"]
```

## Customizing the Trust Registry

To customize the registry for your needs:

1. Edit the `data/registry.json` file to define your own organizations, ecosystems, and namespaces
2. Modify the API handlers in the `api/` directory if you need to extend the functionality
3. Update the `main.go` file to configure your specific deployment requirements

## API Documentation

The API documentation is available at the `/redoc.html` endpoint when the service is running.
