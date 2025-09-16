import React, { useState, useEffect } from "react";
import LocationService from "../../../services/LocationService";

export default function LocationInput({
  label,
  onSelect,
  defaultValue,
  error,
}) {
  const [query, setQuery] = useState(defaultValue || "");
  const [results, setResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    if (!query || query.length < 2) {
      setResults([]);
      return;
    }

    const fetchData = async () => {
      try {
        const res = await LocationService.getLocationCoordinates(query);
        setResults(res || []);
      } catch (err) {
        console.error("Error fetching location coordinates:", err);
        setResults([]);
      }
    };

    fetchData();
  }, [query]);

  const handleSelect = (place) => {
    setQuery(place.formatted);
    setResults([]);
    setShowDropdown(false);
    onSelect({
      address: place.formatted,
      latitude: place.geometry.lat,
      longitude: place.geometry.lng,
    });
  };

  return (
    <div className="space-y-1 relative">
      {label && (
        <label className="block text-sm font-medium text-primary">
          {label}
        </label>
      )}
      <input
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setShowDropdown(true);
        }}
        placeholder="Type a location..."
        className={`w-full px-4 py-3 border rounded-lg transition-all ${
          error ? "border-danger ring-1 ring-danger" : "border-gray-300"
        }`}
      />
      {showDropdown && results.length > 0 && (
        <ul className="absolute z-50 w-full bg-white border border-gray-300 rounded max-h-40 overflow-y-auto mt-1 shadow-lg">
          {results.map((place, idx) => (
            <li
              key={idx}
              className="p-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleSelect(place)}
            >
              {place.formatted}
            </li>
          ))}
        </ul>
      )}
      {error && <p className="text-sm text-danger">{error}</p>}
    </div>
  );
}
