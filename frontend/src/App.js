import React from "react";
import Dashboard from "./components/Dashboard";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  return (
    <div className="container mt-4">
      <h2>Song Dashboard</h2>
      <Dashboard />
    </div>
  );
}

export default App;
