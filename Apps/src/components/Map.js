import React, { useEffect, useRef } from "react";

const DEFAULT_COORDS = { lat: 12.9948, lng: 77.5800 };

function loadGoogleMapsScript(callback) {
  if (window.google && window.google.maps) {
    callback();
    return;
  }
  const scriptId = "google-maps-script";
  if (document.getElementById(scriptId)) {
    // Script already exists, wait for it to load
    window.initMapCallback = callback;
    return;
  }
  window.initMapCallback = callback;
  const script = document.createElement("script");
  script.id = scriptId;
  script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyCAL5F16dzbwZUDAm9nuia2YzQFDs0OFgg&callback=initMapCallback";
  script.async = true;
  script.defer = true;
  document.body.appendChild(script);
}

const Map = ({ lat, lng }) => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const markerInstance = useRef(null);

  useEffect(() => {
    function initMap() {
      const center = {
        lat: typeof lat === "number" ? lat : DEFAULT_COORDS.lat,
        lng: typeof lng === "number" ? lng : DEFAULT_COORDS.lng,
      };
      if (!mapInstance.current) {
        mapInstance.current = new window.google.maps.Map(mapRef.current, {
          zoom: 12,
          center,
        });
      } else {
        mapInstance.current.setCenter(center);
      }
      if (markerInstance.current) {
        markerInstance.current.setMap(null);
      }
      markerInstance.current = new window.google.maps.Marker({
        position: center,
        map: mapInstance.current,
        title: "Location",
      });
    }
    loadGoogleMapsScript(initMap);
    // Clean up marker on unmount
    return () => {
      if (markerInstance.current) {
        markerInstance.current.setMap(null);
      }
    };
  }, [lat, lng]);

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
       <br/>
      <div
        ref={mapRef}
        style={{
          width: '100%',
          height: '100%',
          minHeight: 120,
          maxHeight: 320,
          flex: 1,
          borderRadius: 12,
          boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
        }}
        id="map"
      />
    </div>
  );
};

export default Map;
