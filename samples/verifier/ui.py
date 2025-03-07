#!/usr/bin/env python3

# egf_ui.py

import streamlit as st
from datetime import datetime, timezone
from verify_flow import ecosystem_recognition_query, authorization_query
from uuid import uuid4


def main():
    st.title("Authority Verification Tool")
    st.write(
        """
    This tool allows you to perform **Ecosystem Recognition** and **Authorization** queries by resolving DIDs and interacting with the appropriate service endpoints.
    """
    )

    # Sidebar for Configuration
    st.sidebar.header("Configuration")
    resolver_url = st.sidebar.text_input(
        "DID Resolver URL",
        value="https://dev.uniresolver.io/1.0/identifiers/",
        help="Specify a custom DID Resolver endpoint. Defaults to https://did-resolver.example.com/resolve/",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by [Ayra Forum](ayra.forum)")

    # Tabs for Different Queries
    tabs = st.tabs(["Ecosystem Recognition", "Authorization"])

    with tabs[0]:
        st.header("Ecosystem Recognition Query")

        # Input Fields
        egf_did_recognition = st.text_input(
            "Recognizing Ecosystem's DID (i.e Ayra)",
            value="did:ayra:forum",
            help="EGF DID for Ecosystem Recognition Query (default: did:ayra:forum)",
        )
        ecosystem_id = st.text_input(
            "Ecosystem ID", help="Ecosystem ID for Recognition Query"
        )
        scope = st.text_input("Scope", help="Scope for Recognition Query")
        time_recognition = st.text_input(
            "Time (RFC3339 format)",
            value=datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"),
            help="Time for Recognition Query in RFC3339 format (default: current UTC time)",
        )

        # Action Button
        if st.button("Perform Ecosystem Recognition Query"):
            if not ecosystem_id:
                st.error("Please provide both Ecosystem ID.")
            else:
                with st.spinner("Performing Ecosystem Recognition Query..."):
                    try:
                        result = ecosystem_recognition_query(
                            egf_did=egf_did_recognition,
                            ecosystem_id=ecosystem_id,
                            time=time_recognition,
                            nonce=str(uuid4()),
                            scope=scope,
                            resolver_url=resolver_url,
                        )
                        st.success("Ecosystem Recognition Query Successful!")
                        st.json(result)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with tabs[1]:
        st.header("Authorization Query")

        # Input Fields
        egf_did_authorization = st.text_input(
            "EGF DID", help="EGF DID for Authorization Query"
        )
        entity_id = st.text_input("Entity ID", help="Entity ID for Authorization Query")
        entity_auth_id = st.text_input(
            "Entity Authorization ID",
            help="Entity Authorization ID for Authorization Query",
        )
        time_authorization = st.text_input(
            "Time (RFC format)",
            value=datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"),
            help="Time for Authorization Query in RFC3339 format (default: current UTC time)",
        )

        # Action Button
        if st.button("Perform Authorization Query"):
            if not egf_did_authorization or not entity_id or not entity_auth_id:
                st.error(
                    "Please provide EGF DID, Entity ID, and Entity Authorization ID."
                )
            else:
                with st.spinner("Performing Authorization Query..."):
                    try:
                        result = authorization_query(
                            egf_did=egf_did_authorization,
                            entity_id=entity_id,
                            authorization_id=entity_auth_id,
                            time=time_authorization,
                            resolver_url=resolver_url,
                            nonce=str(uuid4()),
                        )
                        st.success("Authorization Query Successful!")
                        st.json(result)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
