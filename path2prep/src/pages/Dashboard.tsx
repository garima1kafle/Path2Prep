import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { logout } from '../store/slices/authSlice';
import { fetchProfile } from '../store/slices/profileSlice';
import { matchScholarships, fetchApplications } from '../store/slices/scholarshipSlice';
import { fetchNotifications, fetchUnreadCount } from '../store/slices/notificationSlice';
import apiService from '../services/api';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);
  const { profile } = useAppSelector((state) => state.profile);
  const { matches, applications } = useAppSelector((state) => state.scholarships);
  const { unreadCount } = useAppSelector((state) => state.notifications);

  useEffect(() => {
    dispatch(fetchProfile());
    dispatch(matchScholarships(5));
    dispatch(fetchApplications());
    dispatch(fetchUnreadCount());
  }, [dispatch]);

  const handleLogout = async () => {
    await dispatch(logout());
    navigate('/');
  };

  const handleGetRecommendations = async () => {
    try {
      await apiService.getCareerRecommendations();
      navigate('/career-recommendations');
    } catch (error) {
      console.error('Error getting recommendations:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold text-blue-600">Path2Prep</h1>
            <div className="flex items-center space-x-4">
              <Link to="/notifications" className="relative">
                <span className="text-gray-600 hover:text-blue-600">Notifications</span>
                {unreadCount > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </Link>
              <Link to="/profile" className="text-gray-600 hover:text-blue-600">
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-blue-600"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.full_name || user?.username}!
          </h2>
          <p className="text-gray-600 mt-2">Here's your personalized dashboard</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-sm font-medium text-gray-500">Recommended Scholarships</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">{matches.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-sm font-medium text-gray-500">Applications</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">{applications.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-sm font-medium text-gray-500">Unread Notifications</h3>
            <p className="text-3xl font-bold text-orange-600 mt-2">{unreadCount}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-sm font-medium text-gray-500">Profile Complete</h3>
            <p className="text-3xl font-bold text-purple-600 mt-2">
              {profile ? 'Yes' : 'No'}
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Career Recommendations</h3>
            <p className="text-gray-600 mb-4">
              Get AI-powered career recommendations based on your profile
            </p>
            <button
              onClick={handleGetRecommendations}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Get Recommendations
            </button>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Scholarship Matches</h3>
            <p className="text-gray-600 mb-4">
              View your personalized scholarship matches
            </p>
            <Link
              to="/scholarships"
              className="inline-block bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
            >
              View Matches
            </Link>
          </div>
        </div>

        {/* Recent Matches */}
        {matches.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Top Scholarship Matches</h3>
            <div className="space-y-4">
              {matches.slice(0, 3).map((match) => (
                <div key={match.scholarship.id} className="border-b pb-4 last:border-0">
                  <h4 className="font-semibold text-lg">{match.scholarship.title}</h4>
                  <p className="text-gray-600 text-sm">{match.scholarship.organization}</p>
                  <p className="text-blue-600 text-sm mt-1">
                    Match Score: {(match.relevance_score * 100).toFixed(0)}%
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;

