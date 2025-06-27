package v2

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/gen/trqp/v2"
	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/pkg/utils"
	"github.com/stretchr/testify/assert"
)

func generateTestPrivateKey() *ecdsa.PrivateKey {
	privKey, _ := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	return privKey
}

// Mock Trust Registry
func setupMockRegistry() *utils.TrustRegistry {
	return &utils.TrustRegistry{
		Metadata: utils.Metadata{
			Identifier: "test-trust-registry",
			Name:       "Test Trust Registry",
			Description: "A test trust registry for unit tests",
		},
		Ecosystems: []utils.Ecosystem{
			{
				Metadata: utils.EcosystemMetadata{
					DID:    "did:example:123",
					Status: utils.Status{Active: true},
				},
				RecognitionEntries: []utils.RecognitionEntry{
					{
						DID:    "did:example:123",
						Scope:  "test-scope",
						Status: utils.Status{Active: true},
					},
				},
				AuthorizationEntries: []utils.AuthorizationEntry{
					{
						ID:             "auth-1",
						DID:            "entity-1",
						Authorization:  "auth-1",
						Status:         utils.Status{Active: true},
					},
				},
			},
		},
	}
}

func TestCheckEcosystemRecognition_Success(t *testing.T) {
	handler := &TRQPHandler{Registry: setupMockRegistry()}

	req := httptest.NewRequest("GET", "/ecosystem-recognition", nil)
	w := httptest.NewRecorder()

	params := trqp.CheckEcosystemRecognitionParams{
		EgfDid: "did:example:123",
	}

	handler.CheckEcosystemRecognition(w, req, "did:example:123", params)

	resp := w.Result()
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)

	var response trqp.RecognitionResponse
	err := json.NewDecoder(resp.Body).Decode(&response)
	assert.NoError(t, err)
	assert.NotEmpty(t, response.Jws)
}

func TestCheckEcosystemRecognition_NotFound(t *testing.T) {
	handler := &TRQPHandler{Registry: setupMockRegistry()}

	req := httptest.NewRequest("GET", "/ecosystem-recognition", nil)
	w := httptest.NewRecorder()

	params := trqp.CheckEcosystemRecognitionParams{
		EgfDid: "did:example:999",
	}

	handler.CheckEcosystemRecognition(w, req, "did:example:999", params)

	resp := w.Result()
	defer resp.Body.Close()

	assert.Equal(t, http.StatusNotFound, resp.StatusCode)
}

func TestCheckAuthorizationStatus_Success(t *testing.T) {
	handler := &TRQPHandler{Registry: setupMockRegistry()}

	req := httptest.NewRequest("GET", "/authorization-status", nil)
	w := httptest.NewRecorder()

	params := trqp.CheckAuthorizationStatusParams{
		AuthorizationId: "auth-1",
		EcosystemDid:    "did:example:123",
		All:             false,
	}

	handler.CheckAuthorizationStatus(w, req, "entity-1", params)

	resp := w.Result()
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)

	var response trqp.AuthorizationResponse
	err := json.NewDecoder(resp.Body).Decode(&response)
	assert.NoError(t, err)
	assert.NotEmpty(t, response.Jws)
}

func TestCheckAuthorizationStatus_NotFound(t *testing.T) {
	handler := &TRQPHandler{Registry: setupMockRegistry()}

	req := httptest.NewRequest("GET", "/authorization-status", nil)
	w := httptest.NewRecorder()

	params := trqp.CheckAuthorizationStatusParams{
		AuthorizationId: "auth-999",
		EcosystemDid:    "did:example:123",
		All:             false,
	}

	handler.CheckAuthorizationStatus(w, req, "entity-1", params)

	resp := w.Result()
	defer resp.Body.Close()

	assert.Equal(t, http.StatusNotFound, resp.StatusCode)
}

func TestGetTrustRegistryMetadata_Success(t *testing.T) {
	handler := &TRQPHandler{Registry: setupMockRegistry()}

	req := httptest.NewRequest("GET", "/trust-registry-metadata", nil)
	w := httptest.NewRecorder()

	params := trqp.GetTrustRegistryMetadataParams{}

	handler.GetTrustRegistryMetadata(w, req, params)

	resp := w.Result()
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)

	var response trqp.TrustRegistryMetadata
	err := json.NewDecoder(resp.Body).Decode(&response)
	assert.NoError(t, err)
	assert.NotEmpty(t, response.Id)
}
