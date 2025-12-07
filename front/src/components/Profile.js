import React, { useState, useEffect } from 'react';
import { useAuth } from '../AuthContext.js';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

function Profile() {
  const { user, logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');
  const [message, setMessage] = useState({ type: '', text: '' });

  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  useEffect(() => {
    fetchUserProfile();
    fetchUserStats();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/user/profile`);
      setProfileData(prev => ({
        ...prev,
        name: response.data.name,
        email: response.data.email
      }));
    } catch (error) {
      console.error('Error fetching profile:', error);
      setMessage({ type: 'error', text: 'Failed to load profile' });
    } finally {
      setLoading(false);
    }
  };

  const fetchUserStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/user/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    
    // Validate password if changing
    if (profileData.new_password) {
      if (profileData.new_password.length < 6) {
        setMessage({ type: 'error', text: 'New password must be at least 6 characters' });
        return;
      }
      if (profileData.new_password !== profileData.confirm_password) {
        setMessage({ type: 'error', text: 'New passwords do not match' });
        return;
      }
      if (!profileData.current_password) {
        setMessage({ type: 'error', text: 'Current password is required to change password' });
        return;
      }
    }

    try {
      setSaving(true);
      setMessage({ type: '', text: '' });

      const updateData = {
        name: profileData.name,
        email: profileData.email
      };

      // Only include password fields if changing password
      if (profileData.new_password) {
        updateData.password = profileData.new_password;
        updateData.current_password = profileData.current_password;
      }

      const response = await axios.put(`${API_BASE}/user/profile`, updateData);
      
      setMessage({ 
        type: 'success', 
        text: response.data.message || 'Profile updated successfully!' 
      });

      // Clear password fields
      setProfileData(prev => ({
        ...prev,
        current_password: '',
        new_password: '',
        confirm_password: ''
      }));

      // Refresh stats
      await fetchUserStats();

    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Failed to update profile';
      setMessage({ type: 'error', text: errorMsg });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-fullscreen">
        <div className="loading-spinner"></div>
        <p>Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div>
              <h1><i className="fas fa-user-circle"></i> My Profile</h1>
              <p>Manage your account and view statistics</p>
            </div>
            <div className="header-actions">
              <button 
                onClick={() => window.history.back()} 
                className="btn btn-secondary"
              >
                <i className="fas fa-arrow-left"></i> Back
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container">
        {/* Profile Navigation */}
        <div className="profile-navigation">
          <button 
            className={`profile-nav-btn ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <i className="fas fa-user-edit"></i> Edit Profile
          </button>
          <button 
            className={`profile-nav-btn ${activeTab === 'stats' ? 'active' : ''}`}
            onClick={() => setActiveTab('stats')}
          >
            <i className="fas fa-chart-bar"></i> Statistics
          </button>
          <button 
            className={`profile-nav-btn ${activeTab === 'account' ? 'active' : ''}`}
            onClick={() => setActiveTab('account')}
          >
            <i className="fas fa-cog"></i> Account Settings
          </button>
        </div>

        {message.text && (
          <div className={`alert-message ${message.type}`}>
            <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-circle'}`}></i>
            {message.text}
          </div>
        )}

        {activeTab === 'profile' ? (
          <div className="profile-card">
            <div className="card-header">
              <h2><i className="fas fa-user-edit"></i> Edit Profile</h2>
            </div>
            <div className="card-body">
              <form onSubmit={handleProfileUpdate}>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="name">Full Name</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={profileData.name}
                      onChange={handleInputChange}
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="email">Email Address</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={profileData.email}
                      onChange={handleInputChange}
                      placeholder="Enter your email"
                      required
                    />
                  </div>
                </div>

                <div className="password-section">
                  <h3><i className="fas fa-lock"></i> Change Password (Optional)</h3>
                  
                  <div className="form-group">
                    <label htmlFor="current_password">Current Password</label>
                    <input
                      type="password"
                      id="current_password"
                      name="current_password"
                      value={profileData.current_password}
                      onChange={handleInputChange}
                      placeholder="Enter current password"
                    />
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label htmlFor="new_password">New Password</label>
                      <input
                        type="password"
                        id="new_password"
                        name="new_password"
                        value={profileData.new_password}
                        onChange={handleInputChange}
                        placeholder="Enter new password"
                      />
                      <p className="form-hint">Minimum 6 characters</p>
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="confirm_password">Confirm New Password</label>
                      <input
                        type="password"
                        id="confirm_password"
                        name="confirm_password"
                        value={profileData.confirm_password}
                        onChange={handleInputChange}
                        placeholder="Confirm new password"
                      />
                    </div>
                  </div>
                </div>

                <div className="form-actions">
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={saving}
                  >
                    <i className="fas fa-save"></i> {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        ) : activeTab === 'stats' ? (
          <div className="stats-container">
            {stats ? (
              <>
                <div className="stats-grid">
                  <div className="stat-card primary">
                    <div className="stat-icon">
                      <i className="fas fa-capsules"></i>
                    </div>
                    <div className="stat-content">
                      <h3>{stats.total_capsules}</h3>
                      <p>Total Capsules</p>
                    </div>
                  </div>
                  
                  <div className="stat-card success">
                    <div className="stat-icon">
                      <i className="fas fa-paper-plane"></i>
                    </div>
                    <div className="stat-content">
                      <h3>{stats.total_sent}</h3>
                      <p>Capsules Sent</p>
                    </div>
                  </div>
                  
                  <div className="stat-card secondary">
                    <div className="stat-icon">
                      <i className="fas fa-gift"></i>
                    </div>
                    <div className="stat-content">
                      <h3>{stats.total_received}</h3>
                      <p>Capsules Received</p>
                    </div>
                  </div>
                  
                  <div className="stat-card accent">
                    <div className="stat-icon">
                      <i className="fas fa-calendar-day"></i>
                    </div>
                    <div className="stat-content">
                      <h3>{stats.days_since_join}</h3>
                      <p>Days with us</p>
                    </div>
                  </div>
                </div>

                <div className="stats-details">
                  <div className="detail-card">
                    <h3><i className="fas fa-chart-pie"></i> Sent Capsules Status</h3>
                    <div className="detail-content">
                      <div className="status-item">
                        <span className="status-indicator locked"></span>
                        <span className="status-label">Locked</span>
                        <span className="status-count">{stats.locked_sent}</span>
                      </div>
                      <div className="status-item">
                        <span className="status-indicator ready"></span>
                        <span className="status-label">Ready</span>
                        <span className="status-count">{stats.ready_sent}</span>
                      </div>
                    </div>
                  </div>

                  {Object.keys(stats.categories).length > 0 && (
                    <div className="detail-card">
                      <h3><i className="fas fa-tags"></i> Categories</h3>
                      <div className="categories-list">
                        {Object.entries(stats.categories).map(([category, count]) => (
                          <div key={category} className="category-item">
                            <span className="category-name">{category}</span>
                            <span className="category-count">{count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="detail-card">
                    <h3><i className="fas fa-info-circle"></i> Account Info</h3>
                    <div className="account-info">
                      <div className="info-item">
                        <span className="info-label">Joined On:</span>
                        <span className="info-value">
                          {new Date(stats.joined_date).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="info-item">
                        <span className="info-label">Member for:</span>
                        <span className="info-value">{stats.days_since_join} days</span>
                      </div>
                      <div className="info-item">
                        <span className="info-label">Email:</span>
                        <span className="info-value">{user.email}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="loading-state">
                <i className="fas fa-spinner fa-spin"></i>
                <p>Loading statistics...</p>
              </div>
            )}
          </div>
        ) : (
          <div className="settings-card">
            <div className="card-header">
              <h2><i className="fas fa-cog"></i> Account Settings</h2>
            </div>
            <div className="card-body">
              <div className="settings-section">
                <h3><i className="fas fa-bell"></i> Notifications</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <h4>Email Notifications</h4>
                    <p>Receive emails when your capsules are ready</p>
                  </div>
                  <label className="switch">
                    <input type="checkbox" defaultChecked />
                    <span className="slider"></span>
                  </label>
                </div>
                
                <div className="setting-item">
                  <div className="setting-info">
                    <h4>Reminder Emails</h4>
                    <p>Get reminders for upcoming capsule deliveries</p>
                  </div>
                  <label className="switch">
                    <input type="checkbox" defaultChecked />
                    <span className="slider"></span>
                  </label>
                </div>
              </div>

              <div className="settings-section">
                <h3><i className="fas fa-shield-alt"></i> Security</h3>
                <div className="setting-item">
                  <div className="setting-info">
                    <h4>Two-Factor Authentication</h4>
                    <p>Add an extra layer of security to your account</p>
                  </div>
                  <button className="btn btn-secondary">
                    <i className="fas fa-qrcode"></i> Enable
                  </button>
                </div>
              </div>

              <div className="settings-section danger-zone">
                <h3><i className="fas fa-exclamation-triangle"></i> Danger Zone</h3>
                <div className="danger-actions">
                  <button 
                    className="btn btn-danger"
                    onClick={() => {
                      if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
                        alert('Account deletion feature coming soon!');
                      }
                    }}
                  >
                    <i className="fas fa-trash"></i> Delete Account
                  </button>
                  
                  <button 
                    onClick={logout}
                    className="btn btn-secondary"
                  >
                    <i className="fas fa-sign-out-alt"></i> Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;