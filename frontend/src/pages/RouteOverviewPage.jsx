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

  console.log(routeData)
  const waypoints = routeData.waypoints.map((wp) => ({
    address: wp.location.name,
    lat: wp.location.latitude,
    lng: wp.location.longitude,
    type: wp.type,
  }));

  const restStops = waypoints.filter((w) => w.type === "rest");
  const fuelStops = waypoints.filter((w) => w.type === "fuel");

  return (
    <div className="mx-auto p-6">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-primary">
          Your Compliant Route
        </h1>
        <div className="flex space-x-4">
          <Link to="/">
            <Button variant="secondary" className="px-5 py-2">
              ← Edit Trip
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
    </div>
  );
}
