import { z } from "zod";
import { HOS_RULES } from "../utils/constants";

const tripFormSchema = z.object({
  current_location: z.string().min(3, "Enter where you are now"),
  pickup_location: z.string().min(3, "Where will you pick up?"),
  dropoff_location: z.string().min(3, "Where is your delivery?"),
  current_cycle_hours: z
    .number()
    .min(0, "Cannot be negative")
    .max(
      HOS_RULES.MAX_DUTY_WINDOW,
      `Cannot exceed ${HOS_RULES.MAX_DUTY_WINDOW} hours`
    ),
});

export default tripFormSchema;
