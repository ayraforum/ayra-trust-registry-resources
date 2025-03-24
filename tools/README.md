# Ayra Trust Registry Tools

This directory contains tools to help you create and manage DIDs for the Ayra Trust Network.

## Available Tools

### DID Peer 2 Generator & Resolver

The primary tool in this directory is a generator and resolver for `DID:peer:2` identifiers with support for Trust Registry and Ecosystem DIDs. It uses Streamlit for the web interface and cryptographic libraries to generate DID keys and services.

- [DID Creator UI](./did_creator_ui.py) - Web interface for generating DIDs
- [DID Peer Utils](./did_peer_utils.py) - Core utilities for DID generation and resolution

## Requirements

- Python 3.7 or higher
- Libraries listed in [requirements.txt](./requirements.txt)

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run did_creator_ui.py
   ```

## Usage

### Generate a DID

1. Run the tool and choose the **Generate** mode.
2. Generate a **Trust Registry DID** by clicking on the "Generate Trust Registry DID" button.
3. After generating the Trust Registry DID, generate the **Ecosystem DID** by providing the necessary fields and clicking "Generate Ecosystem DID".

### Resolve a DID

1. Choose the **Resolve** mode in the app.
2. Enter the DID string you wish to resolve in the provided text input field.
3. Click on "Resolve DID" to get the associated DID document.

## Example Workflow

1. **Generate Trust Registry DID**:
   - This generates a DID associated with the Trust Registry.
   - The output includes the DID, Ed25519 Private Key, and X25519 Private Key.

2. **Generate Ecosystem DID**:
   - This generates a DID for an ecosystem that points to the previously generated Trust Registry DID.
   - The output includes the Ecosystem DID with its associated private keys.

3. **Resolve a DID**:
   - Input any DID string into the resolver to obtain the DID document.
