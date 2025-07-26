import { initializeApp } from "firebase/app";
import { getFirestore, collection, onSnapshot } from "firebase/firestore";

const firebaseConfig = { /* your config */ };
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

onSnapshot(collection(db, "LiveLocations"), (snapshot) => {
  const heatmapData = [];

  snapshot.forEach(doc => {
    const data = doc.data();
    heatmapData.push(new google.maps.LatLng(data.lat, data.lng));
  });

  heatmap.setData(heatmapData);
});