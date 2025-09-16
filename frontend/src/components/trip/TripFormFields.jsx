import React from "react";
import { Controller } from "react-hook-form";
import NumberInput from "../ui/form/NumberInput";
import { HOS_RULES } from "../../utils/constants";
import LocationInput from "../ui/form/LocationInput";

export default function TripFormFields({
  control,
  register,
  errors,
  setCurrentLocation,
  setPickupLocation,
  setDropoffLocation,
}) {
  return (
    <>
      <Controller
        name="current_location"
        control={control}
        rules={{ required: "Enter where you are now" }}
        render={({ field }) => (
          <LocationInput
            label="Current Location"
            defaultValue={field.value}
            onSelect={(loc) => {
              field.onChange(loc.address);
              setCurrentLocation({
                latitude: loc.latitude,
                longitude: loc.longitude,
              });
            }}
          />
        )}
      />

      <Controller
        name="pickup_location"
        control={control}
        rules={{ required: "Where will you pick up?" }}
        render={({ field }) => (
          <LocationInput
            label="Pickup Location"
            defaultValue={field.value}
            onSelect={(loc) => {
              field.onChange(loc.address);
              setPickupLocation({
                latitude: loc.latitude,
                longitude: loc.longitude,
              });
            }}
          />
        )}
      />

      <Controller
        name="dropoff_location"
        control={control}
        rules={{ required: "Where is your delivery?" }}
        render={({ field }) => (
          <LocationInput
            label="Dropoff Location"
            defaultValue={field.value}
            onSelect={(loc) => {
              field.onChange(loc.address);
              setDropoffLocation({
                latitude: loc.latitude,
                longitude: loc.longitude,
              });
            }}
          />
        )}
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
