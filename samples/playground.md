# Ayra Trust Network Playground

The following document describes how to setup your own Ayra playground to test the Ayra Trust Network.

**Step 1: Setup a sample Ayra Trust Network.**

Go to `trust-registry`. Run the go program: 

`go run main.go -port 8085`

In production, this is hosted by Ayra. You will see a DID. Remember it! This is the **Ayra DID.**

**Feel free to inspect your DIDs**

To learn more go to https://dev.uniresolver.io and type in the DID's to see how they are structured. 

**Step 2: Setup a sample ecosystem that represents your own ecosystem:**

Open up another terminal. Run the go program: 

`go run main.go -port 8083`

You should have two ecosystems running. 

**Step 3: Authorize an entry in your ecosystem**

Go to `http://localhost:8083/admin/docs`. Go to the `admin/authorize` API. 
Enter an authorization type, egf_identifier, and the entry id. The entry is not authorized in your ecocsystem. 

Note for production, this **will** be dependent on your trust framework and choices. This is simply a sample.

**Step 4: Recognize The Ecosystem With Ayra**

Find the DID of the ecosystem represented in Step 1. Go now to `https://localhost:8085/admin/docs` and go to the `/admin/recognition` API.

For `target_ecosystem` type in the  Sample Ecosystem's DID.
For `egf_did` type in the Ayra Ecosystem DID

In production, this will be done via the Ayra Governance Process.

**Step 5: Test Verification**

Now we are going to test the verification process for a verifier outside the ecosystem. 

Go to `verifier` folder and install the requirements.

`python -m pip install -r requirements.txt`

then type:

python -m streamlit run ui.py

**Step 5.1: Test Ecosystem Recognition**

- Go to the first tab.
- For EGF DID, type in the Ayra DID you created in Step 1. 
- For Target DID, type in the  DID you created in the ecosystem for Step 2.
- Run the query. 

This is the _recognition_ step of Ayra. 

**Step 5.2: Test Ecosystem Authorization**

- Go to the second tab.
- For the EGF, use the Ecosystem DID
- For the Entity ID, used the authorized entity from Step 3
- For the Authorization Type ID, use the type string from Step 3
- Click Run

This is the _authorization_ query.

This performs the Authority Queries of the Ayra Trust Network. 






