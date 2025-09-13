import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import TripFormFields from "./TripFormFields";
import Button from "../ui/form/Button";
import Spinner from "../ui/Spinner";
import tripFormSchema from "../../schemas/tripFormSchema";
// import apiClient from '../../services/apiClient'

export default function TripForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(tripFormSchema),
    defaultValues: { current_cycle_hours: 0 },
  });

  const onSubmit = async (data) => {
    setIsLoading(true);
    setError("");
    try {
      console.log("Trip submitted", data);
    } catch (err) {
      console.error(err);
      setError("Failed to generate route. Check your connection or try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <TripFormFields register={register} errors={errors} />

      {error && (
        <p className="p-3 text-sm text-red-700 bg-red-50 rounded-md">{error}</p>
      )}

      <div className="flex justify-end">
        <Button
          type="submit"
          disabled={isLoading}
          className="w-max py-3 rounded-md bg-cyan-500 hover:bg-cyan-600 cursor-pointer text-white font-medium tracking-wide transition-colors"
        >
          {isLoading ? <Spinner /> : "Generate Route & ELD Logs"}
        </Button>
      </div>
    </form>
  );
}
