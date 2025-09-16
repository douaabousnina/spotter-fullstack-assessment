import React from "react";
import LogGrid from "./LogGrid";

const LogSheet = ({ dayData, index }) => {
  return (
    <div key={index} className="mb-12 print:break-after-page">
      <div className="print-landscape-container">
        <div className="w-max bg-white rounded-xl shadow-lg border border-border p-6 print:shadow-none print:border-none print:p-4">
          <div className="flex justify-between items-start mb-6 print:items-center">
            <h2 className="text-2xl font-bold text-primary">
              Driver's Daily Log
            </h2>
            <p className="text-sm text-secondary font-medium">
              Date: {dayData.date}
            </p>
          </div>

          {/* Trip Info */}
          <div className="grid grid-cols-2 gap-4 mb-6 text-sm text-text">
            <p>
              <span className="font-semibold">From:</span> __________________
            </p>
            <p>
              <span className="font-semibold">To:</span> __________________
            </p>
          </div>

          <div className="flex justify-between">
            <div>
              {/* Mileage */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-primary mb-2">
                  Mileage
                </h3>
                <div className="space-y-1 text-text">
                  <p>
                    Total Miles Driving Today:{" "}
                    <span className="font-medium">__________________ mi</span>
                  </p>
                  <p>
                    Total Mileage Today:{" "}
                    <span className="font-medium">__________________ mi</span>
                  </p>
                </div>
              </div>

              {/* Vehicle Info */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-primary mb-2">
                  Vehicle Information
                </h3>
                <p className="text-text">
                  Truck/Tractor and Trailer Numbers: __________________
                </p>
              </div>
            </div>

            {/* Carrier Info */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-primary mb-2">
                Carrier Information
              </h3>
              <div className="space-y-1 text-text">
                <p>Name of Carrier or Carriers: __________________</p>
                <p>Main Office Address: __________________</p>
                <p>Home Terminal Address: __________________</p>
              </div>
            </div>
          </div>

          {/* Grid — Ensure this is printed fully */}
          <LogGrid dayData={dayData} />

          {/* Recap Section */}
          <div className="mt-8 border-t border-border/20 pt-6">
            <h3 className="text-lg font-semibold text-primary mb-4">Recap</h3>

            <div className="space-y-3 text-text text-sm">
              <p>
                <span className="font-medium">On duty hours today:</span>{" "}
                _______
              </p>

              <div>
                <p>
                  <span className="font-medium">A.</span> Total hours on duty
                  last 7 days including today: _______
                </p>
              </div>
              <div>
                <p>
                  <span className="font-medium">B.</span> Total hours available
                  tomorrow (70 - A): _______
                </p>
              </div>
              <div>
                <p>
                  <span className="font-medium">C.</span> Total hours on duty
                  last 5 days including today: _______
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogSheet;
