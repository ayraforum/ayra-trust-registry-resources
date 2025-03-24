# Sample Verifier for Ayra Trust Network

This directory contains a sample verifier implementation that demonstrates how to query Trust Registries in the Ayra Trust Network.

## Components

- [ui.py](./ui.py) - Streamlit-based user interface for interacting with the verifier
- [verify_flow.py](./verify_flow.py) - Core verification logic implementing the TRQP queries

## Requirements

- Python 3.7 or higher
- Dependencies specified in [requirements.txt](./requirements.txt)

## Running the Verifier

### Using Docker

The simplest way to run the verifier is using Docker as part of the complete playground:

```bash
cd ../
docker-compose up -d
```

The verifier UI will be available at http://localhost:8501

### Manual Setup

If you prefer to run the verifier without Docker:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit interface:
   ```bash
   streamlit run ui.py
   ```

## Features

The sample verifier demonstrates:

1. **Ecosystem Recognition Query** - Checking if an ecosystem is recognized by the Ayra Trust Network
2. **Authorization Query** - Verifying if an entity is authorized within a specific ecosystem

## Using the Verifier

### Testing Ecosystem Recognition

1. Navigate to the "Ecosystem Recognition" tab in the Streamlit interface
2. Enter the Recognizing Ecosystem's DID and the Ecosystem ID to check
3. Click "Perform Ecosystem Recognition Query"
4. The interface will display the recognition status and details

### Testing Authorization

1. Navigate to the "Authorization" tab in the Streamlit interface
2. Enter the EGF DID, Entity ID, and Entity Authorization ID
3. Click "Perform Authorization Query"
4. The interface will display the authorization status

## Customizing the Verifier

You can modify the verifier implementation to:

- Change the UI layout and features
- Add additional query types
- Implement caching for better performance
- Add request signing and validation
