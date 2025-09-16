import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

import TripFormFields from "./TripFormFields";
import Button from "../ui/form/Button";
import tripFormSchema from "../../schemas/tripFormSchema";
import Loading from "../ui/Loading";
import RoutingService from "../../services/routingService";

export default function TripForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentLocation, setCurrentLocation] = useState(null);
  const [pickupLocation, setPickupLocation] = useState(null);
  const [dropoffLocation, setDropoffLocation] = useState(null);

  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(tripFormSchema),
    defaultValues: { current_cycle_hours: 0 },
  });

  const onSubmit = async (data) => {
    if (!currentLocation || !pickupLocation || !dropoffLocation) {
      setError("Please select all locations from the dropdown.");
      return;
    }

    const payload = {
      current: {
        latitude: currentLocation.latitude,
        longitude: currentLocation.longitude,
      },
      origin: {
        latitude: pickupLocation.latitude,
        longitude: pickupLocation.longitude,
      },
      destination: {
        latitude: dropoffLocation.latitude,
        longitude: dropoffLocation.longitude,
      },
      current_cycle_hours: data.current_cycle_hours,
    };

    const res = await RoutingService.getTripRoute(payload);
    navigate(`/route/${res.id}`);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <TripFormFields
        register={register}
        errors={errors}
        control={control}
        setCurrentLocation={setCurrentLocation}
        setDropoffLocation={setDropoffLocation}
        setPickupLocation={setPickupLocation}
      />

      {error && (
        <p className="p-3 text-sm text-danger bg-red-50 rounded-md">{error}</p>
      )}

      <div className="flex justify-end">
        <Button variant="primary" type="submit" disabled={isLoading}>
          {isLoading ? <Loading /> : "Generate Route & ELD Logs"}
        </Button>
      </div>
    </form>
  );
}
