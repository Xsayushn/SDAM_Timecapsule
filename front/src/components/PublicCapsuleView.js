import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

function PublicCapsuleView() {
  const { capsuleId } = useParams();
  const [capsule, setCapsule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCapsule();
  }, [capsuleId]);

  const fetchCapsule = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/capsules/shared/${capsuleId}`);
      setCapsule(response.data);
    } catch (error) {
      setError(error.response?.data?.error || 'Capsule not found or not ready yet');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-fullscreen">
        <div className="loading-spinner"></div>
        <p>Loading capsule...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-fullscreen">
        <div className="error-content">
          <h1>❌ Unable to Open Capsule</h1>
          <p>{error}</p>
          <a href="/" className="btn btn-primary">Go to Time Capsule App</a>
        </div>
      </div>
    );
  }

  return (
    <div className="public-capsule-view">
      <header className="app-header">
        <div className="container">
          <h1><i className="fas fa-time-capsule"></i> Time Capsule</h1>
          <p>You've received a time capsule!</p>
        </div>
      </header>

      <div className="container">
        <div className="public-capsule-card">
          <div className="card-header">
            <h2>🎁 {capsule.title}</h2>
          </div>
          <div className="card-body">
            <div className="capsule-meta-public">
              <p><strong>From:</strong> {capsule.sender_name}</p>
              <p><strong>Delivered on:</strong> {new Date(capsule.delivery_date).toLocaleDateString()}</p>
              <p><strong>Created:</strong> {new Date(capsule.created_at).toLocaleDateString()}</p>
            </div>
            
            <div className="capsule-message-public">
              <h3>Message from the Past:</h3>
              <div className="message-content-public">
                {capsule.message}
              </div>
            </div>

            {capsule.media_files && capsule.media_files.length > 0 && (
              <div className="capsule-media-public">
                <h3>Attachments</h3>
                <div className="media-grid-public">
                  {capsule.media_files.map((file, index) => (
                    <div key={index} className="media-item-public">
                      {file.type.startsWith('image/') ? (
                        <img 
                          src={`http://localhost:5000/api/media/${file.filename}`} 
                          alt={file.original_name}
                        />
                      ) : (
                        <div className="video-item-public">
                          <i className="fas fa-video"></i>
                          <span>Video: {file.original_name}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
        
        <div className="public-actions">
          <a href="/" className="btn btn-primary">
            <i className="fas fa-plus"></i> Create Your Own Time Capsule
          </a>
        </div>
      </div>
    </div>
  );
}

export default PublicCapsuleView;