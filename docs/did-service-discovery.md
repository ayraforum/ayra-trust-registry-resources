# DID service discovery notes

Non-normative design note, offered for discussion. Nothing here changes the
[Ayra TRQP Profile](../spec/profile.md) or the
[Ayra TRQP Profile API](../trqp_ayra_profile_swagger.yaml); it proposes the DID
document shape and client rules those documents currently assume but do not
specify, and records where this repository contradicts itself today.

Written from the implementer's side, while building a TRQP registry that has to
be discoverable by DID.

## The gap

Two normative statements in this repository depend on a DID document shape that
is never given:

- `spec/profile.md` -- "The Trust Registry DID Document should make its TRQP
  service endpoint discoverable."
- `spec/profile.md` -- the ecosystem governance framework "MUST be discoverable
  via the `authority_id`", possibly "through DID Document service entries".

The verifier flow in `guides/implementers_guide.md` then leans on that shape
twice: "Extract Ayra TR endpoint", and "Extract Trust Registry DID **or** TRQP
service endpoint". That second step is the interesting one -- the same lookup
can yield either a URL to call or another DID to resolve, and the guide does not
say how a client tells them apart.

No example DID document appears anywhere in the repository outside
`tools/did_creator_ui.py`. Two independent implementations reading the documents
above will not produce interoperable service entries, which makes the query
endpoints undiscoverable in practice even when both registries are conformant at
the API layer.

## What the specs give us

