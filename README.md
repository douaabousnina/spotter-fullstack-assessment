# 🚚 ELD Routing & Trip Planner

This project is part of an **assessment**. It demonstrates a web application for planning truck routes, managing Hours of Service (HOS) limits, and generating mock ELD logs.  

---

## 🔗 Live Demo
- 🌍 Hosted Demo: [https://spotter-fullstack-assessment.vercel.app]

---

## 📌 Features Implemented
- Interactive trip creation form with:
  - **Location search & autocomplete** (via OpenStreetMap / OpenCage API)  
  - Support for current, pickup, and dropoff locations  
  - Validation with **React Hook Form** + **Zod**  
- Route generation with HOS rules:
  - Maximum driving & duty window enforcement  
  - Fuel stops and rest break insertion  
- Interactive map with **Leaflet**:
  - Custom-colored markers (current, pickup, dropoff, fuel, rest)  
  - Popups showing place names & coordinates  
  - Route polyline between waypoints  
- Frontend built with **React** + **Vite**  

---

## ⚠️ Notes / Limitations
- **ELD Sheets:** Currently implemented with **mock data only**.  
  - Not fully integrated with backend APIs.  
  - No full testing done yet.  
- Backend integration was only partially explored.  

---

## 🛠️ Tech Stack
- **Frontend:** React, React Hook Form, Zod, Axios, TailwindCSS  
- **Mapping:** Leaflet, OpenStreetMap tiles, OpenCage Geocoding API  
- **Backend:** Django
