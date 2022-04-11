import React from "react";
import "./index.css";
import App from "./App";
import SearchBars from "./SearchBar/index";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CompanyContext } from "./CompanyData";
import DashBoard from "./DashBoard/index";
export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/search" element={<SearchBars />} />
        <Route path="/dashboard" element={<DashBoard />} />
      </Routes>
    </BrowserRouter>
  );
}
