import React, { useEffect, useState } from 'react';
import { useAppDispatch } from '../store/hooks';
import apiService from '../services/api';

const CareerRecommendations: React.FC = () => {
  const dispatch = useAppDispatch();
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await apiService.getCareerRecommendations();
      setRecommendations(response.top_careers);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8">Loading recommendations...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">Career Recommendations</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {recommendations.map((rec, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-2">{rec.career}</h3>
              <p className="text-gray-600 mb-4">{rec.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">Confidence</span>
                <span className="text-lg font-bold text-blue-600">
                  {(rec.confidence * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CareerRecommendations;

