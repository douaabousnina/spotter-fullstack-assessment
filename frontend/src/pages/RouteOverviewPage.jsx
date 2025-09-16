import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Button from "../components/ui/form/Button";
import RouteMap from "../components/trip/Map";
import RoutingService from "../services/routingService";

export default function RouteOverviewPage() {
  const { routeId } = useParams();
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchRoute = async () => {
      try {
        setLoading(true);
        const data = await RoutingService.getTripRouteById(routeId);
        setRouteData(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load route. Try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchRoute();
  }, [routeId]);

  if (loading) return <p>Loading route...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!routeData) return <p>No route found.</p>;

  const waypoints = routeData.waypoints.map((wp) => ({
    address: wp.location.name || "",
    lat: wp.location.latitude,
    lng: wp.location.longitude,
    type: wp.type,
    time: wp.arrival_time,
  }));

  const restStops = waypoints.filter((w) => w.type === "rest");
  const fuelStops = waypoints.filter((w) => w.type === "fuel");

  const getStopLabel = (type) => {
    switch (type) {
      case "start":
        return "Start Location";
      case "pickup":
        return "Pickup Point";
      case "dropoff":
        return "Delivery Point";
      case "fuel":
        return "Fuel Stop";
      case "rest":
        return "Mandatory Rest";
      case "cycle_reset":
        return "Cycle Rest";
      default:
        return "Waypoint";
    }
  };

  const getStopColor = (type) => {
    switch (type) {
      case "start":
        return "border-l-[#0ea5e9] bg-sky-50";
      case "pickup":
        return "border-l-[#22c55e] bg-green-50";
      case "dropoff":
        return "border-l-[#3b82f6] bg-blue-50";
      case "fuel":
        return "border-l-[#f97316] bg-orange-50";
      case "rest":
      case "cycle_reset":
        return "border-l-[#ef4444] bg-red-50";
      default:
        return "border-l-gray-500 bg-gray-50";
    }
  };

  const formatDateTime = (dateTimeString) => {
    const date = new Date(dateTimeString);
    return date.toLocaleString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  };

  return (
    <div className="mx-auto p-6">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-primary">
          Your Compliant Route
        </h1>
        <div className="flex space-x-4">
          <Link to="/">
            <Button variant="secondary" className="px-5 py-2">
              ← Try Another Trip
            </Button>
          </Link>
          <Link to={`/eldLogs/${routeId}`}>
            <Button variant="success" className="px-6 py-2">
              View ELD Logs
            </Button>
          </Link>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg border border-border overflow-hidden mb-8">
        <RouteMap waypoints={waypoints} />

        <div className="p-4 bg-gray-50 flex flex-wrap gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-[#0ea5e9] rounded-full border border-gray-300"></div>
            <span>Start Location</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-[#22c55e] rounded-full border border-green-300"></div>
            <span>Pickup</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-[#3b82f6] rounded-full border border-blue-300"></div>
            <span>Dropoff</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-[#f97316] rounded-full border border-orange-300"></div>
            <span>Fuel Stop</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-[#ef4444] rounded-full border border-red-300"></div>
            <span>Mandatory Rest</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow border border-border p-6 text-center">
          <p className="text-sm text-primary mb-1">Total Distance</p>
          <p className="text-3xl font-bold text-gray-800">
            {routeData.total_distance.toFixed(1)} mi
          </p>
        </div>

        <div className="bg-white rounded-xl shadow border border-border p-6 text-center">
          <p className="text-sm text-primary mb-1">Estimated Duration</p>
          <p className="text-3xl font-bold text-gray-800">
            {(routeData.total_duration / 3600).toFixed(1)} hrs
          </p>
        </div>

        <div className="bg-white rounded-xl shadow border border-border p-6 text-center">
          <p className="text-sm text-primary mb-1">Mandatory Rest Stops</p>
          <p className="text-3xl font-bold text-gray-800">{restStops.length}</p>
        </div>
      </div>

      {/* Route Stops List */}
      <div className="bg-white rounded-xl shadow border border-border p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          Route Breakdown
        </h2>
        <div className="space-y-3">
          {waypoints.map((waypoint, index) => (
            <div
              key={index}
              className={`flex items-center p-4 rounded-lg border-l-4 ${getStopColor(
                waypoint.type
              )}`}
            >
              <div className="flex items-center space-x-4 flex-1">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
                      Stop {index + 1}
                    </span>
                    <span className="text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded-full">
                      {getStopLabel(waypoint.type)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    <strong>Estimated arrival:</strong>{" "}
                    {formatDateTime(waypoint.time)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
