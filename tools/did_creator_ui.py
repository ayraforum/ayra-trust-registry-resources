#!/usr/bin/env python

import streamlit as st
import json
from did_peer_utils import generate_did_peer2, resolve_did_peer2

st.set_page_config(page_title="DID Peer 2 Generator")
st.title("DID Peer 2 Generator & Resolver")

# Ensure that the Trust Registry DID is stored in session_state
if "trust_registry_did" not in st.session_state:
    st.session_state["trust_registry_did"] = None

mode = st.radio("Select mode:", ["Generate", "Resolve"])

# --------------------------------------------------------------
# Mode: Generate
# --------------------------------------------------------------
if mode == "Generate":
    st.subheader("1) Generate Trust Registry DID")

    tr_method_prefix = st.text_input(
        "Trust Registry DID Method Prefix", value="did:peer:2"
    )
    trqp_endpoint = st.text_input(
        "Service Endpoint For Trust Registry", value="https://localhost:3000/trqp"
    )

    if st.button("Generate Trust Registry DID"):
        trust_registry_config = {
            "services": [
                {
                    "id": "#tr-1",
                    "type": "TRQP",
                    "serviceEndpoint": {
                        "profile": "https://trustoverip.org/profiles/trp/v2",
                        "uri": trqp_endpoint,
                        "integrity": "122041dd7b6443542e75701aa98a0c235952a28a0d851b11564d20022ab11d2589a8",
                    },
                }
            ]
        }
        try:
            tr_did, tr_ed_hex, tr_x_hex = generate_did_peer2(
                trust_registry_config, tr_method_prefix
            )
            st.success("Successfully generated Trust Registry DID!")
            st.code(tr_did, language="bash")

            st.write("**Ed25519 Private Key (hex):**", tr_ed_hex)
            st.write("**X25519 Private Key (hex):**", tr_x_hex)

            # Store it in session_state
            st.session_state["trust_registry_did"] = tr_did
        except Exception as e:
            st.error(f"Error generating Trust Registry DID: {str(e)}")

    # Only display next step if we have a TR DID
    if True:  # st.session_state["trust_registry_did"]:
        st.subheader("2) Generate Ecosystem DID that references the Trust Registry DID")

        ec_method_prefix = st.text_input(
            "Ecosystem DID Method Prefix", value="did:peer:2"
        )
        egf_uri = st.text_input(
            "Ecosystem Governance Framework URI", value="https://localhost:3000/terms"
        )
        tr_did = st.text_input("Trust Registry DID's", value="")
        generate_ecosystem = st.button("Generate Ecosystem DID")
        if generate_ecosystem:
            if not tr_did:
                st.error(
                    "Trust Registry DID is not generated yet. Please generate it first."
                )
            else:
                ecosystem_config = {
                    "services": [
                        {
                            "id": "#egfURI",
                            "type": "egfURI",
                            "serviceEndpoint": {
                                "profile": "https://trustoverip.org/profiles/trp/egfURI/v1",
                                "uri": egf_uri,
                                "integrity": "122041dd7b6443542e75701aa98a0c235951a28a0d851b11564d20022ab11d2589a8",
                            },
                        },
                    ]
                }

                # Add the service URI to the Ecosystem DID configuration
                if tr_did:
                    ecosystem_config["services"].append(
                        {
                            "id": "#TRQP",
                            "type": "TRQP",
                            "serviceEndpoint": {
                                "profile": "https://example.org/profiles/ecosystemService/v1",
                                "uri": tr_did,
                                "integrity": "example_integrity_hash_value",
                            },
                        }
                    )
                else:
                    st.error("Please input the trust registry DID")
                    raise "no trust registry DID"
                try:
                    print("Created ecosystem DID")
                    ec_did, ec_ed_hex, ec_x_hex = generate_did_peer2(
                        ecosystem_config, ec_method_prefix
                    )
                    st.success("Successfully generated Ecosystem DID!")
                    st.code(ec_did, language="bash")

                    st.write("**Ed25519 Private Key (hex):**", ec_ed_hex)
                    st.write("**X25519 Private Key (hex):**", ec_x_hex)
                except Exception as e:
                    st.error(f"Error generating Ecosystem DID: {str(e)}")

# --------------------------------------------------------------
# Mode: Resolve
# --------------------------------------------------------------
elif mode == "Resolve":
    st.subheader("Resolve a DID")

    did_str = st.text_input("DID to Resolve", value="")
    if st.button("Resolve DID"):
        try:
            doc = resolve_did_peer2(did_str, "did:peer:2")
            st.success("DID Resolution Successful!")
            st.json(doc)
        except Exception as e:
            st.error(f"Error: {str(e)}")
