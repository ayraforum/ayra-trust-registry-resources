# Ayra TR Profile DID Peer 2 Generator & Resolver

This project allows you to generate and resolve `DID:peer:2` identifiers with support for Trust Registry and Ecosystem DIDs. It uses Streamlit for the web interface and cryptographic libraries to generate DID keys and services.

## Requirements

This project requires the following Python libraries:

- `streamlit`: A framework for creating interactive web applications.
- `cryptography`: A library for cryptographic operations.
- `base58`: A library to handle base58 encoding.
  
You can install the dependencies using the `requirements.txt` file provided.

## Prerequisites

Ensure that you have Python 3.7 or higher installed. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

This will launch the Streamlit application in your default browser.

## Usage

### Generate a DID:
1. Choose the **Generate** mode in the app.
2. First, generate a **Trust Registry DID** by clicking on the "Generate Trust Registry DID" button.
3. After generating the Trust Registry DID, generate the **Ecosystem DID** by providing the necessary fields and clicking "Generate Ecosystem DID".

### Resolve a DID:
1. Choose the **Resolve** mode in the app.
2. Enter the DID string you wish to resolve in the provided text input field.
3. Click on "Resolve DID" to get the associated DID document.

## Example Workflow

1. **Generate Trust Registry DID**:
   - This will generate a DID associated with the Trust Registry.
   - The output includes the DID, Ed25519 Private Key, and X25519 Private Key.

2. **Generate Ecosystem DID**:
   - This will generate a DID for an ecosystem that points to the previously generated Trust Registry DID.
   - The output includes the Ecosystem DID along with its associated private keys.

3. **Resolve a DID**:
   - Input any DID string into the resolver to obtain the DID document.

## Files

- `streamlit_app.py`: The main Streamlit app that provides the UI and calls the DID generation/resolution functions.
- `did_peer_utils.py`: Utility functions to generate and resolve DIDs.

