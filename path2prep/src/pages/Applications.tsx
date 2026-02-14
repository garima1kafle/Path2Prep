import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchApplications } from '../store/slices/scholarshipSlice';

const Applications: React.FC = () => {
  const dispatch = useAppDispatch();
  const { applications, loading } = useAppSelector((state) => state.scholarships);

  useEffect(() => {
    dispatch(fetchApplications());
  }, [dispatch]);

  if (loading) {
    return <div className="p-8">Loading applications...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">My Applications</h1>
        <div className="space-y-4">
          {applications.length > 0 ? (
            applications.map((app) => (
              <div key={app.id} className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold">{app.scholarship.title}</h3>
                <p className="text-gray-600">{app.scholarship.organization}</p>
                <span className={`inline-block mt-2 px-3 py-1 rounded-full text-sm ${
                  app.status === 'submitted' ? 'bg-green-100 text-green-800' :
                  app.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {app.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No applications yet. Start applying to scholarships!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Applications;

