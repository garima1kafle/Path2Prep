import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreateProfile.css';

const CreateProfile = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    country: '',
    age: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleNext = () => {
    // You can add form validation here before navigating
    console.log('Form data:', formData);
    navigate('/academic-info');
  };

  return (
    <div className="create-profile-container">
      <div className="create-profile-card">
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
            <div className="step-indicator">Step 1 of 4</div>
          </div>
          <div className="progress-bar">
            <div className="progress-fill step-1"></div>
          </div>
        </div>
        
        <div className="profile-form">
          <div className="form-section">
            <div className="form-field">
              <label htmlFor="fullName" className="field-label">Full Name</label>
              <input
                id="fullName"
                name="fullName"
                type="text"
                className="input-field"
                placeholder="Enter your full name"
                value={formData.fullName}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-field">
              <label htmlFor="email" className="field-label">Email Address</label>
              <input
                id="email"
                name="email"
                type="email"
                className="input-field"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-field">
              <label htmlFor="password" className="field-label">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                className="input-field"
                placeholder="Create a password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="country" className="field-label">Country</label>
                <select
                  id="country"
                  name="country"
                  className="select-field"
                  value={formData.country}
                  onChange={handleChange}
                >
                  <option value="">Select country</option>
                  <option value="US">United States</option>
                  <option value="CA">Canada</option>
                  <option value="UK">United Kingdom</option>
                  <option value="AU">Australia</option>
                  <option value="IN">India</option>
                </select>
              </div>
              
              <div className="form-field">
                <label htmlFor="age" className="field-label">Age</label>
                <input
                  id="age"
                  name="age"
                  type="number"
                  className="input-field"
                  placeholder="Your age"
                  value={formData.age}
                  onChange={handleChange}
                  min="1"
                  max="100"
                />
              </div>
            </div>
          </div>
          
          <div className="form-navigation">
            <div className="previous-button-placeholder"></div>
            <button className="next-button" onClick={handleNext}>Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateProfile;