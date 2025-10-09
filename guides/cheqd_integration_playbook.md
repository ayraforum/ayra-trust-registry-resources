

# Ecosystem to Ecosystem Linkage

Any ecosystem that wants to allow access, even on a limited basis, to the external world, must provide the information that integrators will need to connect to and understand their ecosystem.

This information will include:

* **Authorities** that an ecoystem manages: i
* what approach is used to 


## Determining Ecoystem `authority_id` Values



In the early stages of the creation of a web of trust registries, the norms and mores for the `authority_id` do not exist. However, they will evolve. 

Ayra and Ayra Members can help speed up the establishment of the norms and mores. 




Sample `claim_id` from cheqd ecosystem:

```json
{
  "credentialSubject": {
    "accreditedFor": [
      {
        "schemaId": "https://resolver.cheqd.net/1.0/identifiers/did:cheqd:testnet:4ef4abb6-4c99-4aa5-aaac-a3cef01f3786?resourceName=AgentFactsSchema&resourceType=JsonSchemaValidator2020",
        "types": [
          "AgentFacts"
        ]
      },
      {
        "schemaId": "https://resolver.cheqd.net/1.0/identifiers/did:cheqd:testnet:4ef4abb6-4c99-4aa5-aaac-a3cef01f3786?resourceName=AgentFactsSchemaVCDM&resourceType=JsonSchemaValidator2020",
        "types": [
          "VerifiableCredential",
          "AgentFactsCredential"
        ]
      },
      {
        "schemaId": "https://resolver.cheqd.net/1.0/identifiers/did:cheqd:testnet:06f1b8a0-5650-4d57-a28e-36e6e7b66882?resourceName=AiAgentAuditSchema&resourceType=JsonSchemaValidator2020",
        "types": [
          "VerifiableCredential",
          "AiAgentAuditCredential"
        ]
      },
      {
        "schemaId": "https://resolver.cheqd.net/1.0/identifiers/did:cheqd:testnet:b003df6f-ec8e-48dd-9a2b-7011c5cf0a5e?resourceName=VerifiableAccreditation&resourceType=JSONSchemaValidator2020",
        "types": [
          "VerifiableCredential",
          "VerifiableAccreditation",
          "VerifiableAccreditationToAccredit"
        ]
      },
      {
        "schemaId": "https://resolver.cheqd.net/1.0/identifiers/did:cheqd:testnet:b003df6f-ec8e-48dd-9a2b-7011c5cf0a5e?resourceName=VerifiableAttestation&resourceType=JSONSchemaValidator2020",
        "types": [
          "VerifiableCredential",
          "VerifiableAttestation",
          "VerifiableAccreditationToAttest"
        ]
      }
    ],
    "id": "did:cheqd:testnet:169753bb-71a3-4d3d-856a-02c3f8734266"
  },
  "issuer": {
    "id": "did:cheqd:testnet:06f1b8a0-5650-4d57-a28e-36e6e7b66882"
  },
  "type": [
    "VerifiableCredential",
    "VerifiableAccreditationToAccredit"
  ],
  "termsOfUse": {
    "type": "AccreditationPolicy",
    "parentAccreditation": "did:cheqd:testnet:06f1b8a0-5650-4d57-a28e-36e6e7b66882?resourceName=RootAuthorizationForAiAgentTrustChain&resourceType=VerifiableAuthorizationForTrustChain",
    "rootAuthorization": "did:cheqd:testnet:06f1b8a0-5650-4d57-a28e-36e6e7b66882?resourceName=RootAuthorizationForAiAgentTrustChain&resourceType=VerifiableAuthorizationForTrustChain"
  },
  "@context": [
    "https://www.w3.org/2018/credentials/v1"
  ],
  "issuanceDate": "2025-07-30T12:12:50.000Z",
  "proof": {
    "type": "JwtProof2020",
    "jwt": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJ2YyI6eyJAY29udGV4dCI6WyJodHRwczovL3d3dy53My5vcmcvMjAxOC9jcmVkZW50aWFscy92MSJdLCJ0eXBlIjpbIlZlcmlmaWFibGVDcmVkZW50aWFsIiwiVmVyaWZpYWJsZUFjY3JlZGl0YXRpb25Ub0FjY3JlZGl0Il0sImNyZWRlbnRpYWxTdWJqZWN0Ijp7ImFjY3JlZGl0ZWRGb3IiOlt7InNjaGVtYUlkIjoiaHR0cHM6Ly9yZXNvbHZlci5jaGVxZC5uZXQvMS4wL2lkZW50aWZpZXJzL2RpZDpjaGVxZDp0ZXN0bmV0OjRlZjRhYmI2LTRjOTktNGFhNS1hYWFjLWEzY2VmMDFmMzc4Nj9yZXNvdXJjZU5hbWU9QWdlbnRGYWN0c1NjaGVtYSZyZXNvdXJjZVR5cGU9SnNvblNjaGVtYVZhbGlkYXRvcjIwMjAiLCJ0eXBlcyI6WyJBZ2VudEZhY3RzIl19LHsic2NoZW1hSWQiOiJodHRwczovL3Jlc29sdmVyLmNoZXFkLm5ldC8xLjAvaWRlbnRpZmllcnMvZGlkOmNoZXFkOnRlc3RuZXQ6NGVmNGFiYjYtNGM5OS00YWE1LWFhYWMtYTNjZWYwMWYzNzg2P3Jlc291cmNlTmFtZT1BZ2VudEZhY3RzU2NoZW1hVkNETSZyZXNvdXJjZVR5cGU9SnNvblNjaGVtYVZhbGlkYXRvcjIwMjAiLCJ0eXBlcyI6WyJWZXJpZmlhYmxlQ3JlZGVudGlhbCIsIkFnZW50RmFjdHNDcmVkZW50aWFsIl19LHsic2NoZW1hSWQiOiJodHRwczovL3Jlc29sdmVyLmNoZXFkLm5ldC8xLjAvaWRlbnRpZmllcnMvZGlkOmNoZXFkOnRlc3RuZXQ6MDZmMWI4YTAtNTY1MC00ZDU3LWEyOGUtMzZlNmU3YjY2ODgyP3Jlc291cmNlTmFtZT1BaUFnZW50QXVkaXRTY2hlbWEmcmVzb3VyY2VUeXBlPUpzb25TY2hlbWFWYWxpZGF0b3IyMDIwIiwidHlwZXMiOlsiVmVyaWZpYWJsZUNyZWRlbnRpYWwiLCJBaUFnZW50QXVkaXRDcmVkZW50aWFsIl19LHsic2NoZW1hSWQiOiJodHRwczovL3Jlc29sdmVyLmNoZXFkLm5ldC8xLjAvaWRlbnRpZmllcnMvZGlkOmNoZXFkOnRlc3RuZXQ6YjAwM2RmNmYtZWM4ZS00OGRkLTlhMmItNzAxMWM1Y2YwYTVlP3Jlc291cmNlTmFtZT1WZXJpZmlhYmxlQWNjcmVkaXRhdGlvbiZyZXNvdXJjZVR5cGU9SlNPTlNjaGVtYVZhbGlkYXRvcjIwMjAiLCJ0eXBlcyI6WyJWZXJpZmlhYmxlQ3JlZGVudGlhbCIsIlZlcmlmaWFibGVBY2NyZWRpdGF0aW9uIiwiVmVyaWZpYWJsZUFjY3JlZGl0YXRpb25Ub0FjY3JlZGl0Il19LHsic2NoZW1hSWQiOiJodHRwczovL3Jlc29sdmVyLmNoZXFkLm5ldC8xLjAvaWRlbnRpZmllcnMvZGlkOmNoZXFkOnRlc3RuZXQ6YjAwM2RmNmYtZWM4ZS00OGRkLTlhMmItNzAxMWM1Y2YwYTVlP3Jlc291cmNlTmFtZT1WZXJpZmlhYmxlQXR0ZXN0YXRpb24mcmVzb3VyY2VUeXBlPUpTT05TY2hlbWFWYWxpZGF0b3IyMDIwIiwidHlwZXMiOlsiVmVyaWZpYWJsZUNyZWRlbnRpYWwiLCJWZXJpZmlhYmxlQXR0ZXN0YXRpb24iLCJWZXJpZmlhYmxlQWNjcmVkaXRhdGlvblRvQXR0ZXN0Il19XX0sInRlcm1zT2ZVc2UiOnsidHlwZSI6IkFjY3JlZGl0YXRpb25Qb2xpY3kiLCJwYXJlbnRBY2NyZWRpdGF0aW9uIjoiZGlkOmNoZXFkOnRlc3RuZXQ6MDZmMWI4YTAtNTY1MC00ZDU3LWEyOGUtMzZlNmU3YjY2ODgyP3Jlc291cmNlTmFtZT1Sb290QXV0aG9yaXphdGlvbkZvckFpQWdlbnRUcnVzdENoYWluJnJlc291cmNlVHlwZT1WZXJpZmlhYmxlQXV0aG9yaXphdGlvbkZvclRydXN0Q2hhaW4iLCJyb290QXV0aG9yaXphdGlvbiI6ImRpZDpjaGVxZDp0ZXN0bmV0OjA2ZjFiOGEwLTU2NTAtNGQ1Ny1hMjhlLTM2ZTZlN2I2Njg4Mj9yZXNvdXJjZU5hbWU9Um9vdEF1dGhvcml6YXRpb25Gb3JBaUFnZW50VHJ1c3RDaGFpbiZyZXNvdXJjZVR5cGU9VmVyaWZpYWJsZUF1dGhvcml6YXRpb25Gb3JUcnVzdENoYWluIn19LCJzdWIiOiJkaWQ6Y2hlcWQ6dGVzdG5ldDoxNjk3NTNiYi03MWEzLTRkM2QtODU2YS0wMmMzZjg3MzQyNjYiLCJuYmYiOjE3NTM4Nzc1NzAsImlzcyI6ImRpZDpjaGVxZDp0ZXN0bmV0OjA2ZjFiOGEwLTU2NTAtNGQ1Ny1hMjhlLTM2ZTZlN2I2Njg4MiJ9.m2QhvYyO5K1ih5pWQelyUc3CYhqReIUBxO-sbEb0L2WUwiMaTsOt60f3Bf7zPirBj896wLKYVzfVQaXDK-fzCg"
  }
}
```