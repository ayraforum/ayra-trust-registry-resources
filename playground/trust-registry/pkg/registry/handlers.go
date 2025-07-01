package registry

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/gen/admin"
	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/pkg/utils"
)

type TrustRegistryHandlers struct {
	svc *TrustRegistryService
}

func NewTrustRegistryHandlers(svc *TrustRegistryService) *TrustRegistryHandlers {
	return &TrustRegistryHandlers{svc: svc}
}

// Helper to write JSON error responses
func writeJSONError(w http.ResponseWriter, code int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	_ = json.NewEncoder(w).Encode(map[string]string{"error": message})
}

func (h *TrustRegistryHandlers) CreateEcosystem(w http.ResponseWriter, r *http.Request) {
	var eco utils.Ecosystem
	if err := json.NewDecoder(r.Body).Decode(&eco); err != nil {
		writeJSONError(w, http.StatusBadRequest, err.Error())
		return
	}

	if err := h.svc.CreateEcosystem(eco); err != nil {
		writeJSONError(w, http.StatusConflict, err.Error())
		return
	}

	w.WriteHeader(http.StatusCreated)
	_ = json.NewEncoder(w).Encode(map[string]string{"message": "ecosystem created"})
}

// GetEcosystem handles GET /ecosystems/{did}
func (h *TrustRegistryHandlers) GetEcosystem(w http.ResponseWriter, r *http.Request, did string) {
	eco, err := h.svc.GetEcosystem(did)
	if err != nil {
		writeJSONError(w, http.StatusNotFound, err.Error())
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(eco)
}

func (h *TrustRegistryHandlers) UpdateEcosystem(w http.ResponseWriter, r *http.Request, did string) {

	var eco utils.Ecosystem
	if err := json.NewDecoder(r.Body).Decode(&eco); err != nil {
		writeJSONError(w, http.StatusBadRequest, err.Error())
		return
	}

	// Ensure the JSON DID matches the path param
	if eco.Metadata.DID != did {
		writeJSONError(w, http.StatusBadRequest, "Mismatched ecosystem DID")
		return
	}

	if err := h.svc.UpdateEcosystem(eco); err != nil {
		writeJSONError(w, http.StatusNotFound, err.Error())
		return
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]string{"message": "ecosystem updated"})
}

func (h *TrustRegistryHandlers) RemoveEcosystem(w http.ResponseWriter, r *http.Request, did string) {

	if err := h.svc.RemoveEcosystem(did); err != nil {
		writeJSONError(w, http.StatusNotFound, err.Error())
		return
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]string{"message": "ecosystem removed"})
}

func (h *TrustRegistryHandlers) RecognizeEcosystem(w http.ResponseWriter, r *http.Request, params admin.RecognizeEcosystemParams) {
	did := params.Did
	if did == "" {
		writeJSONError(w, http.StatusBadRequest, "Missing required query parameter: did")
		return
	}
	egf := params.Egf
	if egf == "" {
		writeJSONError(w, http.StatusBadRequest, "Missing required query parameter: egf")
		return
	}

	// Optional scope
	var scopePtr *string
	if params.Scope != nil && *params.Scope != "" {
		scopePtr = params.Scope
	}

	// Build the request object from the generated admin package struct
	req := admin.RecognizeEcosystemParams{
		Did:   did,
		Egf:   egf,
		Scope: scopePtr,
	}

	resp, err := h.svc.RecognizeEcosystem(req)
	if err != nil {
		writeJSONError(w, http.StatusBadRequest, err.Error())
		return
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}

func (h *TrustRegistryHandlers) ListEcosystems(w http.ResponseWriter, r *http.Request) {
	ecosystems := h.svc.Registry.Ecosystems
	ecoIds := make([]string, 0, len(ecosystems))
	for _, eco := range ecosystems {
		ecoIds = append(ecoIds, eco.Metadata.DID)
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(ecoIds)

}

// AuthorizeEntry handles POST /ecosystems/authorizations
// Takes all parameters (did, egf, authorization_id, active) from the query (NOT the path).
func (h *TrustRegistryHandlers) AuthorizeEntry(w http.ResponseWriter, r *http.Request, params admin.AuthorizeEntryParams) {
	q := r.URL.Query()

	// Required: did, egf, authorization_id
	did := q.Get("did")
	if did == "" {
		writeJSONError(w, http.StatusBadRequest, "Missing required query parameter: did")
		return
	}
	egf := q.Get("egf")
	if egf == "" {
		writeJSONError(w, http.StatusBadRequest, "Missing required query parameter: egf")
		return
	}
	authID := q.Get("authorization_id")
	if authID == "" {
		writeJSONError(w, http.StatusBadRequest, "Missing required query parameter: authorization_id")
		return
	}

	// Optional active
	var activePtr *bool
	if activeStr := q.Get("active"); activeStr != "" {
		parsed, err := strconv.ParseBool(activeStr)
		if err != nil {
			writeJSONError(w, http.StatusBadRequest, "Invalid 'active' query param; must be boolean")
			return
		}
		activePtr = &parsed
	}

	// Build the request object from the generated admin package struct
	req := admin.AuthorizeEntryParams{
		Did:             did,
		Egf:             egf,
		AuthorizationId: authID,
		Active:          activePtr,
	}

	resp, err := h.svc.AuthorizeEntry(req)
	if err != nil {
		writeJSONError(w, http.StatusBadRequest, err.Error())
		return
	}

	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}
