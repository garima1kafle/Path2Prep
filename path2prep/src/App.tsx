import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { getCurrentUser } from './store/slices/authSlice';
import { fetchProfile } from './store/slices/profileSlice';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import CareerRecommendations from './pages/CareerRecommendations';
import Scholarships from './pages/Scholarships';
import Applications from './pages/Applications';
import Navbar from './components/Navbar';

function AppContent() {
  const dispatch = useAppDispatch();
  const { isAuthenticated, user } = useAppSelector((state) => state.auth);
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token && !user) {
      dispatch(getCurrentUser());
    }
  }, [dispatch, user]);

  // Fetch profile for authenticated users (needed by Navbar for avatar)
  useEffect(() => {
    if (isAuthenticated) {
      dispatch(fetchProfile());
    }
  }, [dispatch, isAuthenticated]);

  // Hide navbar on login/register pages
  const hideNavbar = ['/login', '/register'].includes(location.pathname);

  return (
    <div className="App min-h-screen bg-gray-50">
      {!hideNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/profile"
          element={isAuthenticated ? <Profile /> : <Navigate to="/login" />}
        />
        <Route
          path="/career-recommendations"
          element={isAuthenticated ? <CareerRecommendations /> : <Navigate to="/login" />}
        />
        <Route
          path="/scholarships"
          element={<Scholarships />}
        />
        <Route
          path="/applications"
          element={isAuthenticated ? <Applications /> : <Navigate to="/login" />}
        />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