| Type | Status |
| :-- | :-- |
| `TrustRegistry` | Defined in the [ToIP Service Profile spec](https://github.com/trustoverip/tswg-trust-registry-service-profile/blob/main/spec.md), **Pre-Draft 0.0.1**, self-described as not binding. The only spec that names a service type for this purpose. |
| `TRQP` | Used by `tools/did_creator_ui.py`. No spec, no registration. |
| `DIDCommMessaging` | Registered in [W3C DID Extensions](https://www.w3.org/TR/did-extensions-properties/#service-types). Relevant only once a non-HTTPS binding exists. |

[TRQP v2.0](https://trustoverip.github.io/tswg-trust-registry-protocol/approved/)
declines to name a service type, but does bless the indirection:

> "It is RECOMMENDED that the TRQP service endpoint(s) for any authoritative
> trust registry be machine-discoverable via the `authority_id`. An example
> would be to publish either of the following in the DID document for the
> `authority_id`: 1. The authoritative TRQP service endpoint URL(s). 2. The
> DID(s) identifying authoritative trust registries."

Both options in one sentence, with no discriminator -- which is exactly the
ambiguity the implementers guide inherits.

The ToIP Service Profile struct is `{uri, profile|definition, integrity?}`:
`uri` required, exactly one of `profile`/`definition`, `integrity` an optional
multihash. Its own text states "An array of structs is not valid", so one
service entry per binding, always.
[CID 1.0 §Services](https://www.w3.org/TR/cid-1.0/#services) governs the
container: `type` is required and may be a string **or a set of strings**;
`serviceEndpoint` may be a string, a map, or a set; service `id`s must be unique
within the document.

## Conflicting and out-of-date material in this repository

### 1. Three profile URIs for two things, none of which resolve

| Location | URI | Meaning |
| :-- | :-- | :-- |
| `guides/implementers_guide.md` (Creating an Identifier for Your Registry) | `https://ayra.forum/profiles/trqp/tr/v2` | TR query endpoint |
| `tools/did_creator_ui.py` | `https://trustoverip.org/profiles/trp/v2` | TR query endpoint |
| `tools/did_creator_ui.py` | `https://trustoverip.org/profiles/trp/egfURI/v1` | ecosystem governance framework |
| `tools/did_creator_ui.py` | `https://example.org/profiles/ecosystemService/v1` | ecosystem -> TR referral |

Open PR #38 moves the tool to `https://ayra.forum/profiles/trqp/tr/v2` and
`https://ayra.forum/profiles/trqp/egfURI/v1`, which settles the guide/tool split
in the guide's favour. This note assumes that direction.

Two things remain after #38:

- **`example.org` for the ecosystem -> TR referral.** A placeholder domain in
  the one entry whose semantics are least defined. Proposal below reuses the
  registry profile URI and disambiguates on the value of `uri` instead.
- **None of these URIs resolve** -- `ayra.forum/profiles/trqp/tr/v2`,
  `trustoverip.org/profiles/trp/v2` and `trustoverip.org/profiles/trp/egfURI/v1`
  all return 404 today. The ToIP struct describes `profile` as "a JSON Profile
  document that can be resolved through HTTPS". Until something is served there,
  `profile` is an opaque version tag, not a capability descriptor, and a client
  can only string-compare it. Publishing a real document at the `ayra.forum`
  URIs is what turns the field into discovery rather than decoration.

Separately, ToIP's own `trp` spelling predates the protocol's rename to TRQP;
`trqp` is worth raising upstream, and Ayra's `ayra.forum/profiles/trqp/...`
already reads correctly.

### 2. The service type conflicts with the only spec that defines the struct

`tools/did_creator_ui.py` emits `"type": "TRQP"` while using the ToIP Service
Profile struct for `serviceEndpoint`. The ToIP example that struct comes from
uses `"type": "TrustRegistry"`. A consumer written against ToIP matches on
`TrustRegistry` and finds nothing; a consumer written against the tool matches
on `TRQP` and finds nothing in a ToIP-shaped document. Neither fails loudly --
both read the document as advertising no registry at all.

`spec/profile.md` names no type, so there is nothing normative to break by
choosing one.

### 3. `integrity` values are the spec's placeholder, copied

The three `integrity` values in `tools/did_creator_ui.py` are the ToIP spec
example's constant `122041dd...2589a8` (twice, differing by one character) and
the literal string `"example_integrity_hash_value"`. PR #38 keeps them. They
look like real multihashes in generated documents. A client that pins and checks
them rejects a correct endpoint; a client that does not check gains nothing.
`integrity` is optional -- omit it until something actually verifies it.

### 4. `did:peer:2` tooling against a `did:webvh` profile

`tools/did_creator_ui.py` defaults to `did:peer:2` while the profile prefers
`did:webvh` for higher assurance. PR #38 labels the tool a local demo, which
resolves the confusion; worth noting here only because a `did:peer:2` document
cannot be fetched from the identifier alone, so it cannot demonstrate the
resolution flow the implementers guide describes.

### Adjacent, out of scope for this note

- `CLAUDE.md` predates the TRQP v2.0 alignment: it names `swagger.yaml`
  (now `trqp_ayra_profile_swagger.yaml`), `playground/trust-registry/` and
  `playground/verifier/` (neither is in the tree), `GET
  /entities/{entity_id}/authorization` and `GET /egfs/{...}/lookups/didmethods`
  (now `POST /authorization` and `/lookups/didMethods`), and the tag
  `ayra-extensions` (the README and OpenAPI use `ayra-extension`).
- `guides/trqp-consumer-implementation-guide.md` uses `assertion_id` where the
  profile uses the PARC pair `action` + `resource`, and ends mid-sentence.

## Proposed shapes

### Trust Registry DID document

Advertises what this registry actually serves.

```json
{
  "id": "did:webvh:QmRegistryScid:registry.example",
  "service": [
    {
      "id": "did:webvh:QmRegistryScid:registry.example#trqp",
      "type": "TrustRegistry",
      "serviceEndpoint": {
        "uri": "https://registry.example",
        "profile": "https://ayra.forum/profiles/trqp/tr/v2"
      }
    }
  ]
}
```

- `uri` is the base URL that `POST /authorization` and `POST /recognition` hang
  off, matching the OpenAPI server base. Clients append the paths; the entry does
  not name individual endpoints.
- `integrity` omitted deliberately -- see above.
- An implementation may add its own type alongside the standard one using CID's
  set form, `"type": ["TrustRegistry", "SomethingLocal"]`. The rules below treat
  `type` as a set for exactly this reason; consumers must not assume a string.

### Ecosystem / authority DID document

An ecosystem names the registry authoritative for it. Same type, `uri` holds a
**DID** instead of an HTTPS URL -- legal, since the ToIP schema is
`{"type":"string","format":"uri"}` and a `did:` string is a URI.

```json
{
  "id": "did:webvh:QmEcosystemScid:ecosystem.example",
  "service": [
    {
      "id": "did:webvh:QmEcosystemScid:ecosystem.example#egf",
      "type": "egfURI",
      "serviceEndpoint": {
        "uri": "https://ecosystem.example/governance",
        "profile": "https://ayra.forum/profiles/trqp/egfURI/v1"
      }
    },
    {
      "id": "did:webvh:QmEcosystemScid:ecosystem.example#trust-registry",
      "type": "TrustRegistry",
      "serviceEndpoint": {
        "uri": "did:webvh:QmRegistryScid:registry.example",
        "profile": "https://ayra.forum/profiles/trqp/tr/v2"
      }
    }
  ]
}
```

Multiple registries get multiple entries with distinct fragments
(`#trust-registry-eu`, `#trust-registry-apac`) -- never an array inside one
`serviceEndpoint`, which the ToIP struct forbids.

An ecosystem that serves TRQP itself uses the HTTPS form directly and no
referral is involved.

## Proposed client rules

`TrustRegistry` means two different things depending on whose document it is in:
an endpoint in a registry's own document, a referral in an ecosystem's. A client
must disambiguate before it can use either.

1. Resolve the starting DID -- normally the `authority_id`.
2. For each `TrustRegistry` entry: if `serviceEndpoint.uri` starts with `did:`
   and differs from this document's `id`, it is a **referral**; otherwise it is
   an **endpoint**.
3. On a referral, resolve that DID once and restart at step 2 against the new
   document. **Cap at one hop.** TRQP's wording assumes the registry's own
   document holds the endpoints; chasing chains invites cycles.
4. Query the endpoint per the Ayra TRQP Profile API.
5. **Close the loop.** Confirm the registry's answer names the authority the
   client started from -- the `authority_id` in the response matches the DID
   whose document produced the referral.

Step 5 is not optional. A pointer in an ecosystem's own document is a
self-assertion: anyone can publish a DID document naming any registry. Authority
flows registry -> subject, never the reverse. Until the registry confirms, a
referral has told the client *where to ask* and nothing about the answer.

Treat `type` as a set and `serviceEndpoint` as string-or-map on the read side,
per CID 1.0, even though this note only ever writes the map form.

## Compatibility

The proposals that change existing behaviour are the service type (`TRQP` ->
`TrustRegistry`) and dropping placeholder `integrity`. Both only affect
`tools/did_creator_ui.py` and any documents generated by it. A consumer matching
`s["type"] == "TRQP"` reads a renamed document as advertising no registry -- a
silent capability loss rather than a parse error -- so the change wants to land
before more implementations exist rather than after.

A registry needing both can emit `"type": ["TrustRegistry", "TRQP"]` during a
transition, which CID permits and which the read-side rule above already
tolerates.

## Open questions

1. Is `ayra.forum/profiles/trqp/tr/v2` intended to serve a real profile document?
   If not, is a non-resolving version tag the intent, and should the guide say
   so?
2. Does Ayra want `TrustRegistry` (following ToIP) or a distinct Ayra type? A
   third spelling would be worse than either.
3. Should the referral pattern be normative in `spec/profile.md`, or stay
   guidance? It is currently neither, but the verifier flow depends on it.
4. Is the one-hop cap right, or does Ayra foresee registry chains that need
   more?
5. Worth raising upstream: TRQP v2.0 recommends DID-document discoverability
   without naming a service type, and the Service Profile spec it leans on is
   still Pre-Draft (and its example has a JSON syntax error and the pre-rename
   `trp` spelling).
