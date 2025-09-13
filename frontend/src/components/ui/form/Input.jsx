import React from "react";

export default function Input({ label, error, className = "", ...props }) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-primary">
          {label}
        </label>
      )}
      <input
        className={`w-full px-4 py-3 border border-gray-300 rounded-lg transition-all ${className} ${
          error ? "border-danger ring-1 ring-danger" : ""
        }`}
        {...props}
      />
      {error && <p className="text-sm text-danger">{error}</p>}
    </div>
  );
}
