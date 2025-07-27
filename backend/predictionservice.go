package predictionapi

import (
	"io"
	"net/http"
)

var (
	baseURL      = "<<firebase_cloud_func_endpoint>>"
)


func PredictiontHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
		case "GET":
		getAndReturn(baseURL, w)

		default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
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
