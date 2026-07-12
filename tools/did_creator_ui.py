#!/usr/bin/env python

import streamlit as st
from did_peer_utils import generate_did_peer2, resolve_did_peer2

TRQP_TR_PROFILE_URL = "https://ayra.forum/profiles/trqp/tr/v2"
TRQP_EGF_PROFILE_URL = "https://ayra.forum/profiles/trqp/egfURI/v1"


def show_demo_private_keys(ed25519_hex, x25519_hex):
    """Show generated private keys with clear demo-only warnings."""
    st.warning(
        "Demo-only private keys: do not paste these keys into production systems, "
        "logs, tickets, or shared documentation. Generate production keys with your "
        "approved key-management process."
    )
    with st.expander("Show demo private keys"):
        st.code(
            f"Ed25519 private key (hex): {ed25519_hex}\n"
            f"X25519 private key (hex): {x25519_hex}"
        )


st.set_page_config(page_title="DID Peer 2 Local Demo")
st.title("DID Peer 2 Local Demo Generator & Resolver")
st.warning(
    "Ayra profile identifiers are did:webvh DIDs. This DID Peer 2 tool is a "
    "local service-profile encoding demo only; do not use generated did:peer "
    "values as production Ayra ecosystem, trust registry, or cluster IDs."
)

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
                        "profile": TRQP_TR_PROFILE_URL,
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

            show_demo_private_keys(tr_ed_hex, tr_x_hex)

            # Store it in session_state
            st.session_state["trust_registry_did"] = tr_did
        except Exception as e:
            st.error(f"Error generating Trust Registry DID: {str(e)}")

    st.subheader("2) Generate Ecosystem DID that references the Trust Registry DID")

    ec_method_prefix = st.text_input("Ecosystem DID Method Prefix", value="did:peer:2")
    egf_uri = st.text_input(
        "Ecosystem Governance Framework URI", value="https://localhost:3000/terms"
    )
    tr_did = st.text_input(
        "Trust Registry DID",
        value=st.session_state.get("trust_registry_did") or "",
        help="Generate a Trust Registry DID first or paste an existing DID here.",
    )
    generate_ecosystem = st.button("Generate Ecosystem DID")
    if generate_ecosystem:
        if not tr_did:
            st.error("Please generate or input the Trust Registry DID first.")
        else:
            ecosystem_config = {
                "services": [
                    {
                        "id": "#egfURI",
                        "type": "egfURI",
                        "serviceEndpoint": {
                            "profile": TRQP_EGF_PROFILE_URL,
                            "uri": egf_uri,
                            "integrity": "122041dd7b6443542e75701aa98a0c235951a28a0d851b11564d20022ab11d2589a8",
                        },
                    },
                    {
                        "id": "#trust-registry",
                        "type": "TrustRegistryService",
                        "serviceEndpoint": {
                            "profile": TRQP_TR_PROFILE_URL,
                            "uri": tr_did,
                            "integrity": "example_integrity_hash_value",
                        },
                    },
                ]
            }

            try:
                ec_did, ec_ed_hex, ec_x_hex = generate_did_peer2(
                    ecosystem_config, ec_method_prefix
                )
                st.success("Successfully generated Ecosystem DID!")
                st.code(ec_did, language="bash")

                show_demo_private_keys(ec_ed_hex, ec_x_hex)
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
