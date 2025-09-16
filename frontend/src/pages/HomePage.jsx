import TripForm from "../components/trip/TripForm";

export default function HomePage() {
  return (
    <div className="bg-white rounded-xl shadow-md p-10 mx-auto">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold tracking-tight text-primary">
          TruckHOS
        </h1>
        <p className="mt-2 text-secondary">
          Plan your trip. Stay compliant. Drive with confidence.
        </p>
      </div>

      <TripForm />
    </div>
  );
}
