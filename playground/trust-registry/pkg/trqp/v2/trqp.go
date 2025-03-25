package v2

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/golang-jwt/jwt/v4"

	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/gen/trqp/v2"
	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/pkg/utils"
)

var ecdsaPrivateKey *ecdsa.PrivateKey

func init() {
	// Generate an ephemeral ECDSA P-256 private key on startup.
	// In production, you'd likely load this key from a secure store or file.
	var err error
	ecdsaPrivateKey, err = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		panic("failed to generate ECDSA private key: " + err.Error())
	}
}

type TRQPHandler struct {
	Registry *utils.TrustRegistry
}

func (impl *TRQPHandler) GetEntityInformation(
	w http.ResponseWriter,
	r *http.Request,
	entityId string,
) {
	writeError(w, http.StatusNotImplemented, "Not implemented", "This endpoint is not implemented.")
}

func (impl *TRQPHandler) ListEcosystemRecognitions(
	w http.ResponseWriter,
	r *http.Request,
	ecosystemDID string,
	params trqp.ListEcosystemRecognitionsParams,
) {
	writeError(w, http.StatusNotImplemented, "Not implemented", "This endpoint is not implemented.")
}

func (impl *TRQPHandler) LookupAuthorizations(
	w http.ResponseWriter,
	r *http.Request,
	ecosystemDID string,
) {
	writeError(w, http.StatusNotImplemented, "Not implemented", "This endpoint is not implemented.")
}

func (impl *TRQPHandler) LookupSupportedAssuranceLevels(
	w http.ResponseWriter,
	r *http.Request,
	ecosystemDID string,
) {
	writeError(w, http.StatusNotImplemented, "Not implemented", "This endpoint is not implemented.")
}

func (impl *TRQPHandler) LookupSupportedDIDMethods(
	w http.ResponseWriter,
	r *http.Request,
	ecosystemDID string,
) {
	writeError(w, http.StatusNotImplemented, "Not implemented", "This endpoint is not implemented.")
}

