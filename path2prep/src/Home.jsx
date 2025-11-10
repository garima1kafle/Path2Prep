import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/create-profile');
  };

  return (
    <div className="home">
      {/* Header/Navigation */}
      <header className="header">
        <div className="container">
          <div className="logo">
            <div className="logo-icon">
              <div className="graduation-cap">
                <div className="cap-top"></div>
                <div className="cap-bottom"></div>
                <div className="tassel"></div>
              </div>
            </div>
            <h2>Path2Prep</h2>
          </div>
          <nav className="nav">
            <a href="#features">Features</a>
            <a href="#how-it-works">How it Works</a>
            <a href="#about">About</a>
            <a href="#signin" className="nav-signin">Sign In</a>
            <a href="#get-started" className="nav-get-started" onClick={handleGetStarted}>Get Started</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1>Your AI-Powered Path to<br /><span className="hero-highlight">Scholarships & Careers</span></h1>
            <p>Discover personalized scholarship opportunities and career recommendations using advanced AI technology. No more endless searching—we match you with the perfect opportunities.</p>
            <div className="hero-buttons">
              <button className="btn-primary" onClick={handleGetStarted}>
                Start Your Journey
                <span className="btn-arrow">→</span>
              </button>
              <button className="btn-secondary">Watch Demo</button>
            </div>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <h3>10,000+</h3>
              <p>Scholarships Tracked</p>
            </div>
            <div className="stat">
              <h3>95%</h3>
              <p>Match Accuracy</p>
            </div>
            <div className="stat">
              <h3>$50M+</h3>
              <p>Awarded to Students</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features">
        <div className="container">
          <h2>Powerful Features</h2>
          <p className="section-subtitle">Everything you need to succeed in one platform</p>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon ai-matching">
                <div className="icon-shape">
                  <div className="ai-line-1"></div>
                  <div className="ai-line-2"></div>
                  <div className="ai-line-3"></div>
                  <div className="ai-line-4"></div>
                  <div className="ai-line-5"></div>
                  <div className="ai-line-6"></div>
                  <div className="ai-line-7"></div>
                </div>
              </div>
              <h3>AI-Powered Matching</h3>
              <p>Advanced algorithms match you with the most relevant opportunities</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon career-guidance">
                <div className="icon-shape">
                  <div className="career-outer"></div>
                  <div className="career-middle"></div>
                  <div className="career-inner"></div>
                </div>
              </div>
              <h3>Career Guidance</h3>
              <p>Personalized career recommendations based on your profile and interests</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon smart-alerts">
                <div className="icon-shape">
                  <div className="alert-bell"></div>
                  <div className="alert-clapper"></div>
                </div>
              </div>
              <h3>Smart Alerts</h3>
              <p>Never miss a deadline with intelligent notification system</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon application-tracking">
                <div className="icon-shape">
                  <div className="arrow-up"></div>
                  <div className="arrow-line"></div>
                  <div className="chart-bars">
                    <div className="chart-bar bar-1"></div>
                    <div className="chart-bar bar-2"></div>
                    <div className="chart-bar bar-3"></div>
                  </div>
                </div>
              </div>
              <h3>Application Tracking</h3>
              <p>Manage all your applications from one comprehensive dashboard</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="how-it-works">
        <div className="container">
          <div className="section-header">
            <h2>How Path2Prep Works</h2>
            <p className="section-subtitle">Simple steps to unlock your potential</p>
          </div>
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Create Your Profile</h3>
              <p>Tell us about your academic background, interests, and career goals</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Get AI Recommendations</h3>
              <p>Our AI analyzes thousands of opportunities to find your perfect matches</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Apply & Track</h3>
              <p>Apply directly through our platform and track your progress</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <h2>Ready to Start Your Journey?</h2>
          <p>Join thousands of students who have found their path to success</p>
          <div className="cta-button-container">
            <button className="btn-primary cta-btn" onClick={handleGetStarted}>
              Get Started for Free
              <span className="btn-arrow">→</span>
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <div className="footer-logo">
                <div className="logo-icon">
                  <div className="graduation-cap">
                    <div className="cap-top"></div>
                    <div className="cap-bottom"></div>
                    <div className="tassel"></div>
                  </div>
                </div>
                <span>Path2Prep</span>
              </div>
              <p>Empowering students to achieve their dreams through AI-powered scholarship and career guidance.</p>
            </div>
            <div className="footer-section">
              <h4>Platform</h4>
              <ul>
                <li><a href="#features">Features</a></li>
                <li><a href="#how-it-works">How it Works</a></li>
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#api">API</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Support</h4>
              <ul>
                <li><a href="#help">Help Center</a></li>
                <li><a href="#contact">Contact Us</a></li>
                <li><a href="#privacy">Privacy Policy</a></li>
                <li><a href="#terms">Terms of Service</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Connect</h4>
              <ul>
                <li><a href="#twitter">Twitter</a></li>
                <li><a href="#linkedin">LinkedIn</a></li>
                <li><a href="#facebook">Facebook</a></li>
                <li><a href="#instagram">Instagram</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2025 Path2Prep. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;