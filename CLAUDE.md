# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## TRQP Core 

The Trust Registry Query Protocol specification is located at: https://trustoverip.github.io/tswg-trust-registry-protocol/ 

### Maintained APIs

We need TWO key APIs - which can be in one Swagger file, and use OAS "tags" to differentiate:


* `trqp-core` - the core TRQP
* `ayra-extensions` - endpoints that are specific to the Ayra Trust Network Profile



## Repository Overview

This repository contains resources for implementing Trust Registry Query Protocol (TRQP) compliance with the Ayra Trust Network, including specifications, sample implementations, testing tools, and developer guides.

## Development Commands

### Documentation Development
- `npm run edit` - Start spec-up editor for documentation
- `npm run render` - Render documentation with spec-up (production mode)  
- `npm run dev` - Render documentation with spec-up (development mode)

Note: All npm commands run `prepare.sh` first, which copies image assets from playground to dist directory.

### Go Trust Registry Development (playground/trust-registry/)
- `go mod tidy` - Install/update Go dependencies
- `go run main.go --port=8082 --registry-name=TR-1` - Run trust registry server
- `go test` - Run Go tests

### Python Tools Development
- `pip install -r requirements.txt` - Install Python dependencies (for tools/ or playground/verifier/)
- `streamlit run ui.py` - Run verifier UI (in playground/verifier/)
- `python api_conformance_test.py` - Run API conformance tests (in tests/)

### Docker Development
- `docker-compose up -d` - Start all playground services (from playground/)
- `docker-compose logs [service-name]` - View logs for specific service
- `docker-compose down` - Stop all services

Available playground services:
- Ayra Trust Registry: http://localhost:8082
- Ecosystem Trust Registry: http://localhost:8083  
- Verifier UI: http://localhost:8501

## Project Architecture

### Core Components

**Specifications & Standards**
- `swagger.yaml` - Main TRQP API specification for Ayra compliance
- `spec/profile.md` - Ayra TRQP Profile requirements
- `playground/trust-registry/api/` - API specifications (v1.yaml, v2.yaml, admin.yaml)

**Sample Implementations**
- `playground/trust-registry/` - Go-based TRQP-compliant trust registry server
- `playground/verifier/` - Python Streamlit verifier application for testing queries

**Development Tools**
- `tools/did_creator_ui.py` - Interactive DID creation tool for ecosystems
- `tools/did_peer_utils.py` - Utility functions for DID generation and resolution
- `tests/api_conformance_test.py` - Automated API compliance testing

### Key Architecture Patterns

**TRQP Bridge Pattern**: The trust registry acts as a bridge between internal trust frameworks and the standardized TRQP interface. Internal authorization models can vary, but must expose TRQP endpoints.

**Multi-Ecosystem Support**: The system supports multiple trust registries running simultaneously (Ayra network + individual ecosystems), with cross-ecosystem recognition capabilities.

**DID-based Identity**: All ecosystems and entities are identified using DIDs, with service endpoints defining TRQP interfaces.

## Configuration

### Trust Registry Environment Variables
- `PORT` - Server port (default varies)
- `REGISTRY_NAME` - Human-readable registry identifier
- `BASE_URL` - Full base URL including protocol and hostname
- `REGISTRY_PATH` - Path to registry data file
- `REGISTRY_DATA` - Inline JSON/YAML registry data (alternative to file)

### Verifier Environment Variables  
- `DEFAULT_DID_RESOLVER_URL` - DID resolver service URL (default: https://dev.uniresolver.io/1.0/identifiers/)

## Key TRQP Endpoints

**Core TRQP Queries**
- `GET /entities/{entity_id}/authorization` - Check entity authorization status
- `GET /registries/{ecosystem_did}/recognition` - Verify ecosystem recognition
- `GET /metadata` - Retrieve trust registry metadata

**Ayra Extensions**
- `GET /ecosystems/{ecosystem_did}/recognitions` - List recognized ecosystems
- `GET /ecosystems/{ecosystem_did}/lookups/assuranceLevels` - Get supported assurance levels
- `GET /ecosystems/{ecosystem_did}/lookups/authorizations` - List ecosystem authorizations
- `GET /egfs/{ecosystem_did}/lookups/didmethods` - Get supported DID methods

## Testing and Compliance

Run the API conformance test to verify TRQP compliance:
```bash
cd tests
python api_conformance_test.py --base-url http://localhost:8082
```

The test verifies:
- Trust registry metadata structure
- Authorization query responses
- Recognition query responses  
- Error handling (401, 404 responses)

## Development Workflow

1. **Documentation Changes**: Use `npm run edit` to modify specs, `npm run render` to generate output
2. **Trust Registry Development**: Work in `playground/trust-registry/`, test with `go run main.go`
3. **Integration Testing**: Use `docker-compose up -d` to run full playground environment
4. **API Testing**: Run conformance tests against your implementation
5. **Tool Development**: Python tools in `tools/` directory for DID management

## Important Notes

- The playground uses container networking - `BASE_URL` should use container names (e.g., `http://ayra:8082`) in Docker Compose
- All APIs should return signed JWS responses for production use (playground may skip for demo purposes)
- Entity IDs, authorization IDs, and ecosystem DIDs are implementation-specific - no prescribed format
- The system is designed to bridge existing trust frameworks, not replace them