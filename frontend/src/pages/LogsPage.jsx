// src/pages/LogsPage.jsx
import React from "react";
import Button from "../components/ui/form/Button";
import { Link, useNavigate, useParams } from "react-router-dom";
import LogSheet from "../components/logs/LogSheet";

const mockRouteData = {
  route_id: "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
  events: [
    // June 16
    { time: "06:00", duty_status: "driving", date: "2024-06-16" },
    { time: "08:30", duty_status: "on_duty", date: "2024-06-16" },
    { time: "09:30", duty_status: "off_duty", date: "2024-06-16" },
    { time: "10:00", duty_status: "driving", date: "2024-06-16" },
    { time: "15:00", duty_status: "driving", date: "2024-06-16" },
    { time: "17:00", duty_status: "on_duty", date: "2024-06-16" },
    { time: "18:00", duty_status: "off_duty", date: "2024-06-16" },
    { time: "19:00", duty_status: "driving", date: "2024-06-16" },
    { time: "23:00", duty_status: "driving", date: "2024-06-16" },
    { time: "23:30", duty_status: "rest", date: "2024-06-16" },
    // June 17
    { time: "00:30", duty_status: "driving", date: "2024-06-17" },
    { time: "04:00", duty_status: "driving", date: "2024-06-17" },
    { time: "06:00", duty_status: "on_duty", date: "2024-06-17" },
    { time: "07:00", duty_status: "off_duty", date: "2024-06-17" },
    { time: "08:00", duty_status: "driving", date: "2024-06-17" },
    { time: "12:00", duty_status: "driving", date: "2024-06-17" },
    { time: "13:00", duty_status: "rest", date: "2024-06-17" },
    { time: "14:00", duty_status: "driving", date: "2024-06-17" },
    { time: "19:00", duty_status: "driving", date: "2024-06-17" },
    { time: "20:00", duty_status: "on_duty", date: "2024-06-17" },
    { time: "21:00", duty_status: "sleeper_berth", date: "2024-06-17" },
  ],
};

function buildLineGrid(events) {
  const days = {};

  events.forEach((event) => {
    const date = event.date;
    if (!days[date]) days[date] = [];
    days[date].push(event);
  });

  return Object.keys(days)
    .sort()
    .map((date) => {
      const dayEvents = days[date].sort((a, b) => a.time.localeCompare(b.time));

      const grid = {
        off_duty: Array(24).fill(true),
        sleeper_berth: Array(24).fill(false),
        driving: Array(24).fill(false),
        on_duty: Array(24).fill(false),
      };

      let currentStatus = "off_duty"; // default
      let currentStartHour = 0;

      dayEvents.forEach((event) => {
        const [hourStr, minuteStr] = event.time.split(":");
        const hour = parseInt(hourStr, 10);
        const minute = parseInt(minuteStr, 10);

        let status = event.duty_status;
        if (status === "rest") status = "on_duty";

        for (let h = currentStartHour; h < hour; h++) {
          grid.off_duty[h] = false;
          grid[currentStatus][h] = true;
        }

        if (hour < 24) {
          grid.off_duty[hour] = false;
          grid[status][hour] = true;
        }

        currentStatus = status;
        currentStartHour = hour;
      });

      for (let h = currentStartHour; h < 24; h++) {
        grid.off_duty[h] = false;
        grid[currentStatus][h] = true;
      }

      return { date, grid };
    });
}

export default function LogsPage() {
  const { routeId } = useParams();
  const dailySheets = buildLineGrid(mockRouteData.events);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="mx-auto p-6 max-w-screen bg-transparent">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-primary">ELD Log Sheet(s)</h1>

        <div className="flex space-x-4">
          <Link to={`/route/${routeId}`}>
            <Button variant="secondary" className="px-5 py-2">
              ← View Route
            </Button>
          </Link>
          <Button onClick={handlePrint} variant="success" className="px-6 py-2">
            Print All Logs
          </Button>
        </div>
      </div>

      {dailySheets.map((dayData, idx) => (
        <LogSheet key={dayData.date} dayData={dayData} index={idx} />
      ))}
    </div>
  );
}
