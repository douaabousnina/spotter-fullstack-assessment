import Input from "../ui/form/Input";
import NumberInput from "../ui/form/NumberInput";
import { HOS_RULES } from "../../utils/constants";

export default function TripFormFields({ register, errors }) {
  return (
    <>
      <Input
        label="Current Location"
        placeholder="e.g., Chicago, IL"
        {...register("current_location")}
        error={errors.current_location?.message}
      />
      <Input
        label="Pickup Location"
        placeholder="e.g., Milwaukee, WI"
        {...register("pickup_location")}
        error={errors.pickup_location?.message}
      />
      <Input
        label="Dropoff Location"
        placeholder="e.g., Phoenix, AZ"
        {...register("dropoff_location")}
        error={errors.dropoff_location?.message}
      />
      <NumberInput
        label="Hours Already Driven In Current Cycle"
        step={1}
        min={0}
        max={HOS_RULES.MAX_DUTY_WINDOW}
        {...register("current_cycle_hours", { valueAsNumber: true })}
        error={errors.current_cycle_hours?.message}
      />
    </>
  );
}
