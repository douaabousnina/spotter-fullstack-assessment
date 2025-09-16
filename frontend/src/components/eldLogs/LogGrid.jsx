import React from "react";
import { DUTY_STATUSES, HOURS } from "../../utils/constants";

const LogGrid = ({ dayData }) => {
  if (!dayData || !dayData.grid) {
    return (
      <div className="border-2 border-red-500 p-4">
        <p className="text-red-500">Error: No dayData or grid provided</p>
        <pre className="text-xs">{JSON.stringify(dayData, null, 2)}</pre>
      </div>
    );
  }

  return (
    <div className="w-max border-border">
      <div className="w-full">
        <div className="flex border-b-2 border-border">
          <div className="w-32 h-36 px-2 py-3 flex items-center justify-center"></div>
          {HOURS.map((time, i) => (
            <div
              key={i}
              className="w-12 h-36 relative flex items-center justify-start"
            >
              <div
                className="absolute whitespace-nowrap text-xs font-bold text-secondary"
                style={{
                  transform: "translate(-8px, 63px) rotate(-45deg)",
                  transformOrigin: "left center",
                }}
              >
                <span className="border-b border-border pb-1 px-2">{time}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Duty rows */}
        {Object.entries(DUTY_STATUSES).map(
          ([statusKey, label], rowIdx, arr) => {
            const gridRow = dayData.grid[statusKey];

            return (
              <div
                key={statusKey}
                className={`flex ${
                  rowIdx < arr.length - 1 ? "border-b border-border" : ""
                }`}
              >
                <div className="w-32 h-16 px-2 py-4 border-r-2 text-primary border-border text-sm font-semibold flex items-center justify-center">
                  {label}
                </div>

                {(gridRow || Array(24).fill(null)).map((hasLine, hourIndex) => (
                  <div
                    key={hourIndex}
                    className={
                      "w-12 h-16 border-r border-border relative flex items-center justify-center overflow-visible"
                    }
                  >
                    {hasLine && (
                      <>
                        <div className="absolute bottom-4 h-2 w-full bg-secondary" />
                        <div className="hidden print:block text-black font-bold text-xl z-10">
                          —
                        </div>
                      </>
                    )}
                    {!gridRow && <span className="text-xs text-danger">X</span>}
                  </div>
                ))}
              </div>
            );
          }
        )}
      </div>
    </div>
  );
};

export default LogGrid;
