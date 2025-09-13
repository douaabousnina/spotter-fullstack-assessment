export const HOS_RULES = {
  MAX_DRIVE_TIME: 11, // hours
  MAX_DUTY_WINDOW: 14, // hours
  REQUIRED_REST: 10, // hours off after 14h
  BREAK_AFTER_HOURS: 8, // mandatory break after 8h driving
  FUEL_STOP_INTERVAL: 1000, // miles
  PICKUP_DROP_OFF_TIME: 1, // hour added for loading/unloading
};

export const DUTY_STATUSES = {
  off_duty: "Off-Duty",
  sleeper_berth: "Sleeper Berth",
  driving: "Driving",
  on_duty: "On-Duty",
};

export const STOP_TYPES = {
  mandatory: "Mandatory Rest",
  fuel: "Fuel Stop",
  meal: "Meal Break",
};

export const HOURS = Array.from({ length: 25 }, (_, i) => {
  if (i === 0 || i === 24) return "12 AM";
  if (i === 12) return "12 PM";
  if (i < 12) return `${i}`;
  return `${i - 12}`;
});
