import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('scholarships');

  const stats = [
    { title: 'Recommended', value: '127', icon: 'recommended', color: 'blue' },
    { title: 'Applications', value: '8', icon: 'applications', color: 'green' },
    { title: 'Deadlines', value: '3', icon: 'deadlines', color: 'orange' },
    { title: 'Match Score', value: '94%', icon: 'match', color: 'purple' }
  ];

  const scholarships = [
    {
      title: 'Global Excellence Scholarship',
      organization: 'International Education Foundation',
      description: 'Merit-based scholarship for outstanding international students pursuing STEM degrees.',
      match: '95%',
      status: 'available',
      tags: ['GPA 3.5+', 'TOEFL 100+', 'STEM Field', 'Financial Need'],
      amount: '$25,000',
      location: 'United States',
      deadline: 'March 15, 2025'
    },
    {
      title: 'Tech Innovation Grant',
      organization: 'Future Tech Foundation',
      description: 'Supporting innovative students in computer science and IT fields.',
      match: '88%',
      status: 'applied',
      tags: ['CS/IT Major', 'Portfolio Required', 'GPA 3.0+'],
      amount: '$15,000',
      location: 'Canada',
      deadline: 'April 20, 2025'
    },
    {
      title: 'Women in Engineering Scholarship',
      organization: 'Engineering Excellence Society',
      description: 'Empowering women to pursue careers in engineering and technology.',
      match: '82%',
      status: 'available',
      tags: ['Female', 'Engineering Major', 'Leadership Experience'],
      amount: '$20,000',
      location: 'Australia',
      deadline: 'February 28, 2025'
    }
  ];

  const menuItems = [
    { name: 'Dashboard', icon: 'dashboard' },
    { name: 'Scholarships', icon: 'scholarships' },
    { name: 'Careers', icon: 'careers' },
    { name: 'Applications', icon: 'applications' },
    { name: 'Profile', icon: 'profile' }
  ];

  const handleTabClick = (tab) => {
    setActiveTab(tab);
    if (tab === 'careers') {
      navigate('/career-recommendations');
    }
  };

  return (
    <div className="dashboard">
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
            <h1>Welcome back, Ekta <span className="name-break">Rayamajhi!</span></h1>
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

          <div className="divider"></div>

          {/* Content Tabs */}
          <section className="content-section">
            <div className="content-tabs">
              <div className="tab-container">
                <button 
                  className={`tab ${activeTab === 'scholarships' ? 'active' : ''}`}
                  onClick={() => handleTabClick('scholarships')}
                >
                  Top Scholarships
                </button>
                <button 
                  className={`tab ${activeTab === 'careers' ? 'active' : ''}`}
                  onClick={() => handleTabClick('careers')}
                >
                  Career Matches
                </button>
                <button 
                  className={`tab ${activeTab === 'applications' ? 'active' : ''}`}
                  onClick={() => handleTabClick('applications')}
                >
                  My Applications
                </button>
              </div>
            </div>

            <div className="divider"></div>

            {/* Scholarships Header */}
            <div className="scholarships-header">
              <h2>Recommended Scholarships</h2>
              <button className="view-all-button">
                View All
              </button>
            </div>

            <div className="scholarships-list">
              {scholarships.map((scholarship, index) => (
                <div key={index} className="scholarship-card">
                  <div className="scholarship-content">
                    <div className="scholarship-main">
                      <div className="scholarship-header">
                        <div className="scholarship-title-section">
                          <h3>{scholarship.title}</h3>
                          <div className="scholarship-meta">
                            <span className={`match-badge ${scholarship.match === '95%' ? 'high-match' : scholarship.match === '88%' ? 'medium-match' : 'low-match'}`}>
                              {scholarship.match} Match
                            </span>
                            {scholarship.status === 'applied' && (
                              <span className="status-badge">Applied</span>
                            )}
                          </div>
                        </div>
                      </div>
                      
                      <p className="organization">{scholarship.organization}</p>
                      <p className="description">{scholarship.description}</p>
                      
                      <div className="tags">
                        {scholarship.tags.map((tag, tagIndex) => (
                          <span key={tagIndex} className="tag">{tag}</span>
                        ))}
                      </div>
                      
                      <div className="scholarship-details">
                        <div className="detail">
                          <div className="detail-icon amount">
                            <span className="dollar-symbol">$</span>
                          </div>
                          <span>{scholarship.amount}</span>
                        </div>
                        <div className="detail">
                          <div className="detail-icon location">
                            <div className="location-pin"></div>
                          </div>
                          <span>{scholarship.location}</span>
                        </div>
                        <div className="detail">
                          <div className="detail-icon calendar">
                            <div className="calendar-icon"></div>
                          </div>
                          <span>{scholarship.deadline}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="scholarship-actions">
                      <button className="save-button">Save</button>
                      {scholarship.status === 'available' && (
                        <button className="apply-button">Apply Now</button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

// Icon Components
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

export default Dashboard;