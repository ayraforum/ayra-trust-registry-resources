package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/ghodss/yaml"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"

	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/gen/admin"
	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/gen/trqp/v2"
	registrysvc "github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/pkg/registry"
	v2trqp "github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/pkg/trqp/v2"
	"github.com/andorsk/tswg-trust-registry-protocol/reference_implementation/pkg/utils"
)

// LoadRegistry loads the trust registry data from a JSON/YAML file or environment variable.
func LoadRegistry(path string) (*utils.TrustRegistry, error) {
	var registry utils.TrustRegistry
	
	// Check if REGISTRY_DATA environment variable is set
	if registryData := os.Getenv("REGISTRY_DATA"); registryData != "" {
		log.Printf("Loading registry from REGISTRY_DATA environment variable")
		err := yaml.Unmarshal([]byte(registryData), &registry)
		if err != nil {
			return nil, fmt.Errorf("failed to parse REGISTRY_DATA: %v", err)
		}
		return &registry, nil
	}
	
	// Check if REGISTRY_PATH environment variable is set
	registryPath := getEnv("REGISTRY_PATH", path)
	log.Printf("Loading registry from file: %s", registryPath)
	
	dat, err := os.ReadFile(registryPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read registry file: %v", err)
	}
	err = yaml.Unmarshal(dat, &registry)
	if err != nil {
		return nil, fmt.Errorf("failed to parse registry file: %v", err)
	}
	return &registry, nil
}

// swaggerUI serves a Swagger UI HTML that loads a YAML spec directly.
func swaggerUI(specURL string) string {
	return strings.TrimSpace(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>API Documentation</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: '` + specURL + `',
        dom_id: '#swagger-ui',
        requestInterceptor: (req) => {
          req.headers.Accept = 'application/yaml';
          return req;
        }
      });
    };
  </script>
