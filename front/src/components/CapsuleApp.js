import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext.js';
import axios from 'axios';
import ReceivedCapsules from './ReceivedCapsules.js';

const API_BASE = 'http://localhost:5000/api';

function CapsuleApp() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('sent');
  const [sentCapsules, setSentCapsules] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [viewingCapsule, setViewingCapsule] = useState(null);
  const [categories, setCategories] = useState([]);
  
  const [formData, setFormData] = useState({
    title: '',
    message: '',
    delivery_date: '',
    recipient_type: 'self',
    recipient_email: '',
    recipients: [],
    category: 'personal',
    tags: [],
    media_files: []
  });

  useEffect(() => {
    if (activeTab === 'sent') {
      fetchSentCapsules();
      fetchCategories();
    }
  }, [activeTab]);

  const fetchSentCapsules = async (query = '', category = '') => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (query) params.append('q', query);
      if (category) params.append('category', category);
      
      const response = await axios.get(`${API_BASE}/capsules/sent?${params}`);
      setSentCapsules(response.data);
    } catch (error) {
      console.error('Error fetching sent capsules:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE}/capsules/categories`);
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    fetchSentCapsules(query, selectedCategory);
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    fetchSentCapsules(searchQuery, category);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const fileReaders = files.map(file => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          resolve({
            filename: file.name,
            content: e.target.result,
            type: file.type,
            size: file.size
          });
        };
        reader.readAsDataURL(file);
      });
    });

    Promise.all(fileReaders).then(fileData => {
      setFormData(prev => ({
        ...prev,
        media_files: [...prev.media_files, ...fileData]
      }));
    });
  };

  const removeFile = (index) => {
    setFormData(prev => ({
      ...prev,
      media_files: prev.media_files.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.title.trim()) {
      alert('Please enter a capsule title');
      return;
    }
    
    if (!formData.message.trim()) {
      alert('Please enter a message');
      return;
    }
    
    if (!formData.delivery_date) {
      alert('Please select a delivery date');
      return;
    }

    if (formData.recipient_type === 'other' && !formData.recipient_email) {
      alert('Please enter recipient email');
      return;
    }

    // Validate file sizes (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    for (const file of formData.media_files) {
      if (file.size > maxSize) {
        alert(`File ${file.filename} exceeds 10MB limit`);
        return;
      }
    }

    try {
      setLoading(true);
      
      // Prepare data for backend
      const capsuleData = {
        title: formData.title,
        message: formData.message,
        delivery_date: formData.delivery_date,
        recipient_type: formData.recipient_type,
        category: formData.category,
        tags: formData.tags.filter(tag => tag.trim()),
        media_files: formData.media_files
      };

      if (formData.recipient_type === 'other') {
        capsuleData.recipient_email = formData.recipient_email;
      } else if (formData.recipient_type === 'multiple') {
        capsuleData.recipients = formData.recipients;
      }

      await axios.post(`${API_BASE}/capsules`, capsuleData);
      
      // Reset form
      setFormData({
        title: '',
        message: '',
        delivery_date: '',
        recipient_type: 'self',
        recipient_email: '',
        recipients: [],
        category: 'personal',
        tags: [],
        media_files: []
      });
      setShowForm(false);
      await fetchSentCapsules();
      alert('Time capsule created successfully!');
    } catch (error) {
      console.error('Error creating capsule:', error);
      const errorMsg = error.response?.data?.error || 'Error creating capsule. Please try again.';
      alert(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const deleteCapsule = async (id, e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this capsule? This action cannot be undone.')) {
      try {
        await axios.delete(`${API_BASE}/capsules/${id}`);
        await fetchSentCapsules();
      } catch (error) {
        console.error('Error deleting capsule:', error);
        alert('Error deleting capsule. Please try again.');
      }
    }
  };

  const viewCapsule = async (capsuleId) => {
    try {
      const response = await axios.get(`${API_BASE}/capsules/${capsuleId}`);
      setViewingCapsule(response.data);
    } catch (error) {
      console.error('Error fetching capsule:', error);
      alert('Error loading capsule details.');
    }
  };

  const closeCapsuleView = () => {
    setViewingCapsule(null);
  };

  const calculateCountdown = (deliveryDate) => {
    const today = new Date();
    const delivery = new Date(deliveryDate);
    const diffTime = delivery - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays > 0) {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''}`;
    } else if (diffDays === 0) {
      return 'Today!';
    } else {
      return 'Ready to open!';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  // Modal Component
  const CapsuleViewModal = ({ capsule, onClose }) => {
    if (!capsule) return null;

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="modal-header">
            <h2><i className="fas fa-time-capsule"></i> {capsule.title}</h2>
            <button className="close-button" onClick={onClose}>
              <i className="fas fa-times"></i>
            </button>
          </div>
          <div className="modal-body">
            <div className="capsule-meta-modal">
              <div>
                <strong>Delivery Date</strong>
                <p>{new Date(capsule.delivery_date).toLocaleDateString()}</p>
              </div>
              <div>
                <strong>Created</strong>
                <p>{new Date(capsule.created_at).toLocaleDateString()}</p>
              </div>
              <div>
                <strong>Category</strong>
                <p>{capsule.category || 'personal'}</p>
              </div>
              <div>
                <strong>Status</strong>
                <p>
                  <span className={`status-${capsule.status}`}>
                    <i className={`fas fa-${capsule.status === 'ready' ? 'check-circle' : 'lock'}`}></i>
                    {capsule.status === 'ready' ? 'Ready to Open!' : 'Locked'}
                  </span>
                </p>
              </div>
            </div>
            
            <div className="capsule-message-modal">
              <h3>Your Message:</h3>
              <div className="message-content">
                {capsule.message}
              </div>
            </div>

            {capsule.media_files && capsule.media_files.length > 0 && (
              <div className="capsule-media-modal">
                <h3>Attachments ({capsule.media_files.length})</h3>
                <div className="media-grid">
                  {capsule.media_files.map((file, index) => (
                    <div key={index} className="media-item-modal">
                      {file.type.startsWith('image/') ? (
                        <img 
                          src={`http://localhost:5000/api/media/${file.filename}`} 
                          alt={file.original_name}
                          onError={(e) => {
                            e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDE1MCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiBmaWxsPSIjRjVEM0M0Ii8+CjxwYXRoIGQ9Ik03NSA0M1YxMDciIHN0cm9rZT0iIzY5NkZDNyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHBhdGggZD0iTTQzIDc1SDEwNyIgc3Ryb2tlPSIjNjk2RkM3IiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K';
                          }}
                        />
                      ) : (
                        <div className="video-item">
                          <i className="fas fa-video"></i>
                          <span>Video Attachment</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          <div className="modal-footer">
            <button className="btn btn-primary" onClick={onClose}>
              <i className="fas fa-times"></i> Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Capsule Item Component
  const CapsuleItem = ({ capsule }) => {
    const statusClass = capsule.status === 'ready' ? 'status-ready-badge' : 'status-locked-badge';
    const statusIcon = capsule.status === 'ready' ? 'fa-check-circle' : 'fa-lock';
    
    return (
      <div 
        className="capsule-item"
        onClick={() => viewCapsule(capsule.id)}
      >
        <div className="capsule-info">
          <h3>
            <i className="fas fa-capsule"></i> {capsule.title}
            <span className={`status-badge ${statusClass}`}>
              <i className={`fas ${statusIcon}`}></i>
              {capsule.status === 'ready' ? 'Ready' : 'Locked'}
            </span>
          </h3>
          <p className="capsule-message">{capsule.message}</p>
          
          {capsule.media_files && capsule.media_files.length > 0 && (
            <div className="capsule-media">
              <p>
                <i className="fas fa-paperclip"></i> 
                {capsule.media_files.length} attached file{capsule.media_files.length !== 1 ? 's' : ''}
              </p>
            </div>
          )}
          
          <div className="capsule-meta">
            <span>
              <i className="fas fa-user"></i> 
              To: {capsule.recipient_type === 'self' ? 'Myself' : capsule.recipient_email}
            </span>
            <span>
              <i className="fas fa-calendar"></i> 
              Delivery: {new Date(capsule.delivery_date).toLocaleDateString()}
            </span>
            <span className="countdown">
              <i className="fas fa-clock"></i> 
              {calculateCountdown(capsule.delivery_date)}
            </span>
            <span>
              <i className="fas fa-tag"></i>
              Category: {capsule.category || 'personal'}
            </span>
          </div>
        </div>
        
        <div className="click-to-view">
          <i className="fas fa-eye"></i> Click to View
        </div>
        
        <div className="capsule-actions">
          <button 
            className="btn-danger"
            onClick={(e) => deleteCapsule(capsule.id, e)}
            title="Delete capsule"
          >
            <i className="fas fa-trash"></i>
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="capsule-app">
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div>
              <h1><i className="fas fa-time-capsule"></i> Time Capsule</h1>
              <p>Welcome back, {user.name}!</p>
            </div>
            <div className="header-actions">
              <Link to="/profile" className="btn btn-secondary">
                <i className="fas fa-user-circle"></i> Profile
              </Link>
              <button onClick={logout} className="btn btn-secondary">
                <i className="fas fa-sign-out-alt"></i> Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container">
        {/* Tab Navigation */}
        <div className="tabs-navigation">
          <button 
            className={`tab-button ${activeTab === 'sent' ? 'active' : ''}`}
            onClick={() => setActiveTab('sent')}
          >
            <i className="fas fa-paper-plane"></i> My Sent Capsules
          </button>
          <button 
            className={`tab-button ${activeTab === 'received' ? 'active' : ''}`}
            onClick={() => setActiveTab('received')}
          >
            <i className="fas fa-gift"></i> Received Capsules
          </button>
        </div>

        {activeTab === 'sent' ? (
          <>
            {/* Search and Filter Section - Only for sent capsules */}
            <div className="search-section">
              <div className="search-box">
                <i className="fas fa-search"></i>
                <input
                  type="text"
                  placeholder="Search your capsules..."
                  value={searchQuery}
                  onChange={handleSearch}
                />
              </div>
              <div className="category-filters">
                <button 
                  className={selectedCategory === '' ? 'btn active' : 'btn'}
                  onClick={() => handleCategoryFilter('')}
                >
                  All
                </button>
                {categories.map(category => (
                  <button 
                    key={category}
                    className={selectedCategory === category ? 'btn active' : 'btn'}
                    onClick={() => handleCategoryFilter(category)}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <div className="app-controls">
              <button 
                className="btn btn-primary"
                onClick={() => setShowForm(!showForm)}
                disabled={loading}
              >
                <i className="fas fa-plus"></i> {showForm ? 'Cancel' : 'Create New Capsule'}
              </button>
            </div>

            {showForm && (
              <div className="capsule-form-container">
                <div className="card">
                  <div className="card-header">
                    <i className="fas fa-plus-circle"></i> Create New Time Capsule
                  </div>
                  <div className="card-body">
                    <form onSubmit={handleSubmit}>
                      <div className="form-group">
                        <label htmlFor="title">Capsule Title *</label>
                        <input
                          type="text"
                          id="title"
                          name="title"
                          value={formData.title}
                          onChange={handleInputChange}
                          placeholder="e.g., Birthday Wishes for 2025"
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="message">Your Message *</label>
                        <textarea
                          id="message"
                          name="message"
                          value={formData.message}
                          onChange={handleInputChange}
                          placeholder="Write your future message here..."
                          required
                          rows="5"
                        />
                      </div>

                      <div className="form-group">
                        <label>Add Photos or Videos (Optional - Max 10MB each)</label>
                        <div className="upload-area">
                          <input
                            type="file"
                            multiple
                            accept="image/*,video/*"
                            onChange={handleFileUpload}
                          />
                          <i className="fas fa-cloud-upload-alt"></i>
                          <p>Click to upload or drag and drop</p>
                          <p className="small">PNG, JPG, MP4 up to 10MB</p>
                        </div>
                        <div className="media-preview">
                          {formData.media_files.map((file, index) => (
                            <div key={index} className="media-item">
                              <div className="media-preview-content">
                                {file.type.startsWith('image/') ? (
                                  <img src={file.content} alt="Preview" />
                                ) : (
                                  <div className="video-preview">
                                    <i className="fas fa-video"></i>
                                    <span>{file.filename}</span>
                                  </div>
                                )}
                                <div className="file-info">
                                  <span className="file-name">{file.filename}</span>
                                  <span className="file-size">{formatFileSize(file.size)}</span>
                                </div>
                              </div>
                              <button
                                type="button"
                                className="remove"
                                onClick={() => removeFile(index)}
                              >
                                <i className="fas fa-times"></i>
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="form-group">
                        <label htmlFor="category">Category</label>
                        <select
                          id="category"
                          name="category"
                          value={formData.category}
                          onChange={handleInputChange}
                        >
                          {categories.map(category => (
                            <option key={category} value={category}>
                              {category.charAt(0).toUpperCase() + category.slice(1)}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="form-group">
                        <label htmlFor="delivery_date">Delivery Date *</label>
                        <input
                          type="date"
                          id="delivery_date"
                          name="delivery_date"
                          value={formData.delivery_date}
                          onChange={handleInputChange}
                          min={new Date().toISOString().split('T')[0]}
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="recipient_type">Send To *</label>
                        <select
                          id="recipient_type"
                          name="recipient_type"
                          value={formData.recipient_type}
                          onChange={handleInputChange}
                        >
                          <option value="self">Myself</option>
                          <option value="other">Someone Else</option>
                        </select>
                      </div>

                      {formData.recipient_type === 'other' && (
                        <div className="form-group">
                          <label htmlFor="recipient_email">Recipient's Email *</label>
                          <input
                            type="email"
                            id="recipient_email"
                            name="recipient_email"
                            value={formData.recipient_email}
                            onChange={handleInputChange}
                            placeholder="Enter email address"
                            required
                          />
                        </div>
                      )}

                      <button 
                        type="submit" 
                        className="btn btn-primary btn-block" 
                        disabled={loading}
                      >
                        <i className="fas fa-lock"></i> {loading ? 'Creating...' : 'Lock Time Capsule'}
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            )}

            <div className="capsules-list">
              <h2>
                <i className="fas fa-archive"></i> My Sent Capsules
                {sentCapsules.length > 0 && <span className="count-badge">{sentCapsules.length}</span>}
              </h2>
              
              {loading ? (
                <div className="loading-state">
                  <i className="fas fa-spinner fa-spin"></i>
                  <p>Loading capsules...</p>
                </div>
              ) : sentCapsules.length === 0 ? (
                <div className="empty-state">
                  <i className="fas fa-inbox"></i>
                  <p>No capsules sent yet. Create your first one!</p>
                  <button 
                    className="btn btn-primary"
                    onClick={() => setShowForm(true)}
                  >
                    <i className="fas fa-plus"></i> Create First Capsule
                  </button>
                </div>
              ) : (
                sentCapsules.map(capsule => (
                  <CapsuleItem key={capsule.id} capsule={capsule} />
                ))
              )}
            </div>
          </>
        ) : (
          <ReceivedCapsules />
        )}

        {/* Capsule Viewing Modal */}
        {viewingCapsule && (
          <CapsuleViewModal 
            capsule={viewingCapsule} 
            onClose={closeCapsuleView} 
          />
        )}
      </div>
    </div>
  );
}

export default CapsuleApp;