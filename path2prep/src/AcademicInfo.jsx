import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AcademicInfo.css';

const AcademicInfo = () => {
  const navigate = useNavigate();
  const [academicData, setAcademicData] = useState({
    educationLevel: '',
    fieldOfStudy: '',
    gpa: '',
    graduationYear: '',
    institution: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setAcademicData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handlePrevious = () => {
    navigate('/');
  };

  const handleNext = () => {
    // You can add form validation here before navigating
    console.log('Academic data:', academicData);
    navigate('/career-interests');
  };

  return (
    <div className="academic-info-container">
      <div className="academic-info-card">
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
            <div className="step-indicator">Step 2 of 4</div>
          </div>
          <div className="progress-bar">
            <div className="progress-fill step-2"></div>
          </div>
        </div>
        
        <div className="academic-form">
          <div className="form-section">
            <div className="form-field">
              <label htmlFor="educationLevel" className="field-label">Current Education Level</label>
              <select
                id="educationLevel"
                name="educationLevel"
                className="select-field"
                value={academicData.educationLevel}
                onChange={handleChange}
              >
                <option value="">Select level</option>
                <option value="high-school">High School</option>
                <option value="undergraduate">Undergraduate</option>
                <option value="graduate">Graduate</option>
                <option value="postgraduate">Postgraduate</option>
                <option value="phd">PhD</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="fieldOfStudy" className="field-label">Field of Study</label>
              <select
                id="fieldOfStudy"
                name="fieldOfStudy"
                className="select-field"
                value={academicData.fieldOfStudy}
                onChange={handleChange}
              >
                <option value="">Select field</option>
                <option value="computer-science">Computer Science</option>
                <option value="engineering">Engineering</option>
                <option value="business">Business</option>
                <option value="medicine">Medicine</option>
                <option value="arts">Arts & Humanities</option>
                <option value="sciences">Natural Sciences</option>
                <option value="social-sciences">Social Sciences</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="gpa" className="field-label">GPA / Grade</label>
                <input
                  id="gpa"
                  name="gpa"
                  type="text"
                  className="input-field"
                  placeholder="e.g., 3.8"
                  value={academicData.gpa}
                  onChange={handleChange}
                />
              </div>
              
              <div className="form-field">
                <label htmlFor="graduationYear" className="field-label">Graduation Year</label>
                <input
                  id="graduationYear"
                  name="graduationYear"
                  type="number"
                  className="input-field"
                  placeholder="e.g., 2025"
                  value={academicData.graduationYear}
                  onChange={handleChange}
                  min="2000"
                  max="2050"
                />
              </div>
            </div>
            
            <div className="form-field">
              <label htmlFor="institution" className="field-label">Institution</label>
              <input
                id="institution"
                name="institution"
                type="text"
                className="input-field"
                placeholder="Your current school/university"
                value={academicData.institution}
                onChange={handleChange}
              />
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

export default AcademicInfo;