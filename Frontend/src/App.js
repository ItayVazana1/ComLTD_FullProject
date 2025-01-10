import React, { useState, useEffect } from 'react';
import { useLocation, Route, Routes, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import DataPlans from './pages/DataPlans';
import Contact from './pages/Contact';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import AddCustomer from './pages/AddCustomer';
import SearchCustomer from './pages/SearchCustomer';
import UserProfile from './pages/UserProfile';
import ChangePassword from './pages/ResetPassword';
import ModalLoader from './components/ModalLoader';
import PageNotFound from './pages/404Page.js';

/**
 * App Component:
 * Handles routing, authentication, and loading animations.
 */
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => JSON.parse(localStorage.getItem('isAuthenticated')) || false
  );
  const [username, setUsername] = useState(() => localStorage.getItem('username') || ''); // State to store username
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const location = useLocation(); // Use location to track route changes

  useEffect(() => {
    // Show loader on route change
    setIsLoading(true);

    // Hide loader after 500ms
    const timer = setTimeout(() => setIsLoading(false), 500);

    return () => clearTimeout(timer);
  }, [location]);

  const handleLogin = (name) => {
    setIsAuthenticated(true);
    setUsername(name); // Save username
    localStorage.setItem('isAuthenticated', true);
    localStorage.setItem('username', name); // Save username to localStorage
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUsername(''); // Clear username
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username'); // Remove username from localStorage
  };

  const ProtectedRoute = ({ element }) => {
    return isAuthenticated ? element : <Navigate to="/login" />;
  };

  return (
    <>
      {isLoading && <ModalLoader />}
      <Routes>
        {/* Public Routes */}
        <Route
          path="/login"
          element={<Login onLogin={handleLogin} />}
        />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute
              element={<Home username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/about"
          element={
            <ProtectedRoute
              element={<About username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/data-plans"
          element={
            <ProtectedRoute
              element={<DataPlans username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/contact"
          element={
            <ProtectedRoute
              element={<Contact username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/customers/new"
          element={
            <ProtectedRoute
              element={<AddCustomer username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/customers/search"
          element={
            <ProtectedRoute
              element={<SearchCustomer username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/account/profile"
          element={
            <ProtectedRoute
              element={<UserProfile username={username} onLogout={handleLogout} />}
            />
          }
        />
        <Route
          path="/account/change-password"
          element={
            <ProtectedRoute
              element={<ChangePassword username={username} onLogout={handleLogout} />}
            />
          }
        />

        {/* Fallback Route (404) */}
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}

export default App;
