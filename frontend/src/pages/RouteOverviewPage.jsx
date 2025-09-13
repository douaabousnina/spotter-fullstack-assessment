import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import Button from "../components/ui/form/Button";

const mockRouteData = {
  route_id: "1",
  total_distance: 1842,
  total_duration: 29.5,
  waypoints: [
    {
      address: "Chicago, IL",
      lat: 41.8781,
      lng: -87.6298,
      type: "current",
    },
    {
      address: "Milwaukee, WI",
      lat: 43.0389,
      lng: -87.9065,
      type: "pickup",
    },
    {
      address: "Des Moines, IA",
      lat: 41.5909,
      lng: -93.6208,
      type: "fuel",
    },
    {
      address: "Omaha, NE",
      lat: 41.2524,
      lng: -95.9955,
      type: "rest",
    },
    {
      address: "Denver, CO",
      lat: 39.7392,
      lng: -104.9903,
      type: "fuel",
    },
    {
      address: "Grand Junction, CO",
      lat: 39.0606,
      lng: -108.5573,
      type: "rest",
    },
    {
      address: "Phoenix, AZ",
      lat: 33.4484,
      lng: -112.074,
      type: "dropoff",
    },
  ],
  restStops: [
    {
      location: "Omaha, NE",
      latitude: 41.2524,
      longitude: -95.9955,
      stop_type: "mandatory",
      duration_minutes: 30,
    },
    {
      location: "Grand Junction, CO",
      latitude: 39.0606,
      longitude: -108.5573,
      stop_type: "mandatory",
      duration_minutes: 30,
    },
  ],
  fuelStops: [
    {
      location: "Des Moines, IA",
      latitude: 41.5909,
      longitude: -93.6208,
    },
    {
      location: "Denver, CO",
      latitude: 39.7392,
      longitude: -104.9903,
    },
  ],
};

export default function RouteOverviewPage() {
  const { routeId } = useParams();

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
          <Link to={`/logs/${routeId}`}>
            <Button variant="success" className="px-6 py-2">
              View ELD Logs
            </Button>
          </Link>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg border border-border overflow-hidden mb-8">
        <iframe
          src="https://maps.google.com/maps?q=35.856737, 10.606619&z=15&output=embed"
          width="100%"
          height="500"
          frameborder="0"
        ></iframe>

        <div className="p-4 bg-gray-50 flex flex-wrap gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-primary rounded-full border border-gray-300"></div>
            <span>Start Location</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full border border-green-300"></div>
            <span>Pickup</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full border border-red-300"></div>
            <span>Dropoff</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-orange-500 rounded-full border border-orange-300"></div>
            <span>Fuel Stop</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full border border-red-300"></div>
            <span>Mandatory Rest</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow border border-border p-6 text-center">
          <p className="text-sm text-primary mb-1">Total Distance</p>
          <p className="text-3xl font-bold text-gray-800">
            {mockRouteData.total_distance} mi
          </p>
        </div>

        <div className="bg-white rounded-xl shadow border border-border p-6 text-center">
          <p className="text-sm text-primary mb-1">Estimated Duration</p>
          <p className="text-3xl font-bold text-gray-800">
            {mockRouteData.total_duration} hrs
          </p>
        </div>

        <div className="bg-white rounded-xl shadow border border-border p-6 text-center">
          <p className="text-sm text-primary mb-1">Mandatory Rest Stops</p>
          <p className="text-3xl font-bold text-gray-800">
            {mockRouteData.restStops.length}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow border border-border p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">
          Mandatory Rest Stops
        </h2>
        <ul className="space-y-3">
          {mockRouteData.restStops.map((stop, i) => (
            <li
              key={i}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <span className="font-medium text-gray-800">
                  {stop.location}
                </span>
                <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full">
                  Mandatory Rest
                </span>
              </div>
              <span className="text-sm text-gray-600">
                {stop.duration_minutes} min
              </span>
            </li>
          ))}
        </ul>
      </div>

      <div className="bg-white rounded-xl shadow border border-border p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Fuel Stops</h2>
        <ul className="space-y-3">
          {mockRouteData.fuelStops.map((stop, i) => (
            <li
              key={i}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="font-medium text-gray-800">
                  {stop.location}
                </span>
                <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs font-medium rounded-full">
                  Fuel Stop
                </span>
              </div>
              <span className="text-sm text-gray-600">~1,000 mi apart</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
