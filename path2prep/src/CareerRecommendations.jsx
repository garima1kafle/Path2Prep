import React, { useState } from 'react';
import './CareerRecommendations.css';

const CareerRecommendations = () => {
  const [activeTab, setActiveTab] = useState('careers');

  const stats = [
    { title: 'Recommended', value: '127', icon: 'recommended', color: 'blue' },
    { title: 'Applications', value: '8', icon: 'applications', color: 'green' },
    { title: 'Deadlines', value: '3', icon: 'deadlines', color: 'orange' },
    { title: 'Match Score', value: '94%', icon: 'match', color: 'purple' }
  ];

  const careers = [
    {
      title: 'AI/Machine Learning Engineer',
      description: 'Design and implement AI systems and machine learning models to solve complex problems.',
      match: '92%',
      salary: '$130,000',
      growth: '+22%',
      skills: ['Python', 'TensorFlow', 'Statistics', 'Neural Networks']
    },
    {
      title: 'Data Scientist',
      description: 'Analyze complex data to help organizations make informed business decisions.',
      match: '87%',
      salary: '$115,000',
      growth: '+35%',
      skills: ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics']
    },
    {
      title: 'Software Developer',
      description: 'Create applications, websites, and systems that power modern technology.',
      match: '84%',
      salary: '$105,000',
      growth: '+25%',
      skills: ['JavaScript', 'React', 'Node.js', 'Database Design']
    }
  ];

  const menuItems = [
    { name: 'Dashboard', icon: 'dashboard' },
    { name: 'Scholarships', icon: 'scholarships' },
    { name: 'Careers', icon: 'careers' },
    { name: 'Applications', icon: 'applications' },
    { name: 'Profile', icon: 'profile' }
  ];

  return (
    <div className="career-recommendations">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">
              <div className="icon-top"></div>
              <div className="icon-bottom"></div>
            </div>
            <span className="logo-text">Path2Prep</span>
          </div>
          <div className="header-actions">
            <button className="icon-button">
              <div className="search-icon">
                <div className="search-magnifier"></div>
                <div className="search-handle"></div>
              </div>
            </button>
            <button className="icon-button">
              <div className="bell-icon">
                <div className="bell-body"></div>
                <div className="bell-clapper"></div>
              </div>
            </button>
            <div className="user-avatar">
              <span>ER</span>
            </div>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        {/* Sidebar */}
        <aside className="sidebar">
          <nav className="sidebar-nav">
            {menuItems.map((item, index) => (
              <div key={index} className="nav-item">
                <div className={`nav-icon ${item.icon}`}>
                  {item.icon === 'dashboard' && <DashboardIcon />}
                  {item.icon === 'scholarships' && <ScholarshipsIcon />}
                  {item.icon === 'careers' && <CareersIcon />}
                  {item.icon === 'applications' && <ApplicationsIcon />}
                  {item.icon === 'profile' && <ProfileIcon />}
                </div>
                <span className="nav-text">{item.name}</span>
              </div>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {/* Welcome Section */}
          <section className="welcome-section">
            <h1>Welcome back, Ekta Rayamajhi!</h1>
            <p>Here's your personalized scholarship and career dashboard.</p>
          </section>

          {/* Stats Grid */}
          <section className="stats-grid">
            {stats.map((stat, index) => (
              <div key={index} className="stat-card">
                <div className="stat-content">
                  <div className="stat-info">
                    <span className="stat-title">{stat.title}</span>
                    <span className="stat-value">{stat.value}</span>
                  </div>
                  <div className={`stat-icon ${stat.color}`}>
                    {stat.icon === 'recommended' && <RecommendedIcon />}
                    {stat.icon === 'applications' && <ApplicationsStatIcon />}
                    {stat.icon === 'deadlines' && <DeadlinesIcon />}
                    {stat.icon === 'match' && <MatchIcon />}
                  </div>
                </div>
              </div>
            ))}
          </section>

          <div className="content-section">
            {/* Content Tabs */}
            <div className="content-tabs">
              <div className="tab-container">
                <button 
                  className={`tab ${activeTab === 'scholarships' ? 'active' : ''}`}
                  onClick={() => setActiveTab('scholarships')}
                >
                  Top Scholarships
                </button>
                <button 
                  className={`tab ${activeTab === 'careers' ? 'active' : ''}`}
                  onClick={() => setActiveTab('careers')}
                >
                  Career Matches
                </button>
                <button 
                  className={`tab ${activeTab === 'applications' ? 'active' : ''}`}
                  onClick={() => setActiveTab('applications')}
                >
                  My Applications
                </button>
              </div>
            </div>

            {/* Career Recommendations Header */}
            <div className="career-header">
              <h2>Career Recommendations</h2>
              <button className="career-assessment-button">
                Career Assessment
                <div className="arrow-icon">
                  <div className="arrow-line"></div>
                  <div className="arrow-head"></div>
                </div>
              </button>
            </div>

            {/* Career Cards */}
            <div className="careers-list">
              {careers.map((career, index) => (
                <div key={index} className="career-card">
                  <div className="career-content">
                    <div className="career-header-section">
                      <h3>{career.title}</h3>
                      <div className="career-meta">
                        <span className="match-badge">{career.match} Match</span>
                      </div>
                    </div>
                    
                    <p className="career-description">{career.description}</p>
                    
                    <div className="career-stats">
                      <div className="stat-item">
                        <span className="stat-label">Avg. Salary</span>
                        <span className="salary-value">{career.salary}</span>
                      </div>
                      <div className="stat-item">
                        <span className="stat-label">Job Growth</span>
                        <span className="growth-value">{career.growth}</span>
                      </div>
                    </div>
                    
                    <div className="skills-section">
                      <span className="skills-label">Required Skills</span>
                      <div className="skills-tags">
                        {career.skills.map((skill, skillIndex) => (
                          <span key={skillIndex} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="career-actions">
                      <button className="learn-more-button">Learn More</button>
                      <button className="find-jobs-button">Find Related Jobs</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

// Reuse the same icon components from Dashboard
const DashboardIcon = () => (
  <div className="icon-shape">
    <div className="dashboard-square"></div>
    <div className="dashboard-middle"></div>
    <div className="dashboard-center"></div>
  </div>
);

const ScholarshipsIcon = () => (
  <div className="icon-shape">
    <div className="scholarship-outer"></div>
    <div className="scholarship-inner"></div>
  </div>
);

const CareersIcon = () => (
  <div className="icon-shape">
    <div className="career-top"></div>
    <div className="career-middle"></div>
    <div className="career-bottom"></div>
  </div>
);

const ApplicationsIcon = () => (
  <div className="icon-shape">
    <div className="application-arrow"></div>
    <div className="application-body"></div>
  </div>
);

const ProfileIcon = () => (
  <div className="icon-shape">
    <div className="profile-top"></div>
    <div className="profile-bottom"></div>
  </div>
);

const RecommendedIcon = () => (
  <div className="icon-shape">
    <div className="recommended-outer"></div>
    <div className="recommended-inner"></div>
  </div>
);

const ApplicationsStatIcon = () => (
  <div className="icon-shape">
    <div className="applications-arrow"></div>
    <div className="applications-body"></div>
  </div>
);

const DeadlinesIcon = () => (
  <div className="icon-shape">
    <div className="deadlines-bell"></div>
    <div className="deadlines-clapper"></div>
  </div>
);

const MatchIcon = () => (
  <div className="icon-shape">
    <div className="match-outer"></div>
    <div className="match-middle"></div>
    <div className="match-inner"></div>
  </div>
);

export default CareerRecommendations;