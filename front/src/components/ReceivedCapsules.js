import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

function ReceivedCapsules() {
  const [receivedCapsules, setReceivedCapsules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [viewingCapsule, setViewingCapsule] = useState(null);

  useEffect(() => {
    fetchReceivedCapsules();
  }, []);

  const fetchReceivedCapsules = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/capsules/received`);
      setReceivedCapsules(response.data);
    } catch (error) {
      console.error('Error fetching received capsules:', error);
    } finally {
      setLoading(false);
    }
  };

  const viewCapsule = async (capsuleId) => {
    try {
      const response = await axios.get(`${API_BASE}/capsules/shared/${capsuleId}`);
      setViewingCapsule(response.data);
    } catch (error) {
      console.error('Error fetching capsule:', error);
      alert('Error loading capsule. It might not be ready yet or does not exist.');
    }
  };

  const closeCapsuleView = () => {
    setViewingCapsule(null);
  };

  const CapsuleViewModal = ({ capsule, onClose }) => {
    if (!capsule) return null;

    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="modal-header">
            <h2>🎁 {capsule.title}</h2>
            <button className="close-button" onClick={onClose}>
              <i className="fas fa-times"></i>
            </button>
          </div>
          <div className="modal-body">
            <div className="capsule-meta-modal">
              <p><strong>From:</strong> {capsule.sender_name}</p>
              <p><strong>Delivery Date:</strong> {new Date(capsule.delivery_date).toLocaleDateString()}</p>
              <p><strong>Created:</strong> {new Date(capsule.created_at).toLocaleDateString()}</p>
            </div>
            
            <div className="capsule-message-modal">
              <h3>Message:</h3>
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
              Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="received-capsules">
      <h2>
        <i className="fas fa-gift"></i> Received Capsules
        {receivedCapsules.length > 0 && <span className="count-badge">{receivedCapsules.length}</span>}
      </h2>
      
      {loading ? (
        <div className="loading-state">
          <i className="fas fa-spinner fa-spin"></i>
          <p>Loading received capsules...</p>
        </div>
      ) : receivedCapsules.length === 0 ? (
        <div className="empty-state">
          <i className="fas fa-inbox"></i>
          <p>No capsules received yet.</p>
          <p className="small">Capsules sent to you will appear here once they're ready!</p>
        </div>
      ) : (
        receivedCapsules.map(capsule => (
          <div 
            key={capsule.id} 
            className="capsule-item received-capsule"
            onClick={() => viewCapsule(capsule.id)}
          >
            <div className="capsule-info">
              <h3>🎁 {capsule.title}</h3>
              <p className="capsule-message-preview">
                {capsule.message.length > 150 ? capsule.message.substring(0, 150) + '...' : capsule.message}
              </p>
              
              <div className="capsule-meta">
                <span>
                  <i className="fas fa-user"></i> 
                  From: {capsule.recipient_type === 'self' ? 'Yourself' : 'A Friend'}
                </span>
                <span>
                  <i className="fas fa-calendar"></i> 
                  Delivered: {new Date(capsule.delivery_date).toLocaleDateString()}
                </span>
                <span className="status-ready">
                  <i className="fas fa-check-circle"></i> 
                  Ready to open!
                </span>
              </div>
            </div>
            <div className="capsule-actions">
              <button 
                className="btn btn-primary"
                onClick={(e) => {
                  e.stopPropagation();
                  viewCapsule(capsule.id);
                }}
                title="Open capsule"
              >
                <i className="fas fa-eye"></i> View
              </button>
            </div>
          </div>
        ))
      )}

      {viewingCapsule && (
        <CapsuleViewModal 
          capsule={viewingCapsule} 
          onClose={closeCapsuleView} 
        />
      )}
    </div>
  );
}

export default ReceivedCapsules;