</body>
</html>`)
}

// getEnv gets environment variable value or returns default if not present
func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists && value != "" {
		return value
	}
	return defaultValue
}

func main() {
	// Command-line flags
	var port string
	var baseURL string
	var registryName string

	// Define flags with defaults (will be overridden by env vars if present)
	flag.StringVar(&port, "port", getEnv("PORT", "8082"), "Port to listen on")
	flag.StringVar(&baseURL, "base-url", getEnv("BASE_URL", "http://localhost"), "Base URL for services")
	flag.StringVar(&registryName, "registry-name", getEnv("REGISTRY_NAME", "Default-TR"), "Registry name")
	flag.Parse()

	log.Printf("Starting Trust Registry: %s", registryName)
	log.Printf("Port: %s", port)
	log.Printf("Base URL: %s", baseURL)

	// Load the trust registry
	defaultRegistryPath := "data/registry.json"
	registry, err := LoadRegistry(defaultRegistryPath)
	if err != nil {
		log.Fatalf("Failed to load registry: %v", err)
	}

	// -------------------------------------
	// 1) Generate the Trust Registry DID
	// -------------------------------------
	trustRegistryDID, err := utils.GenerateDidPeer2(utils.Peer2ConfigFile{
		Services: []utils.Service{
			{
				ID:   "#tr-1",
				Type: "TRQP",
				ServiceEndpoint: utils.ServiceProfile{
					Profile:   "https://trustoverip.org/profiles/trp/v2",
					URI:       baseURL + ":" + port + "/api/v2/",
					Integrity: "122041dd7b6443542e75701aa98a0c235951a28a0d851b11564d20022ab11d2589a8",
				},
			},
		},
	})
	if err != nil {
		log.Fatalf("Failed to generate Trust Registry DID: %v", err)
	}
	log.Printf("Generated Trust Registry DID: %s", trustRegistryDID)

	// -------------------------------------
	// 2) Generate the Ecosystem DID, referencing the Trust Registry DID
	// -------------------------------------
	ecosystemDID, err := utils.GenerateDidPeer2(utils.Peer2ConfigFile{
		Services: []utils.Service{
			{
				ID:   "#egfURI",
				Type: "egfURI",
				ServiceEndpoint: utils.ServiceProfile{
					Profile:   "https://trustoverip.org/profiles/trp/egfURI/v1",
					URI:       baseURL + ":" + port + "/terms",
					Integrity: "122041dd7b6443542e75701aa98a0c235951a28a0d851b11564d20022ab11d2589a8",
				},
			},
			{
				ID:   "#TRQP",
				Type: "TRQP",
				// Point this service endpoint's 'uri' to the Trust Registry DID
				ServiceEndpoint: utils.ServiceProfile{
					Profile:   "https://example.org/profiles/ecosystemService/v1",
					URI:       trustRegistryDID,
					Integrity: "example_integrity_hash_value",
				},
			},
		},
	})
	if err != nil {
		log.Fatalf("Failed to generate Ecosystem DID: %v", err)
	}
	log.Printf("Generated Ecosystem DID: %s", ecosystemDID)

	// Set the environment variables that will be used by the TRQP handler
	// This must be done BEFORE the TRQP handler is created
	os.Setenv("TRUST_REGISTRY_DID", trustRegistryDID)
	os.Setenv("ECOSYSTEM_DID", ecosystemDID)
	
	// Log the environment variable setting
	log.Printf("Setting TRUST_REGISTRY_DID: %s", trustRegistryDID)
	log.Printf("Setting ECOSYSTEM_DID: %s", ecosystemDID)

	// Create the TRQP handler with the registry
	impl := &v2trqp.TRQPHandler{
		Registry: registry,
	}
	
	// Create the registry service
	svc := &registrysvc.TrustRegistryService{Registry: registry}
	registryHandlers := registrysvc.NewTrustRegistryHandlers(svc)

	// Create a new ecosystem for runtime use
	eco := utils.NewEcosystem(utils.EcosystemMetadata{
		DID:         ecosystemDID, // root ecosystem DID
		Type:        "Root",
		Description: fmt.Sprintf("Root ecosystem for %s", registryName),
		Name:        registryName,
		Status: utils.Status{
			Active: true,
			Detail: "Active ecosystem",
		},
	})

	// Example: add an authorization type to your new root ecosystem.
	eco.AuthorizationTypes["auth1"] = utils.AuthorizationType{
		Name:        "auth1",
		Description: "Authorization type 1",
	}

	// Create the ecosystem in the registry
	if err := svc.CreateEcosystem(*eco); err != nil {
		log.Fatalf("Failed to create ecosystem: %v", err)
	}

	// Create Chi router
	r := chi.NewRouter()

	// Setup CORS
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"*"}, // Allow all origins
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300, // Maximum value not ignored by any of major browsers
	}))

	// Serve static YAML specs
	r.Get("/admin/openapi.yaml", serveYAML("api/admin.yaml"))
	r.Get("/api/v2/openapi.yaml", serveYAML("api/v2.yaml"))

	// Serve Swagger UI pages
	r.Get("/admin/docs", serveSwaggerUI("/admin/openapi.yaml"))
	r.Get("/api/v2/docs", serveSwaggerUI("/api/v2/openapi.yaml"))

	// Attach admin and TRQP routes
	adminRouter := admin.HandlerFromMux(registryHandlers, r)
	trqpRouter := trqp.HandlerFromMux(impl, r)

	r.Mount("/admin", adminRouter)
	r.Mount("/api/v2", trqpRouter)

	// Serve Terms file
	r.Get("/terms", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "terms.html")
	})

	// Add status endpoint
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `{"status":"ok","name":"%s","trust_registry_did":"%s","ecosystem_did":"%s"}`, 
			registryName, trustRegistryDID, ecosystemDID)
	})

	// Start the server
	log.Printf("Listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}

// serveYAML serves a static YAML file.
func serveYAML(filepath string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/yaml")
		http.ServeFile(w, r, filepath)
	}
}

// serveSwaggerUI serves the Swagger UI that loads the given YAML spec.
func serveSwaggerUI(specPath string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		fmt.Fprint(w, swaggerUI(specPath))
	}
}
