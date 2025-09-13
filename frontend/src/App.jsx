import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import RouteOverviewPage from "./pages/RouteOverviewPage";
import NotFoundPage from "./pages/NotFoundPage";
import LogsPage from "./pages/LogsPage";
import Footer from "./components/layout/Footer";

export default function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-background">
        <div className="flex-1 flex flex-col">
          <main className="flex-1 p-6 overflow-y-auto">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/route/:routeId" element={<RouteOverviewPage />} />
              <Route path="/logs/:routeId" element={<LogsPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </main>

          <Footer />
        </div>
      </div>
    </Router>
  );
}
