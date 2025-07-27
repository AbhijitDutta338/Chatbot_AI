package incidentapi

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

var (
	projectID    = "silken-zenith-466515-b8"
	baseURL      = "<<firebase-url>>"
)

type Incident struct {
	ID     string `json:"id"`
	UserID string `json:"user_id"`
	Status string `json:"status"`
	Description string `json:"description"`
	AssigneeID string `json:"assignee_id"`
    EventID string `json:"event_id`
    Type string `json:"type"`
    Zone string `json:"zone"`
}

func IncidentHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		var incident Incident
		if err := json.NewDecoder(r.Body).Decode(&incident); err != nil {
			http.Error(w, "Invalid body", http.StatusBadRequest)
			return
		}
		url := fmt.Sprintf("%s/incidents/%s.json", baseURL, incident.ID)
		postOrPatch("PUT", url, incident, w)

	case "GET":
		userID := r.URL.Query().Get("user_id")
        assigneeID := r.URL.Query().Get("assignee_id")
		var url string
		if userID != "" {
			url = fmt.Sprintf("%s/incidents.json", baseURL)
		} else if assigneeID != "" {
			url = fmt.Sprintf("%s/incidents.json?orderBy=\"assignee_id\"&equalTo=\"%s\"", baseURL, assigneeID)
		} else{
            http.Error(w, "Missing query params", http.StatusBadRequest)
			return
        }
		getAndReturn(url, w)

	case "PATCH":
		incidentID := r.URL.Query().Get("incident_id")
		status := r.URL.Query().Get("status")
		if incidentID == "" || status == "" {
			http.Error(w, "Missing query params", http.StatusBadRequest)
			return
		}
		patch := map[string]string{"status": status}
		url := fmt.Sprintf("%s/incidents/%s.json", baseURL, incidentID)
		postOrPatch("PATCH", url, patch, w)

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}


func postOrPatch(method, url string, data interface{}, w http.ResponseWriter) {
	jsonData, _ := json.Marshal(data)
	req, _ := http.NewRequest(method, url, bytes.NewBuffer(jsonData))
	req.Header.Set("Content-Type", "application/json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}

func getAndReturn(url string, w http.ResponseWriter) {
	resp, err := http.Get(url)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}