func (impl *TRQPHandler) CheckEcosystemRecognition(
	w http.ResponseWriter,
	r *http.Request,
	ecosystemId string,
	params trqp.CheckEcosystemRecognitionParams,
) {
	egfDid := params.EgfDid

	ecosystem, err := impl.Registry.GetEcosystemByDID(egfDid)
	if err != nil {
		writeError(w, http.StatusNotFound, "Ecosystem not found", err.Error())
		return
	}

	if ecosystem.Metadata.DID != egfDid {
		writeError(w, http.StatusNotFound, "Ecosystem ID mismatch",
			"The ecosystem DID does not match the provided ecosystem_id.")
		return
	}

	var isRecognized = false

	for _, entry := range ecosystem.RecognitionEntries {
		if entry.DID == ecosystemId && entry.Status.Active {
			isRecognized = true
			break

		}
	}

	// Here we assume that an ecosystem is recognized if its metadata status is "active"

	recognitionPayload := map[string]interface{}{
		"ecosystem_did": ecosystem.Metadata.DID,
		"egf_did":       egfDid,
		"recognized":    isRecognized,
		"timestamp":     time.Now().UTC().Format(time.RFC3339),
	}
	payloadBytes, _ := json.Marshal(recognitionPayload)

	jws, err := signPayload(payloadBytes)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "Failed to sign payload", err.Error())
		return
	}
	expiry := time.Now().Add(time.Hour)

	resp := trqp.RecognitionResponse{
		EgfDid:       &ecosystem.Metadata.DID,
		EvaluatedAt:  time.Now(),
		ExpiryTime:   &expiry,
		Message:      "Ecosystem recognition evaluation",
		Recognized:   isRecognized,
		ResponseTime: time.Now(),
		Jws:          &jws,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func (impl *TRQPHandler) CheckAuthorizationStatus(
	w http.ResponseWriter,
	r *http.Request,
	entityId string,
	params trqp.CheckAuthorizationStatusParams,
) {
	authorizationId := params.AuthorizationId
	egfDid := params.EcosystemDid

	ecosystem, err := impl.Registry.GetEcosystemByDID(egfDid)
	if err != nil {
		writeError(w, http.StatusNotFound, "Ecosystem not found", err.Error())
		return
	}

	var found *utils.AuthorizationEntry
	for i, authEntry := range ecosystem.AuthorizationEntries {
		fmt.Println(authEntry.Authorization, authorizationId)
		if authEntry.ID == authorizationId && authEntry.DID == entityId {
			found = &ecosystem.AuthorizationEntries[i]
			break
		}
	}

	if found == nil {
		writeError(w, http.StatusNotFound, "Authorization not found",
			"No matching authorization entry for entity.")
		return
	}

	// If no status was provided in the authorization entry, assume it is active.
	authorized := true
	if found.Status.Active != true {
		authorized = (found.Status.Active == true)
	}

	authorizationPayload := map[string]interface{}{
		"entity_id":        entityId,
		"authorization_id": authorizationId,
		"authorized":       authorized,
		"timestamp":        time.Now().UTC().Format(time.RFC3339),
	}
	payloadBytes, _ := json.Marshal(authorizationPayload)

	jws, err := signPayload(payloadBytes)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "Failed to sign payload", err.Error())
		return
	}

	expiry := time.Now().Add(time.Hour)
	resp := trqp.AuthorizationResponse{
		Authorized:   authorized,
		EgfDid:       &egfDid,
		ExpiryTime:   &expiry,
		Message:      "Authorization status evaluation",
		Recognized:   true,
		ResponseTime: time.Now(),
		Jws:          &jws,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func (impl *TRQPHandler) GetTrustRegistryMetadata(w http.ResponseWriter, r *http.Request, params trqp.GetTrustRegistryMetadataParams) {
	// Define extended metadata that includes ecosystem and trust registry DIDs
	type ExtendedMetadata struct {
		trqp.TrustRegistryMetadata
		EcosystemDID     string `json:"ecosystem_did,omitempty"`
		TrustRegistryDID string `json:"trust_registry_did,omitempty"`
	}

	// Get the ecosystem DID from query parameters, if provided
	var ecosystemDID string
	if params.EgfDid != nil && *params.EgfDid != "" {
		ecosystemDID = *params.EgfDid

		// Verify that the ecosystem exists
		_, err := impl.Registry.GetEcosystemByDID(ecosystemDID)
		if err != nil {
			writeError(w, http.StatusNotFound, "Ecosystem not found", err.Error())
			return
		}
	} else {
		// If no ecosystem DID was provided, use the first one in the registry if available
		if len(impl.Registry.Ecosystems) > 0 {
			ecosystemDID = impl.Registry.Ecosystems[0].Metadata.DID
		}
	}

	// Create the response with additional fields
	resp := ExtendedMetadata{
		TrustRegistryMetadata: trqp.TrustRegistryMetadata{
			Name:          impl.Registry.Metadata.Name,
			Id:            impl.Registry.Metadata.Identifier,
			Description:   impl.Registry.Metadata.Description,
			DefaultEgfDid: &ecosystemDID,
		},
		EcosystemDID:     ecosystemDID,
		TrustRegistryDID: impl.Registry.Metadata.Identifier,
	}

	// Add controllers if available
	if ecosystemDID != "" {
		controllers := []string{ecosystemDID}
		resp.Controllers = controllers
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// signPayload creates a compact JWS string (header.payload.signature)
// using ES256 (ECDSA with P-256 and SHA-256).
func signPayload(payload []byte) (string, error) {
	// Manually build a JWT-like structure.
	header := base64.RawURLEncoding.EncodeToString([]byte(`{"alg":"ES256","typ":"JWT"}`))
	payloadEncoded := base64.RawURLEncoding.EncodeToString(payload)
	unsigned := header + "." + payloadEncoded

	signMethod := jwt.GetSigningMethod("ES256")
	signature, err := signMethod.Sign(unsigned, ecdsaPrivateKey)
	if err != nil {
		return "", err
	}
	return unsigned + "." + signature, nil
}

func writeError(w http.ResponseWriter, code int, errShort, details string) {
	w.WriteHeader(code)
	resp := trqp.ProblemDetails{
		Status: &code,
		Title:  &errShort,
		Detail: &details,
	}
	json.NewEncoder(w).Encode(resp)
}
