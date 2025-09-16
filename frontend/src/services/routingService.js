import apiClient from "./apiClient";

const RoutingService = {
  async getTripRoute(payload) {
    try {
      const response = await apiClient.post("/trips/routes/", payload);
      return response.data;
    } catch (error) {
      console.error("Error fetching trip route:", error);
      throw error.response?.data || error.message;
    }
  },

  async getTripRouteById(routeId) {
    try {
      const response = await apiClient.get(`/trips/routes/${routeId}/`);
      return response.data;
    } catch (error) {
      console.error("Error fetching trip route:", error);
      throw error.response?.data || error.message;
    }
  },
};

export default RoutingService;
