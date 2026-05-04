import React from "react";
import { useNavigate, useLocation } from "react-router-dom";

function NavBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const isLoggedIn = location.pathname !== "/login";

  const handleLogout = () => {
    navigate("/login");
  };

  return (
    <div className="fixed top-0 left-0 w-full z-50 bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        
        {/* Logo */}
        <h1
          onClick={() => navigate("/select")}
          className="text-lg font-bold text-gray-800 cursor-pointer"
        >
          Personality App
        </h1>

        {/* Right Side Button */}
        <div>
          {!isLoggedIn ? (
            <button
              onClick={() => navigate("/login")}
              className="border border-blue-500 text-blue-500 px-4 py-1.5 rounded-lg hover:bg-blue-500 hover:text-white transition"
            >
              Login
            </button>
          ) : (
            <button
              onClick={handleLogout}
              className="border border-red-500 text-red-500 px-4 py-1.5 rounded-lg hover:bg-red-500 hover:text-white transition"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default NavBar;