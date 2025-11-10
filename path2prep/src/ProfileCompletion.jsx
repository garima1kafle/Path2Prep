import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ProfileCompletion.css';

const ProfileCompletion = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    skills: '',
    financialNeed: '',
    careerGoals: '',
    agreedToTerms: false
  });

  const financialNeedOptions = [
    'No financial aid needed',
    'Low financial need',
    'Moderate financial need',
    'High financial need',
    'Full scholarship required'
  ];

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePrevious = () => {
    navigate('/career-interests');
  };

  // In ProfileCompletion.jsx, update the handleSubmit function:
const handleSubmit = () => {
  console.log('Profile completed:', formData);
  // Navigate to dashboard after profile completion
  navigate('/dashboard');
};

  return (
    <div className="profile-completion-container">
      <div className="profile-completion-card">
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
            <div className="step-indicator">Step 4 of 4</div>
          </div>
          <div className="progress-bar">
            <div className="progress-fill step-4"></div>
          </div>
        </div>
        
        <div className="completion-form">
          <div className="form-section">
            <div className="form-field">
              <label className="field-label">Skills & Achievements</label>
              <div className="textarea-field">
                <textarea
                  placeholder="Tell us about your skills, achievements, extracurricular activities, work experience, etc."
                  value={formData.skills}
                  onChange={(e) => handleChange('skills', e.target.value)}
                  className="form-textarea"
                  rows={3}
                />
              </div>
            </div>
            
            <div className="form-field">
              <label className="field-label">Financial Need Level</label>
              <div className="select-field">
                <span className="select-text">
                  {formData.financialNeed || 'Select level'}
                </span>
                <div className="dropdown-arrow">
                  <div className="arrow-down"></div>
                </div>
                <select
                  value={formData.financialNeed}
                  onChange={(e) => handleChange('financialNeed', e.target.value)}
                  className="select-hidden"
                >
                  <option value="">Select level</option>
                  {financialNeedOptions.map((option, index) => (
                    <option key={index} value={option}>{option}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="form-field">
              <label className="field-label">Career Goals</label>
              <div className="textarea-field">
                <textarea
                  placeholder="Describe your career aspirations and long-term goals"
                  value={formData.careerGoals}
                  onChange={(e) => handleChange('careerGoals', e.target.value)}
                  className="form-textarea"
                  rows={3}
                />
              </div>
            </div>
            
            <div className="checkbox-agreement">
              <div 
                className={`checkbox-box ${formData.agreedToTerms ? 'checked' : ''}`}
                onClick={() => handleChange('agreedToTerms', !formData.agreedToTerms)}
              >
                {formData.agreedToTerms && (
                  <div className="checkmark">✓</div>
                )}
              </div>
              <span className="agreement-text">
                I agree to the Terms of Service and Privacy Policy
              </span>
            </div>
          </div>
          
          <div className="form-navigation">
            <button className="previous-button" onClick={handlePrevious}>Previous</button>
            <button 
              className="complete-button" 
              onClick={handleSubmit}
              disabled={!formData.agreedToTerms}
            >
              Complete Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileCompletion;