import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchScholarships, matchScholarships } from '../store/slices/scholarshipSlice';
import { Link } from 'react-router-dom';

const Scholarships: React.FC = () => {
  const dispatch = useAppDispatch();
  const { scholarships, matches, loading, matchLoading, error } = useAppSelector((state) => state.scholarships);

  useEffect(() => {
    dispatch(fetchScholarships());
    dispatch(matchScholarships(10));
  }, [dispatch]);

  const isLoading = loading || matchLoading;

  if (isLoading) {
    return <div className="p-8">Loading scholarships...</div>;
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-3xl font-bold mb-6">Scholarships</h1>
          <div className="bg-red-50 text-red-700 p-4 rounded-lg">
            <p className="font-semibold">Error loading scholarships</p>
            <p className="text-sm mt-1">{error}</p>
            <button
              className="mt-3 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              onClick={() => {
                dispatch(fetchScholarships());
                dispatch(matchScholarships(10));
              }}
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">Scholarships</h1>
        <div className="space-y-4">
          {matches.length > 0 ? (
            matches.map((match) => (
              <div key={match.scholarship.id} className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-semibold">{match.scholarship.title}</h3>
                    <p className="text-gray-600">{match.scholarship.organization}</p>
                    <p className="text-sm text-gray-500 mt-2">{match.scholarship.description}</p>
                  </div>
                  <div className="text-right">
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                      {(match.relevance_score * 100).toFixed(0)}% Match
                    </span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No scholarships found. Complete your profile to get matches.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Scholarships;
