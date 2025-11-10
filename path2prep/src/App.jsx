import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Home';
import CreateProfile from './CreateProfile';
import AcademicInfo from './AcademicInfo';
import CareerInterests from './CareerInterests';
import ProfileCompletion from './ProfileCompletion';
import Dashboard from './Dashboard';
import CareerRecommendations from './CareerRecommendations';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create-profile" element={<CreateProfile />} />
          <Route path="/academic-info" element={<AcademicInfo />} />
          <Route path="/career-interests" element={<CareerInterests />} />
          <Route path="/profile-completion" element={<ProfileCompletion />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/career-recommendations" element={<CareerRecommendations />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;