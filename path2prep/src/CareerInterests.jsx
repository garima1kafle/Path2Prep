import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CareerInterests.css';

const CareerInterests = () => {
  const navigate = useNavigate();
  const [selectedCareers, setSelectedCareers] = useState([]);
  const [selectedDestinations, setSelectedDestinations] = useState([]);

  const careerOptions = [
    'Technology',
    'Healthcare',
    'Finance',
    'Education',
    'Research',
    'Engineering',
    'Arts & Design',
    'Business'
  ];

  const destinationOptions = [
    'United States',
    'Canada',
    'United Kingdom',
    'Australia',
    'Germany',
    'Netherlands',
    'Singapore',
    'Other'
  ];

  const handleCareerToggle = (career) => {
    if (selectedCareers.includes(career)) {
      setSelectedCareers(selectedCareers.filter(item => item !== career));
    } else {
      setSelectedCareers([...selectedCareers, career]);
    }
  };

  const handleDestinationToggle = (destination) => {
    if (selectedDestinations.includes(destination)) {
      setSelectedDestinations(selectedDestinations.filter(item => item !== destination));
    } else {
      setSelectedDestinations([...selectedDestinations, destination]);
    }
  };

  const handlePrevious = () => {
    navigate('/academic-info');
  };

  // In CareerInterests.jsx, update the handleNext function:
const handleNext = () => {
  navigate('/profile-completion');
};

  return (
    <div className="career-interests-container">
      <div className="career-interests-card">
        <div className="profile-header">
          <div className="logo-section">
            <div className="logo-icon">
              <div className="icon-top"></div>
              <div className="icon-bottom"></div>
            </div>
            <span className="logo-text">Path2Prep</span>
          </div>
          <div className="step-info">
            <div className="step-title">Create Your Profile</div>
            <div className="step-indicator">Step 3 of 4</div>
          </div>
          <div className="progress-bar">
            <div className="progress-fill step-3"></div>
          </div>
        </div>
        
        <div className="interests-form">
          <div className="form-section">
            <div className="checkbox-section">
              <label className="section-label">Career Interests (Select all that apply)</label>
              <div className="checkbox-grid">
                {careerOptions.map((career, index) => (
                  <div 
                    key={index}
                    className="checkbox-item"
                    onClick={() => handleCareerToggle(career)}
                  >
                    <div className={`checkbox-box ${selectedCareers.includes(career) ? 'checked' : ''}`}>
                      {selectedCareers.includes(career) && (
                        <div className="checkmark">✓</div>
                      )}
                    </div>
                    <span className="checkbox-label">{career}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="checkbox-section">
              <label className="section-label">Preferred Study Destinations</label>
              <div className="checkbox-grid">
                {destinationOptions.map((destination, index) => (
                  <div 
                    key={index}
                    className="checkbox-item"
                    onClick={() => handleDestinationToggle(destination)}
                  >
                    <div className={`checkbox-box ${selectedDestinations.includes(destination) ? 'checked' : ''}`}>
                      {selectedDestinations.includes(destination) && (
                        <div className="checkmark">✓</div>
                      )}
                    </div>
                    <span className="checkbox-label">{destination}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="form-navigation">
            <button className="previous-button" onClick={handlePrevious}>Previous</button>
            <button className="next-button" onClick={handleNext}>Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerInterests;