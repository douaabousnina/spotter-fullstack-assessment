import axios from "axios";

const locationAPIClient = axios.create({
  baseURL: "https://api.opencagedata.com/geocode/v1/json",
  headers: {
    "Content-Type": "application/json",
  },
  params: {
    language: "en",
    key: import.meta.env.VITE_MAP_SEARCH_API_KEY,
  },
});

const LocationService = {
  async getLocationName({ lat, lng }) {
    try {
      const res = await locationAPIClient.get("", {
        params: {
          q: `${lat},${lng}`,
        },
      });
      const name = res.data.results[0]?.formatted || null;
      return { lat, lng, name };
    } catch (err) {
      console.error("getLocationName error:", err);
      return { lat, lng, name: null };
    }
  },

  async getLocationCoordinates(name) {
    try {
      const res = await locationAPIClient.get("", {
        params: {
          q: name,
        },
      });

      if (!res.data.results.length) return null;

      const locations = res.data.results.map((item) => {
        return {
          formatted: item.formatted,
          lat: item.geometry.lat,
          lng: item.geometry.lng,
        };
      });

      return locations;
    } catch (err) {
      console.error("getLocationCoordinates error:", err);
      return null;
    }
  },
};

export default LocationService;
