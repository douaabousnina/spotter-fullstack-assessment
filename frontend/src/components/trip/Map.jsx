import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import LocationService from "../../services/LocationService";

const MARKER_COLOR_MAP = {
  current: "grey",
  pickup: "green",
  dropoff: "blue",
  fuel: "orange",
  rest: "red",
};

export default function RouteMap({ waypoints }) {
  const [waypointsWithNames, setWaypointsWithNames] = useState([]);

  useEffect(() => {
    if (!waypoints || waypoints.length === 0) return;

    const fetchPlaceNames = async () => {
      const updated = await Promise.all(
        waypoints.map(async (wp) => {
          return await LocationService.getLocationName(wp);
        })
      );

      setWaypointsWithNames(updated);
    };

    fetchPlaceNames();
  }, [waypoints]);

  if (!waypoints || waypoints.length === 0) return null;

  const polylinePoints = waypointsWithNames.map((wp) => [wp.lat, wp.lng]);

  // Fix default Leaflet icons
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl:
      "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  });

  return (
    <MapContainer
      center={[waypoints[0].lat, waypoints[0].lng]}
      zoom={6}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      />

      <Polyline positions={polylinePoints} color="blue" weight={3} />

      {waypointsWithNames.map((wp, index) => {
        const color = MARKER_COLOR_MAP[wp.type] || "blue";

        const icon = new L.Icon({
          iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,
          shadowUrl:
            "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41],
        });

        return (
          <Marker key={index} position={[wp.lat, wp.lng]} icon={icon}>
            <Popup>
              <strong className="capitalize">{wp.type}</strong>
              <br />
              {wp.name}
              <br />
              Lat: {wp.lat.toFixed(6)}, Lng: {wp.lng.toFixed(6)}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
